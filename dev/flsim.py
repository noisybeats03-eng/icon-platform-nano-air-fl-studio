"""Tiny FL Studio scripting simulator to exercise device_iCON_PlatformNanoAir.py outside FL.

Usage: python -I flsim.py <script.py>
Uses FL's real midi.py / utils.py; every other FL module is a recording stub.
"""
import sys, types, importlib.util, time

FL_LIB = r'C:\Program Files\Image-Line\FL Studio 2025\Shared\Python\Lib'
sys.path.insert(0, FL_LIB)
import midi  # noqa: E402  (FL's real constants)

calls = []


class Stub:
    def __init__(self, name, **overrides):
        self._name = name
        self._over = overrides

    def __getattr__(self, attr):
        if attr in self._over:
            return self._over[attr]

        def f(*a, **k):
            calls.append((self._name + '.' + attr, a))
            return 0
        return f


# --- a small mixer model
state = {'sel': 8, 'vol': {}, 'mute': set(), 'solo': set(), 'arm': set()}
for t in range(0, 30):
    state['vol'][t * 1000 + midi.REC_Mixer_Vol] = 0.1 + 0.03 * t   # each track a different volume
state['vol'][midi.REC_MainVol] = 0.8


def getTrackPluginId(t, slot):
    return t * 1000 + slot


def getEventValue(eid, *a):
    return round(state['vol'].get(eid, 0.5) * midi.FromMIDI_Max)


def automateEvent(eid, value, *a):
    calls.append(('mixer.automateEvent', (eid, value)))
    if len(a) >= 3 and a[2]:  # isIncrement: knobs step by value * res
        res = a[3] if len(a) >= 4 else 0.01
        state['vol'][eid] = min(1.0, max(0.0, state['vol'].get(eid, 0.5) + value * res))
    else:
        state['vol'][eid] = value / midi.FromMIDI_Max
    return 0


def rec(name, ret=0):
    def f(*a, **k):
        calls.append((name, a))
        return ret
    return f


# --- screen models: the LCD (2 rows x 56 characters) and the 10-digit time display
state['tempo'] = 140.0
toggles = {'metro': 0, 'looprec': 0, 'precount': 0, 'snap': 3, 'loopmode': 0}
LCD = [' '] * 112
DIG = [0] * 10


def lcd_sysex(b):
    calls.append(('device.midiOutSysex', (b,)))
    if bytes(b[:6]) == bytes([0xF0, 0, 0, 0x66, 0x14, 0x12]):
        off = b[6]
        for i, ch in enumerate(b[7:-1]):
            if off + i < 112:
                LCD[off + i] = chr(ch)


def out_msg(m):
    calls.append(('device.midiOutMsg', (m,)))
    if (m & 0xFF) == 0xB0 and 0x40 <= ((m >> 8) & 0x7F) <= 0x49:
        DIG[0x49 - ((m >> 8) & 0x7F)] = (m >> 16) & 0x7F


def global_transport(cmd, val, *a):
    calls.append(('transport.globalTransport', (cmd, val) + a))
    if val:
        if cmd == midi.FPT_Metronome:
            toggles['metro'] ^= 1
        elif cmd == midi.FPT_LoopRecord:
            toggles['looprec'] ^= 1
        elif cmd == midi.FPT_CountDown:
            toggles['precount'] ^= 1
        elif cmd == midi.FPT_Snap:
            toggles['snap'] = 0 if toggles['snap'] == 3 else 3
        elif cmd == midi.FPT_Loop:
            toggles['loopmode'] ^= 1
    return midi.GT_Global


def base_track_select(index, step):
    calls.append(('device.baseTrackSelect', (index, step)))
    if index == 1:
        state['sel'] = max(0, min(29, state['sel'] + step))


def value_string(eid, v):
    if eid == midi.REC_Tempo:
        return '%.3f' % v
    if v > 100000:  # FL 2025: given a value on getEventValue's scale (0..2^30), FL answers 'INFdB'
        return 'INFdB'
    if (eid - midi.REC_Mixer_Pan) % 1000 == 0:  # a track's pan
        p = v / 12800
        if abs(p - 0.5) < 0.005:
            return 'Centered'
        return '%d%% %s' % (round(abs(p - 0.5) * 200), 'left' if p < 0.5 else 'right')
    return '%.1fdB' % (v / 12800 * 10 - 10)  # getAutoSmoothEventValue's scale works


def track_volume(t, mode=0):
    v = state['vol'].get(t * 1000 + midi.REC_Mixer_Vol, 0.5)
    if mode == 1:
        return v * 10 - 10 if v > 0 else float('-inf')
    return v


mixer = Stub('mixer',
             trackNumber=lambda: state['sel'],
             setTrackNumber=lambda t, *a: (calls.append(('mixer.setTrackNumber', (t,))), state.__setitem__('sel', t)),
             getTrackName=lambda t, *a: 'Master' if t == 0 else 'Insert %d' % t,
             getCurrentTempo=lambda *a: state['tempo'],
             getTrackPluginId=getTrackPluginId,
             getEventValue=getEventValue,
             automateEvent=automateEvent,
             getAutoSmoothEventValue=lambda eid: round(state['vol'].get(eid, 0.5) * 12800),
             getEventIDValueString=value_string,
             getTrackVolume=track_volume,
             getEventIDName=lambda eid: 'E%d' % eid,
             trackCount=lambda: 30,
             isTrackArmed=lambda t: t in state['arm'],
             isTrackSolo=lambda t: t in state['solo'],
             isTrackEnabled=lambda t: t not in state['mute'],
             enableTrack=lambda t: (calls.append(('mixer.enableTrack', (t,))), state['mute'].symmetric_difference_update({t})),
             armTrack=lambda t: (calls.append(('mixer.armTrack', (t,))), state['arm'].symmetric_difference_update({t})),
             soloTrack=lambda t, *a: calls.append(('mixer.soloTrack', (t,))),
             getTrackPeaks=lambda *a: 0.0,
             getTrackRecordingFileName=lambda t: 'f.wav',
             getRouteSendActive=lambda a, b: 0,
             isTrackPluginValid=lambda *a: False,
             isTrackAutomationEnabled=lambda *a: False,
             remoteFindEventValue=lambda *a: -1)
device = Stub('device', isAssigned=lambda: True, dispatchReceiverCount=lambda: 0, getPortNumber=lambda: 1,
              midiOutMsg=out_msg, midiOutNewMsg=rec('device.midiOutNewMsg'),
              midiOutSysex=lcd_sysex, baseTrackSelect=base_track_select)
transport = Stub('transport', globalTransport=global_transport, isPlaying=lambda: 0,
                 getLoopMode=lambda: toggles['loopmode'], isRecording=lambda: 0)
ui = Stub('ui', getProgTitle=lambda: 'FL Studio', getVersion=lambda *a: '25.2.5', getFocused=lambda w: 0,
          getSnapMode=lambda: toggles['snap'], getTimeDispMin=lambda: 0, isLoopRecEnabled=lambda: toggles['looprec'],
          getHintMsg=lambda: 'hint', isInPopupMenu=lambda: 0, getFocusedFormCaption=lambda: 'Mixer - Insert 3',
          isClosing=lambda: 0, showWindow=rec('ui.showWindow'))
general = Stub('general', getUndoLevelHint=lambda: '1/5', getChangedFlag=lambda: 0,
               getUseMetronome=lambda: toggles['metro'], getPrecount=lambda: toggles['precount'])
playlist = Stub('playlist', getVisTimeBar=lambda: 1, getVisTimeStep=lambda: 0, getVisTimeTick=lambda: 0)
channels = Stub('channels', getChannelName=lambda i: 'Kick Drum', channelNumber=lambda: 0)
patterns = Stub('patterns', getPatternName=lambda i: 'Pattern %d' % i, patternNumber=lambda: 1)
for name, mod in [('mixer', mixer), ('device', device), ('transport', transport), ('ui', ui), ('general', general),
                  ('playlist', playlist), ('channels', channels), ('patterns', patterns),
                  ('arrangement', Stub('arrangement')), ('launchMapPages', Stub('launchMapPages'))]:
    sys.modules[name] = mod


class Ev:
    def __init__(self, status, d1, d2):
        self.midiId = status & 0xF0
        self.midiChan = status & 0x0F
        self.midiChanEx = self.midiChan
        self.data1, self.data2 = d1, d2
        self.pmeFlags = midi.PME_System | midi.PME_System_Safe
        self.handled = False
        self.inEv = self.outEv = 0
        self.isIncrement = 0


spec = importlib.util.spec_from_file_location('nano', sys.argv[1])
nano = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nano)
S = nano.MackieCU
fails = 0


class FakeTime:
    """the script's clock, moved by hand so the screen's time-outs and read-backs can be tested"""
    def __init__(self):
        self.t = 1000.0

    def time(self):
        return self.t

    def ctime(self, *a):
        return 'now'


clock = FakeTime()
nano.time = clock


def check(cond, what):
    global fails
    print(('PASS ' if cond else 'FAIL ') + what)
    if not cond:
        fails += 1


def note(n, v):
    S.OnMidiMsg(Ev(0x90, n, v))


def cc(n, v):
    S.OnMidiMsg(Ev(0xB0, n, v))


def pb_out(ch):
    """last pitch-bend value sent to the device on channel ch"""
    for name, a in reversed(calls):
        if name in ('device.midiOutNewMsg', 'device.midiOutMsg') and (a[0] & 0xFF) == 0xE0 + ch:
            m = a[0]
            return ((m >> 8) & 0x7F) | (((m >> 16) & 0x7F) << 7)
    return None


S.OnInit()
S.OnRefresh(0xFFFF)
for _ in range(3):
    S.OnIdle()
check(True, 'OnInit / OnRefresh / OnIdle run without exceptions')

# A. fader follows the selected track
state['sel'] = 9
calls.clear()
S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
exp9 = S.AlphaTrack_LevelToSlider(getEventValue(9 * 1000 + midi.REC_Mixer_Vol))
check(all(pb_out(ch) == exp9 for ch in range(8)), 'selection -> track 9 volume sent on strips 1-8 (%s)' % exp9)
state['sel'] = 8
calls.clear()
S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
exp8 = S.AlphaTrack_LevelToSlider(getEventValue(8 * 1000 + midi.REC_Mixer_Vol))
check(pb_out(3) == exp8 and exp8 != exp9, 'selection -> back to track 8 (%s), strip 4 moved' % exp8)

# selected track volume changed elsewhere (track not in the bank)
state['sel'] = 20
S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
state['vol'][20 * 1000 + midi.REC_Mixer_Vol] = 0.33
calls.clear()
S.OnDirtyMixerTrack(20)
S.OnRefresh(midi.HW_Dirty_Mixer_Controls)
check(pb_out(3) == S.AlphaTrack_LevelToSlider(round(0.33 * midi.FromMIDI_Max)), 'selected track 20 volume change -> fader updated')

# fader moved by hand on strip 4 -> selected track volume
calls.clear()
S.OnMidiMsg(Ev(0xE3, 0, 64))  # pitch bend ch 4, value 8192
autos = [a for n, a in calls if n == 'mixer.automateEvent']
check(autos and autos[0][0] == 20 * 1000 + midi.REC_Mixer_Vol, 'hand move on strip 4 -> automates track 20 volume')

# Mute / Solo / Rec act on the selected track
calls.clear()
note(0x13, 127); note(0x13, 0)
check(('mixer.enableTrack', (20,)) in calls, 'Mute (strip 4) -> mutes selected track 20')
calls.clear()
note(0x03, 127); note(0x03, 0)
check(('mixer.armTrack', (20,)) in calls, 'Rec (strip 4) -> arms selected track 20')
calls.clear()
note(0x0B, 127); note(0x0B, 0)
check(('mixer.soloTrack', (20,)) in calls, 'Solo (strip 4) -> solos selected track 20')

# master strip keeps FL's behaviour
calls.clear()
S.OnMidiMsg(Ev(0xE8, 0, 100))
autos = [a for n, a in calls if n == 'mixer.automateEvent']
check(autos and autos[0][0] == midi.REC_MainVol, 'master fader -> Main volume (unchanged)')

# B. wheel modes: hold + wheel = momentary, tap = latch
note(0x3F, 127); cc(0x3C, 1); note(0x3F, 0)
check(S.JogSource == 0, 'hold Mixer + turn wheel -> off after release')
note(0x3F, 127); note(0x3F, 0)
check(S.JogSource == 0x3F, 'tap Mixer -> stays on')
calls.clear()
cc(0x3C, 1)
check(any(n == 'device.baseTrackSelect' for n, a in calls), 'wheel while Mixer latched -> selects next mixer track')
note(0x3F, 127); note(0x3F, 0)
check(S.JogSource == 0, 'tap Mixer again -> off')

# Undo tap, Loop, Zoom (from earlier rounds)
calls.clear()
note(0x3C, 127); note(0x3C, 0)
check(any(n == 'transport.globalTransport' and a[0] == midi.FPT_UndoUp for n, a in calls), 'Undo tap -> FPT_UndoUp')
calls.clear()
note(0x56, 127); note(0x56, 0)
check(any(n == 'transport.globalTransport' and a[0] == midi.FPT_LoopRecord for n, a in calls), 'Loop -> loop recording')
note(0x64, 127); note(0x64, 0)
calls.clear()
note(0x60, 127); note(0x60, 0)
check(any(n == 'transport.globalTransport' and a[0] == midi.FPT_VZoomJog for n, a in calls), 'Zoom + up -> vertical zoom')
note(0x64, 127); note(0x64, 0)
check(S.JogSource == 0, 'Zoom off again')


# C. the Nano's small screen (round 6): top line = LCD row 2 (offset 56), bottom line = row 1 (offset 0)
def screen(strip=None):
    """the Nano's own small screen = the square of the strip the fader is on (round 8 learns it; 0 before)"""
    if strip is None:
        strip = max(0, getattr(S, 'NanoStrip', 0))
    top = ''.join(LCD[56 + 7 * strip:63 + 7 * strip])
    bottom = ''.join(LCD[7 * strip:7 + 7 * strip])
    return (top.rstrip(), bottom.rstrip())


def squares():
    return [screen(k) for k in range(8)]


def on_all_strips():
    return all(screen(k) == screen(0) for k in range(8))


def wait(seconds):
    """let time pass in small steps, with FL calling OnIdle about every 20 ms"""
    end = clock.t + seconds
    while clock.t < end:
        clock.t = min(end, clock.t + 0.02)
        S.OnIdle()


def digits():
    out = ''
    for v in DIG:
        c = v & 0x3F
        out += chr(c) if c >= 0x20 else ' '
        if v & 0x40:
            out += '.'
    return out


def tap(n):
    note(n, 127)
    note(n, 0)


if getattr(nano, 'NanoScreen', False):
    vid20 = 20 * 1000 + midi.REC_Mixer_Vol
    state['vol'][vid20] = 0.8
    state['sel'] = 20
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
    wait(3)
    check(screen() == ('Ins 20', '-2.0dB') and (on_all_strips() or getattr(S, 'NanoStrip', -1) >= 0), 'normal view: selected track on top, its volume below %r' % (screen(),))
    S.UpdateMeterMode()
    wait(1)
    check('.' not in ''.join(LCD[56:]), 'no meter split marks on the top line')

    tap(0x57); wait(0.2)
    check(screen() == ('METRO', 'ON'), 'Metronome -> METRO / ON %r' % (screen(),))
    tap(0x57); wait(0.2)
    check(screen() == ('METRO', 'OFF'), 'Metronome again -> METRO / OFF %r' % (screen(),))
    wait(1.5)
    check(screen() == ('Ins 20', '-2.0dB'), 'message gone -> normal view again %r' % (screen(),))
    tap(0x56); wait(0.2)
    exp = 'ON' if toggles['looprec'] else 'OFF'
    check(screen() == ('LOOPREC', exp), 'Loop -> LOOPREC / %s %r' % (exp, screen()))
    tap(0x56); wait(0.2)
    exp = 'ON' if toggles['looprec'] else 'OFF'
    check(screen() == ('LOOPREC', exp), 'Loop again -> LOOPREC / %s %r' % (exp, screen()))
    note(0x54, 127); tap(0x56); note(0x54, 0); wait(0.2)
    check(screen() == ('SNAP', 'ON'), 'Shift + Loop -> SNAP / ON %r' % (screen(),))
    tap(0x58); wait(0.2)
    check(screen() == ('3..2..1', 'ON'), 'Count-in -> 3..2..1 / ON %r' % (screen(),))
    tap(0x5A); wait(0.2)
    check(screen() == ('MODO', 'SONG'), 'Pattern/Song -> MODO / SONG %r' % (screen(),))
    tap(0x10); wait(0.2)
    exp = 'ON' if 20 in state['mute'] else 'OFF'
    check(screen() == ('MUTE', exp), 'Mute -> MUTE / %s %r' % (exp, screen()))
    tap(0x10); wait(0.2)
    exp = 'ON' if 20 in state['mute'] else 'OFF'
    check(screen() == ('MUTE', exp), 'Mute again -> MUTE / %s %r' % (exp, screen()))
    tap(0x50); wait(0.5)
    check(screen() == ('SAVE', 'OK'), 'Save -> SAVE / OK %r' % (screen(),))
    tap(0x3C); wait(0.2)
    check(screen() == ('UNDO', '1/5'), 'Undo tap -> UNDO / level %r' % (screen(),))
    tap(0x28); wait(0.1)
    check(screen() == ('PAN', 'PAGINA'), 'Pan page button -> PAN / PAGINA %r' % (screen(),))
    wait(1.5)

    tap(0x3F); wait(0.1)
    check(screen() == ('MIXER', 'Ins 20'), 'Mixer mode on -> MIXER / current track %r' % (screen(),))
    cc(0x3C, 1); wait(0.1)
    check(screen() == ('MIXER', 'Ins 21'), 'wheel in Mixer mode -> next track shown %r' % (screen(),))
    tap(0x3F); wait(0.1)
    check(screen() == ('MIXER', 'OFF'), 'Mixer mode off -> MIXER / OFF %r' % (screen(),))
    wait(1.5)
    check(screen()[0] == 'Ins 21', 'then the normal view of the new track %r' % (screen(),))
    tap(0x41); wait(0.1)
    check(screen() == ('TEMPO', '140'), 'Tempo mode -> TEMPO / 140 %r' % (screen(),))
    check(digits().strip() == '140.00', 'Tempo mode -> digits show 140.00 (%r)' % digits())
    tap(0x41); wait(1.5)
    check('.' not in digits(), 'Tempo mode off -> digits show the song position again (%r)' % digits())
    tap(0x40); wait(0.1)
    check(screen() == ('CHANNEL', 'KickDrm'), 'Channel mode -> CHANNEL / channel name %r' % (screen(),))
    tap(0x40); wait(1.5)
    tap(0x3E); wait(0.1)
    check(screen() == ('PATTERN', 'Pat 1'), 'Pattern mode -> PATTERN / Pat 1 %r' % (screen(),))
    tap(0x3E); wait(1.5)
    tap(0x4C); wait(0.1)
    check(screen() == ('WINDOW', 'Mixer'), 'Window mode -> WINDOW / Mixer %r' % (screen(),))
    tap(0x4C); wait(1.5)
    tap(0x64); wait(0.1)
    check(screen() == ('ZOOM', 'ON'), 'Zoom -> ZOOM / ON %r' % (screen(),))
    tap(0x64); wait(1.5)

    S.OnMidiMsg(Ev(0xE0, 0, 100)); wait(0.05)
    check(screen()[0] == 'Ins 21' and S.NanoTemp is None, 'fader move -> normal view stays (track + live volume) %r' % (screen(),))
    S.OnMidiMsg(Ev(0xE8, 0, 90)); wait(0.05)
    check(screen()[0] == 'MASTER', 'master fader -> MASTER / value %r' % (screen(),))
    wait(1.5)

    P = S.NanoParse
    check(P('Control smoothing on') == ('SMOOTH', 'ON'), 'parse: smoothing')
    check(P('Zoom on: up/down = vertical, left/right = horizontal') == ('ZOOM', 'ON'), 'parse: zoom on')
    check(P('Linked to FL Studio (25.2.5)') == ('FL', 'LISTO'), 'parse: linked')
    check(P('Insert 3 - Pan: 25% left') == ('Pan', '25%L'), 'parse: knob %r' % (P('Insert 3 - Pan: 25% left'),))
    check(P('Cut') == ('Cut', ''), 'parse: short message')
    check(P('Horizontal meters mode') == ('METERS', 'HORIZ'), 'parse: meters')
    check(P('Pattern off') == ('PATTERN', 'OFF'), 'parse: mode off')
    check(nano.NanoAbbrev('Insert 125') == 'Ins 125' and nano.NanoAbbrev('Kick Drum') == 'KickDrm', 'names squeezed to 7 characters')
    check(nano.NanoShort('-inf dB') == '-INF dB' and nano.NanoShort('-3.2 dB') == '-3.2dB', 'values squeezed')
    check(nano.NanoFit('Canci' + chr(0xF3) + 'n') == 'Cancion', 'accents folded')

    state['sel'] = 501
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel | midi.HW_Dirty_Mixer_Controls); wait(0.8)
    check(screen() == ('MIXER', '-') and not S.NanoFollow(0), 'invalid selection 501 -> no follow, MIXER / - %r' % (screen(),))
    state['sel'] = 20
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel); wait(0.2)
    check(not S.NanoErr, 'no screen errors reported')
    S.OnDeInit()
    check(screen() == ('', ''), 'script stops -> screen cleared %r' % (screen(),))


# D. no flicker (round 7): every state the screen goes through, over time, with FL's control smoothing modelled
if getattr(nano, 'NanoScreen', False) and hasattr(S, 'NanoFlush'):
    S.OnInit()
    target = {}

    def automate_smooth(eid, value, *a):
        calls.append(('mixer.automateEvent', (eid, value)))
        target[eid] = value / midi.FromMIDI_Max
        return 0

    mixer._over['automateEvent'] = automate_smooth
    mixer._over['getAutoSmoothEventValue'] = lambda eid: round(target.get(eid, state['vol'].get(eid, 0.5)) * 12800)
    timeline = []

    def sysex_rec(b):
        lcd_sysex(b)
        if bytes(b[:6]) == bytes([0xF0, 0, 0, 0x66, 0x14, 0x12]):
            timeline.append((clock.t, screen()))

    device._over['midiOutSysex'] = sysex_rec

    def tick(seconds):
        end = clock.t + seconds
        while clock.t < end - 1e-9:
            clock.t = min(end, clock.t + 0.02)
            for eid, tv in target.items():  # smoothing: the real value moves towards what the fader asked for
                cur = state['vol'].get(eid, tv)
                state['vol'][eid] = cur + (tv - cur) * 0.25
            S.OnIdle()

    max_writes = [0]

    def shown_states(fn, settle=2.0):
        """the screen as the eye sees it: the last state of every moment (both lines are written in the same OnIdle)"""
        timeline.clear()
        start = screen()
        t0 = clock.t
        fn()
        tick(settle)
        frames = {}
        for t, scr in timeline:
            frames.setdefault(round(t, 6), []).append(scr)
        max_writes[0] = max([max_writes[0]] + [len(v) for v in frames.values()])
        out = [(t0, start)]
        for t in sorted(frames):
            scr = frames[t][-1]
            if out[-1][1] != scr:
                out.append((t, scr))
        return [(t - t0, scr) for t, scr in out], clock.t - t0

    def durations(states, total):
        return [(round((states[i + 1][0] if i + 1 < len(states) else total) - t, 3), scr) for i, (t, scr) in enumerate(states)]

    def db(s):
        try:
            return float(s.replace('dB', ''))
        except ValueError:
            return None

    state['sel'] = 20
    state['vol'][vid20] = 0.8
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
    tick(2.5)  # 'FL / LISTO' gone

    def fader_down():
        for k in range(15):  # the hand pulls the fader down, one event every 30 ms
            v = 12000 - k * 250
            S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
            tick(0.03)

    st, total = shown_states(fader_down)
    tops = set(s[1][0] for s in st)
    vals = [db(s[1][1]) for s in st]
    check(tops == {'Ins 20'}, 'D fader (normal view): the top line never changes %r' % (tops,))
    check(None not in vals and all(b <= a for a, b in zip(vals, vals[1:])), 'D fader (normal view): the value only goes down, never back %r' % (vals,))
    check(len(st) - 1 <= 25, 'D fader (normal view): no more than one update per 40 ms (%d updates)' % (len(st) - 1))

    def metro():
        note(0x57, 127)
        tick(0.05)
        note(0x57, 0)

    st, total = shown_states(metro)
    d = durations(st, total)
    m = [x for x in d if x[1][0] == 'METRO']
    check(len(st) == 3 and len(m) == 1 and m[0][0] >= 1.4, 'D Metronome: one message, readable 1.5 s, then the normal view %r' % (d,))

    def metro_fl_hint():  # FL's own text for the same action arrives after the confirmation is up
        metro()
        tick(0.3)
        S.OnSendTempMsg('Metronome on', 500)

    st, total = shown_states(metro_fl_hint)
    check([s[1][0] for s in st][1:] == ['METRO', 'Ins 20'], "D Metronome + FL's own text afterwards: the confirmation stays %r" % ([s[1] for s in st],))

    def metro_then_mute():
        note(0x57, 127)
        note(0x57, 0)
        tick(0.4)
        note(0x10, 127)
        note(0x10, 0)

    st, total = shown_states(metro_then_mute)
    check([s[1][0] for s in st][1:] == ['METRO', 'MUTE', 'Ins 20'], 'D a new press replaces the message %r' % ([s[1] for s in st],))
    tap(0x10)  # unmute, metronome back
    tap(0x57)
    tick(2)

    def mixer_tap():
        note(0x3F, 127)
        tick(0.05)
        note(0x3F, 0)

    st, total = shown_states(mixer_tap)
    check([s[1] for s in st][1:] == [('MIXER', 'Ins 20')], 'D Mixer mode on: straight to MIXER / track, no ON flash %r' % ([s[1] for s in st],))

    def wheel3():
        for k in range(3):
            cc(0x3C, 1)
            tick(0.15)

    st, total = shown_states(wheel3)
    check([s[1] for s in st][1:] == [('MIXER', 'Ins 21'), ('MIXER', 'Ins 22'), ('MIXER', 'Ins 23')], 'D wheel in Mixer mode: only the track changes %r' % ([s[1] for s in st],))

    state['vol'][23 * 1000 + midi.REC_Mixer_Vol] = 0.8
    st, total = shown_states(fader_down)
    during = [s for s in st[1:] if s[1][0] != 'MIXER']
    tops = set(s[1][0] for s in during)
    vals = [db(s[1][1]) for s in during]
    check(tops == {'Ins 23'} and None not in vals and all(b <= a for a, b in zip(vals, vals[1:])), 'D fader in Mixer mode: the track on top, the value only goes down %r' % ([s[1] for s in st],))
    check(st[-1][1] == ('MIXER', 'Ins 23'), 'D fader in Mixer mode: back to MIXER / track afterwards %r' % (st[-1][1],))

    st, total = shown_states(mixer_tap)  # tap again: mode off
    d = durations(st, total)
    check(len(d) == 3 and d[1][1] == ('MIXER', 'OFF') and d[1][0] >= 1.1 and d[2][1][0] == 'Ins 23', 'D Mixer mode off: MIXER / OFF readable, then the normal view, nothing in between %r' % (d,))

    def undo_tap():
        note(0x3C, 127)
        tick(0.05)
        note(0x3C, 0)

    st, total = shown_states(undo_tap)
    tops = [s[1][0] for s in st][1:]
    check(len(tops) >= 2 and all(t == 'UNDO' for t in tops[:-1]) and tops[-1] == 'Ins 23', 'D Undo tap: UNDO stays up until the normal view, no flash %r' % ([s[1] for s in st],))

    def master_move():
        S.OnMidiMsg(Ev(0xE8, 0, 100))
        tick(0.06)
        S.OnMidiMsg(Ev(0xE8, 0, 90))

    st, total = shown_states(master_move)
    check(len(st) >= 3 and all(s[1][0] == 'MASTER' for s in st[1:-1]) and st[-1][1][0] == 'Ins 23', 'D master fader: MASTER stays on top while it moves %r' % ([s[1] for s in st],))

    def no_selection_blip():  # FL without a valid selected track for a moment
        state['sel'] = 501
        S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
        tick(0.2)
        state['sel'] = 23
        S.OnRefresh(midi.HW_Dirty_Mixer_Sel)

    st, total = shown_states(no_selection_blip, 0.5)
    check(all(s[1][0] != 'MIXER' for s in st), 'D a moment without a selected track: no MIXER / - flash %r' % ([s[1] for s in st],))

    check(S.NanoParse('Menu - View ~') == ('Menu', 'View'), "D FL's menu hint 'Menu - View ~' -> Menu / View %r" % (S.NanoParse('Menu - View ~'),))
    state['vol'][23 * 1000 + midi.REC_Mixer_Vol] = 0.8
    t1 = nano.NanoVolText(23)
    state['vol'][23 * 1000 + midi.REC_Mixer_Vol] = 0
    t2 = nano.NanoVolText(23)
    check(t1 == '-2.0dB' and t2 == '-INF dB', 'D volume text from FL dB: %r, silent -> %r' % (t1, t2))
    check(max_writes[0] <= 2, 'D never more than the two lines written in one moment (max %d writes)' % max_writes[0])
    check(not S.NanoErr, 'D no screen errors reported')
    S.OnDeInit()

# E. the external 8-square screen (round 8): one channel per square, the fader's square = the selected track
if getattr(nano, 'NanoScreen', False) and hasattr(S, 'NanoStripView'):
    specE = importlib.util.spec_from_file_location('nanoE', sys.argv[1])
    nanoE = importlib.util.module_from_spec(specE)
    specE.loader.exec_module(nanoE)
    nanoE.time = clock
    S = nanoE.MackieCU  # the helpers (note, cc, tap, screen, wait) use this fresh instance from here on
    mixer._over['automateEvent'] = automateEvent
    mixer._over['getAutoSmoothEventValue'] = lambda eid: round(state['vol'].get(eid, 0.5) * 12800)
    device._over['midiOutSysex'] = lcd_sysex
    state['sel'] = 20
    state['vol'][vid20] = 0.8
    S.OnInit()
    S.OnRefresh(0xFFFF)
    wait(2.5)
    sq = squares()
    check(S.NanoStrip == -1 and all(s == sq[0] for s in sq) and sq[0] == ('Ins 20', '-2.0dB'), 'E before the fader is touched: every square shows the fader view %r' % (sq[0],))
    note(0x6E, 127)
    note(0x6E, 0)
    wait(0.2)
    sq = squares()
    check(S.NanoStrip == 6 and sq[6] == ('Ins 20', '-2.0dB'), 'E fader touched on strip 7: its square shows the selected track %r' % (sq[6],))
    check(all(sq[k] == ('Ins %d' % (k + 1), 'C') for k in range(8) if k != 6), 'E the other squares: their bank channel and its pan %r' % (sq,))
    tap(0x57)
    wait(0.2)
    sq = squares()
    check(all(s == ('METRO', 'ON') for s in sq), 'E Metronome: the message covers all 8 squares %r' % (sq,))
    wait(1.6)
    sq = squares()
    check(sq[0] == ('Ins 1', 'C') and sq[6] == ('Ins 20', '-2.0dB'), 'E after the message: one channel per square again %r' % ([sq[0], sq[6]],))
    tap(0x57)
    wait(1.8)
    tap(0x3F)
    wait(0.1)
    sq = squares()
    check(sq[6] == ('MIXER', 'Ins 20') and sq[0] == ('Ins 1', 'C'), 'E Mixer mode: only the fader square shows MIXER / track %r' % ([sq[0], sq[6]],))
    tap(0x3F)
    wait(1.5)
    cc(0x10, 3)
    wait(0.1)
    sq = squares()
    check(sq[0][0] == 'Ins 1' and sq[0][1].endswith('%R') and sq[6] == ('Ins 20', '-2.0dB') and sq[3] == ('Ins 4', 'C'), 'E knob 1 turned: square 1 shows its new pan live, no full-screen message %r' % (sq,))
    cc(0x16, 3)
    wait(0.1)
    sq = squares()
    check(sq[6][0] == 'Ins 7' and sq[6][1].endswith('%R'), 'E knob of the fader strip: its channel and value in the fader square for a moment %r' % (sq[6],))
    wait(1.2)
    check(squares()[6] == ('Ins 20', '-2.0dB'), 'E then the fader square shows the selected track again %r' % (squares()[6],))
    note(0x19, 127)
    note(0x19, 0)
    wait(0.2)
    sq = squares()
    check(S.NanoStrip == 1 and sq[1][0] == 'Ins 2' and sq[1][1].endswith('dB') and sq[6][0] == 'Ins 7' and sq[6][1].endswith('%R'), 'E fader moved to strip 2 (|< >|): square 2 = selected track, square 7 = its own channel %r' % ([sq[1], sq[6]],))
    S.OnMidiMsg(Ev(0xE8, 0, 100))
    wait(0.1)
    sq = squares()
    check(sq[1][0] == 'MASTER' and sq[0] == ('Ins 1', sq[0][1]) and sq[2][0] == 'Ins 3', 'E master fader: MASTER only in the fader square %r' % (sq[:3],))
    wait(1.2)
    tap(0x2A)
    wait(0.1)
    check(all(s == ('SENDS', 'PAGINA') for s in squares()), 'E Sends page button: PAGINA on all squares %r' % (squares()[0],))
    wait(1.5)
    sq = squares()
    check(sq[0] == ('Ins 1', '-') and sq[1][0] == 'Ins 2', 'E Sends page: each square shows its channel and its send (- = no send) %r' % (sq[:2],))
    tap(0x28)
    wait(1.5)
    check(not S.NanoErr, 'E no screen errors reported')
    S.OnDeInit()
    check(all(s == ('', '') for s in squares()), 'E script stops -> every square cleared')

# F. round 9: resting finger, take-over after a track change, Shift F-keys, Shift+Solo, quick Undo, Marker/Free, menus, clock
if getattr(nano, 'NanoScreen', False) and hasattr(nano, 'NanoFaderDeadband'):
    specF = importlib.util.spec_from_file_location('nanoF', sys.argv[1])
    nanoF = importlib.util.module_from_spec(specF)
    specF.loader.exec_module(nanoF)
    nanoF.time = clock
    S = nanoF.MackieCU
    mixer._over['automateEvent'] = automateEvent
    mixer._over['getAutoSmoothEventValue'] = lambda eid: round(state['vol'].get(eid, 0.5) * 12800)
    device._over['midiOutSysex'] = lcd_sysex
    state['sel'] = 20
    state['vol'][vid20] = 0.8
    S.OnInit()
    check(screen() == ('FL', 'LISTO'), 'F OnInit draws at once (FL / LISTO before any OnIdle) %r' % (screen(),))
    S.OnRefresh(0xFFFF)
    wait(2.5)
    note(0x68, 127)  # finger on the fader (strip 1)
    calls.clear()
    for v in (8800, 8830, 8790, 8815, 8805, 8820):  # a resting finger: within +-48 of the first position
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.06)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(len(autos) == 1, 'F resting finger: the first position is taken, the jitter is ignored (%d automations)' % len(autos))
    calls.clear()
    for v in (8784, 8848, 8752, 8816, 8768, 8832, 8752, 8800, 8848, 8760):  # the real log's resting spread (96 wide)
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.06)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(len(autos) <= 1, "F the real log's resting jitter (96 wide) is ignored too (%d automations)" % len(autos))
    calls.clear()
    for v in range(8800, 8000, -40):  # a slow real move down, 40 units per event
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.03)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(len(autos) >= 8, 'F a slow real move still moves the volume (%d automations for 20 events)' % len(autos))
    tap(0x10)
    for v in (8810, 8795, 8825):
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.1)
    wait(0.2)
    check(screen()[0] == 'MUTE', 'F a confirmation stays while the finger rests on the fader %r' % (screen(),))
    tap(0x10)
    wait(1.8)
    vid25 = 25 * 1000 + midi.REC_Mixer_Vol
    state['vol'][vid25] = 0.3
    state['sel'] = 25  # the selected track changes (wheel, mouse, |< >|) while the finger rests
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
    wait(0.1)
    calls.clear()
    for v in (8790, 8830, 8800, 8700, 8900):
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.06)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(not autos and abs(state['vol'][vid25] - 0.3) < 1e-9, 'F track changed under a resting finger: the new track keeps its volume (%d automations)' % len(autos))
    tgt = S.AlphaTrack_LevelToSlider(getEventValue(vid25))
    S.OnMidiMsg(Ev(0xE0, (tgt + 60) & 0x7F, (tgt + 60) >> 7))
    wait(0.06)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(len(autos) == 1, 'F the fader reaches the new level: it takes over (%d automations)' % len(autos))
    vid26 = 26 * 1000 + midi.REC_Mixer_Vol
    state['vol'][vid26] = 0.25
    state['sel'] = 26  # the selection changes and FL is late with OnRefresh: the finger keeps resting
    calls.clear()
    for v in (tgt + 60, tgt + 120, tgt, tgt + 90):
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        wait(0.06)
    autos = [a for n, a in calls if n == 'mixer.automateEvent']
    check(not autos and abs(state['vol'][vid26] - 0.25) < 1e-9, 'F selection changed before FL refreshed: the new track keeps its volume (%d automations)' % len(autos))
    S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
    note(0x68, 0)
    calls.clear()
    note(0x54, 127)  # Shift + yellow 7, Shift released first
    note(0x3C, 127)
    note(0x54, 0)
    note(0x3C, 0)
    wait(0.3)
    gts = [a for n, a in calls if n == 'transport.globalTransport']
    check(not any(a[0] == midi.FPT_UndoUp for a in gts) and [a[1] for a in gts if a[0] == midi.FPT_F1 + 6] == [2, 0], 'F Shift + yellow 7, Shift released first: F7 down and up, no Undo %r' % (gts,))
    calls.clear()
    note(0x54, 127)
    tap(0x08)
    note(0x54, 0)
    wait(0.3)
    check(any(n == 'mixer.soloTrack' for n, a in calls) and not S.NanoErr, 'F Shift + Solo: solos (no NameError)')
    wait(1.5)
    note(0x3C, 127)
    wait(0.15)
    check(screen()[0] != 'UNDO', 'F quick Undo press: no UNDO view in the first 0.3 s %r' % (screen(),))
    note(0x3C, 0)
    wait(0.3)
    check(screen()[0] == 'UNDO', 'F quick Undo tap: then UNDO and its level %r' % (screen(),))
    wait(1.8)
    note(0x3C, 127)
    wait(0.5)
    check(screen()[0] == 'UNDO', 'F holding Undo: the UNDO view comes up after 0.3 s %r' % (screen(),))
    note(0x3C, 0)
    wait(1.8)
    tap(0x48)  # Marker mode: every wheel click shows FL's text in the mode view, no alternating
    wait(1.5)
    cc(0x3C, 1)
    wait(0.1)
    a1 = screen()
    wait(1.4)
    a2 = screen()
    check(a1 == a2 == ('MARKER', 'hint'), 'F Marker mode: the last jump stays in the view %r %r' % (a1, a2))
    tap(0x48)
    wait(1.5)
    tap(0x42)  # Free 1: wheel clicks show no message
    wait(1.5)
    cc(0x3C, 1)
    wait(0.1)
    check(screen() == ('FREE 1', 'ON'), 'F Free mode wheel click: the view stays FREE 1 / ON %r' % (screen(),))
    tap(0x42)
    wait(1.5)
    base = screen()
    S.OnSendTempMsg('', 500)
    wait(0.1)
    check(screen() == base, 'F an empty FL text does not blank the screen %r' % (screen(),))
    ui._over['isInPopupMenu'] = lambda: 1
    S.OnSendTempMsg('Menu - View ~', 1000)
    wait(2.0)
    check(screen() == ('Menu', 'View'), "F FL's menu hint stays while the menu is open %r" % (screen(),))
    ui._over['isInPopupMenu'] = lambda: 0
    wait(0.6)
    check(screen() == base, 'F the menu closed: back to the normal view %r' % (screen(),))
    clock.t -= 30  # the PC clock goes back
    tap(0x57)
    wait(0.3)
    check(screen()[0] == 'METRO', 'F the clock went back: the screen still draws %r' % (screen(),))
    clock.t += 30
    wait(1.0)
    calls.clear()
    ui._over['getHintValue'] = lambda v, m: (calls.append(('ui.getHintValue', (v, m))), '%d%%' % round(v * 100 / m))[1]
    tap(0x2D)  # Free page: fader text on the 0..65536 scale
    S.OnMidiMsg(Ev(0xE0, 0, 64))
    wait(0.1)
    check(any(n == 'ui.getHintValue' and a[1] == 65536 for n, a in calls) and screen()[1] == '50%', 'F Free page fader text uses the 0..65536 scale %r' % (screen(),))
    tap(0x28)
    wait(1.5)
    check(not S.NanoErr, 'F no screen errors reported')
    S.OnDeInit()

for _ in range(3):
    S.OnIdle()
print('\n%s' % ('ALL PASS' if fails == 0 else '%d FAILED' % fails))
sys.exit(1 if fails else 0)
