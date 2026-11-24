"""Run the real Nano Air script in the FL simulator and record, for every control, what both screens show over time.
Output: JSON for the tutorial (what the script itself would draw: the 'theory' to compare with the real screens).
Usage: python -I gen_screen_data.py <flsim.py> <script.py> <out.json>
"""
import sys, json, importlib.util

sim_path, script_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(sim_path, encoding='utf-8').read()
cut = src.index("spec = importlib.util.spec_from_file_location('nano', sys.argv[1])")
ns = {'__name__': 'flsim_stubs'}
exec(compile(src[:cut], sim_path, 'exec'), ns)  # FL module stubs only
midi, state, mixer, device, ui, general, channels, patterns, playlist, transport = (
    ns[k] for k in ('midi', 'state', 'mixer', 'device', 'ui', 'general', 'channels', 'patterns', 'playlist', 'transport'))
Ev, LCD, DIG, toggles, lcd_sysex, out_msg = ns['Ev'], ns['LCD'], ns['DIG'], ns['toggles'], ns['lcd_sysex'], ns['out_msg']

# --- an example project (generic example names; track 17 is the selected track, outside the bank shown)
NAMES = {0: 'Master', 1: 'Kick', 2: 'Snare', 3: 'HiHat', 4: 'Bass', 5: 'Piano', 6: 'Guitar', 7: 'Synth', 8: 'Pad',
         17: 'Vocal', 18: 'Insert 18', 19: 'Insert 19'}
CHANNELS = ['Kick Drum', 'Snare', 'Hat', '808 Bass']
WINDOWS = ['Mixer', 'Playlist', 'Channel rack', 'Piano roll']
world = {}


def reset_world():
    state['vol'].clear()
    for t in range(0, 30):
        state['vol'][t * 1000 + midi.REC_Mixer_Vol] = 0.7
    state['vol'][17 * 1000 + midi.REC_Mixer_Vol] = 0.48  # -5.2dB in the simulator's dB curve
    state['vol'][2 * 1000 + midi.REC_Mixer_Pan] = 0.45     # Snare 10% left
    state['vol'][3 * 1000 + midi.REC_Mixer_Pan] = 0.625    # HiHat 25% right
    state['vol'][midi.REC_MainVol] = 0.8
    state['sel'] = 17
    state['tempo'] = 130.0
    state['mute'].clear(); state['solo'].clear(); state['arm'].clear()
    toggles.update({'metro': 0, 'looprec': 0, 'precount': 0, 'snap': 3, 'loopmode': 0})
    world.update({'chan': 0, 'pat': 1, 'win': 0, 'undo': 3, 'bar': 1, 'timemin': 0})


def base_track_select(index, step):
    if index == 0:
        world['chan'] = (world['chan'] + step) % len(CHANNELS)
    elif index == 1:
        state['sel'] = max(0, min(125, state['sel'] + step))
    elif index == 2:
        world['pat'] = max(1, world['pat'] + step)


def global_transport(cmd, val, *a):
    ns['global_transport'](cmd, val, *a)
    if val:
        if cmd == midi.FPT_WindowJog:
            world['win'] = (world['win'] + (1 if val > 0 else -1)) % len(WINDOWS)
        elif cmd in (midi.FPT_UndoUp, midi.FPT_UndoJog):
            world['undo'] = max(0, world['undo'] - 1) if (cmd == midi.FPT_UndoUp or val > 0) else world['undo'] + 1
        elif cmd in (midi.FPT_Jog, midi.FPT_Jog + 1):
            world['bar'] = max(1, world['bar'] + val)
    return midi.GT_Global


def process_rec(eid, value, flags):
    if eid == midi.REC_Tempo:
        state['tempo'] += 1
    return 0


def set_time_disp(*a):
    world['timemin'] ^= 1


mixer._over['getTrackName'] = lambda t, *a: NAMES.get(t, 'Insert %d' % t)
mixer._over['trackCount'] = lambda: 127  # like FL: Master + 125 inserts + Current, so <<8 wraps the way a real Nano does
mixer._over['soloTrack'] = lambda t, *a: state['solo'].symmetric_difference_update({t})
device._over['baseTrackSelect'] = base_track_select
device._over['midiOutSysex'] = lcd_sysex
transport._over['globalTransport'] = global_transport
general._over['processRECEvent'] = process_rec
general._over['getUndoLevelHint'] = lambda: '%d/10' % world['undo']
channels._over['getChannelName'] = lambda i: CHANNELS[i % len(CHANNELS)]
channels._over['channelNumber'] = lambda: world['chan']
patterns._over['patternNumber'] = lambda: world['pat']
ui._over['getFocusedFormCaption'] = lambda: WINDOWS[world['win']] + ' - x'
ui._over['getTimeDispMin'] = lambda: world['timemin']
ui._over['setTimeDispMin'] = set_time_disp
ui._over['getHintMsg'] = lambda: '(texto de FL)'
playlist._over['getVisTimeBar'] = lambda: world['bar']


class Clock:
    def __init__(self):
        self.t = 1000.0

    def time(self):
        return self.t

    def ctime(self, *a):
        return 'now'


clock = Clock()
S = None
FADER_STRIP = 6  # example: the Nano's fader sits on strip 7 of the bank (MIDI channel index 6)


def digits():
    out = ''
    for v in DIG:
        c = v & 0x3F
        out += chr(c + 0x40 if c < 0x20 else c) if c else ' '
        if v & 0x40:
            out += '.'
    return out


def frame():
    return [''.join(LCD[56:112]), ''.join(LCD[0:56]), digits(), max(0, S.NanoStrip) if S else FADER_STRIP]


def fresh():
    global S
    for i in range(112):
        LCD[i] = ' '
    for i in range(10):
        DIG[i] = 0
    reset_world()
    spec = importlib.util.spec_from_file_location('nano_gen', script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.time = clock
    S = mod.MackieCU
    S.OnInit()
    S.OnRefresh(0xFFFF)
    note(0x68 + FADER_STRIP, 127)  # touch the fader once: the script learns its strip
    note(0x68 + FADER_STRIP, 0)
    tick(2.6)


REC = []  # every frame that changed while a step runs (also during the step's own waits)


def tick(seconds):
    end = clock.t + seconds
    while clock.t < end - 1e-9:
        clock.t = round(min(end, clock.t + 0.02), 6)
        S.OnIdle()
        f = frame()
        if not REC or REC[-1][1] != f:
            REC.append((clock.t, f))


def note(n, v):
    S.OnMidiMsg(Ev(0x90, n, v))


def cc(n, v):
    S.OnMidiMsg(Ev(0xB0, n, v))


def tap(n):
    note(n, 127)
    note(n, 0)


def shift_tap(n):
    note(0x54, 127)
    tap(n)
    note(0x54, 0)


def fader_moves(ch=0, start=9000, stop=7000, n=10):
    def act():
        for k in range(n):
            v = round(start + (stop - start) * k / (n - 1))
            S.OnMidiMsg(Ev(0xE0 + ch, v & 0x7F, v >> 7))
            tick(0.05)
    return act


def run(steps, settle=2.2):
    """steps: list of (label, action, seconds to watch). Returns the start frame and, per step, the frames that changed"""
    fresh()
    start = frame()
    out = []
    for label, act, watch in steps:
        t0 = clock.t
        last = frame()
        REC.clear()
        REC.append((t0, last))
        act()
        tick(watch or settle)
        frames = []
        prev = last
        for t, f in REC[1:]:
            if f != prev:
                frames.append([round(t - t0, 2), f[0], f[1], f[2], f[3]])
                prev = f
        out.append({'a': label, 'f': frames})
    return {'start': start, 'steps': out}


def mode_steps(n, wheel_label='Giras la rueda un clic'):
    return [('Un toque', lambda: tap(n), 1.6),
            (wheel_label, lambda: cc(0x3C, 1), 0.8),
            ('Otro clic de rueda', lambda: cc(0x3C, 1), 0.8),
            ('Otro toque: se apaga', lambda: tap(n), 2.2)]


TAP = lambda n: [('Un toque', lambda: tap(n), 2.2)]
TAP2 = lambda n: [('Un toque', lambda: tap(n), 2.2), ('Otro toque', lambda: tap(n), 2.2)]

S_ = {}
# colored keys (by MIDI note, the same on every layer that sends it)
S_['n32'] = run(TAP2(0x32))                       # Flip
S_['n3e'] = run(mode_steps(0x3E))                 # Pattern
S_['n34'] = run(TAP(0x34))                        # Display mode
S_['n50'] = run([('Un toque', lambda: tap(0x50), 2.2), ('Shift + Save', lambda: shift_tap(0x50), 2.2)])
S_['n36'] = run(TAP(0x36))
S_['n4a'] = run(TAP(0x4A))
S_['n3f'] = run(mode_steps(0x3F))                 # Mixer
S_['n54'] = run([('Mantener apretado', lambda: note(0x54, 127), 1.0), ('Soltar', lambda: note(0x54, 0), 1.0)])
S_['n51'] = run(TAP(0x51))
S_['n37'] = run(TAP(0x37))
S_['n4b'] = run(TAP(0x4B))
S_['n40'] = run(mode_steps(0x40))                 # Channel
S_['n55'] = run(TAP(0x55))
S_['n52'] = run(TAP(0x52))
S_['n38'] = run(TAP(0x38))
S_['n4c'] = run(mode_steps(0x4C))                 # Window
S_['n41'] = run(mode_steps(0x41))                 # Tempo
S_['n57'] = run([('Un toque', lambda: tap(0x57), 2.2), ('Otro toque', lambda: tap(0x57), 2.2), ('Shift + Metronome', lambda: shift_tap(0x57), 2.2)])
S_['n53'] = run(TAP(0x53))
S_['n39'] = run(TAP(0x39))
S_['n33'] = run(TAP2(0x33))                       # Smooth
for k, n in enumerate([0x42, 0x43, 0x44, 0x45]):
    S_['n%x' % n] = run(mode_steps(n))            # Free 1-4
S_['n35'] = run(TAP2(0x35))                       # Time format
S_['n46'] = run(mode_steps(0x46))                 # Move
S_['n3a'] = run(TAP(0x3A))
S_['n4d'] = run(TAP(0x4D))
S_['n58'] = run(TAP2(0x58))                       # 3..2..1
S_['n47'] = run(TAP(0x47))
S_['n3b'] = run(TAP(0x3B))
S_['n4e'] = run(TAP(0x4E))
S_['n59'] = run(TAP(0x59))
S_['n48'] = run(mode_steps(0x48))                 # Mark
S_['n3c'] = run([('Un toque', lambda: tap(0x3C), 2.2),
                 ('Mantener y girar la rueda', lambda: (note(0x3C, 127), tick(0.3), cc(0x3C, 0x41), tick(0.5), cc(0x3C, 0x41)), 1.0),
                 ('Soltar', lambda: note(0x3C, 0), 2.0)])
S_['n4f'] = run(TAP(0x4F))
S_['n5a'] = run(TAP2(0x5A))                       # Pattern / Song
S_['n49'] = run(TAP(0x49))
S_['n3d'] = run(TAP(0x3D))
# fixed controls
for k in range(1, 5):
    S_['knob%d' % k] = run([('Giras a la derecha', lambda k=k: (cc(0x10 + k - 1, 2), tick(0.1), cc(0x10 + k - 1, 2)), 1.5),
                            ('Apretar la perilla (centro)', lambda k=k: (note(0x20 + k - 1, 127), note(0x20 + k - 1, 0)), 1.5)])
S_['knobM'] = S_['knob1']
S_['fader'] = run([('Bajas el fader', fader_moves(FADER_STRIP), 1.5),
                   ('Con Mixer prendido lo mueves', lambda: (tap(0x3F), tick(0.6), fader_moves(FADER_STRIP, 7000, 8000, 6)()), 1.8),
                   ('Apagas Mixer', lambda: tap(0x3F), 2.0)])
S_['master'] = run([('Con Master prendido mueves el fader', fader_moves(8, 12000, 10000, 8), 1.8)])
S_['mute'] = run(TAP2(0x10 + FADER_STRIP))
S_['solo'] = run(TAP2(0x08 + FADER_STRIP))
S_['rec'] = run(TAP2(0x00 + FADER_STRIP))
for cid, n in (('rew', 0x5B), ('ff', 0x5C), ('stop', 0x5D), ('play', 0x5E), ('recT', 0x5F)):
    S_[cid] = run(TAP(n))
S_['loop'] = run([('Un toque', lambda: tap(0x56), 2.2), ('Otro toque', lambda: tap(0x56), 2.2), ('Shift + Loop', lambda: shift_tap(0x56), 2.2)])
S_['jog'] = run([('Giras la rueda (sin modo)', lambda: (cc(0x3C, 1), tick(0.2), cc(0x3C, 1), tick(0.2), cc(0x3C, 1)), 1.2),
                 ('Aprietas la rueda', lambda: tap(0x65), 2.2), ('Otra vez', lambda: tap(0x65), 2.2)])
# with Zoom on, the script turns the wheel into arrow keys; the simulator taps the arrow note the wheel stands for
S_['zoomV'] = run([('Un toque', lambda: tap(0x64), 1.2), ('Giras la rueda (manda flecha arriba)', lambda: tap(0x60), 0.8), ('Otro toque', lambda: tap(0x64), 2.2)])
S_['zoomH'] = run([('Un toque', lambda: tap(0x64), 1.2), ('Giras la rueda (manda flecha derecha)', lambda: tap(0x63), 0.8), ('Otro toque', lambda: tap(0x64), 2.2)])
for k in range(6):
    S_['pg%d' % k] = run([('Un toque', lambda k=k: tap(0x28 + k), 2.2)])
S_['fprev'] = run([('Un toque', lambda: tap(0x18 + FADER_STRIP - 1), 2.0)])
S_['fnext'] = run([('Un toque', lambda: tap(0x18 + FADER_STRIP + 1), 2.0)])
S_['bprev'] = run([('Un toque', lambda: tap(0x2E), 2.0)])
S_['bnext'] = run([('Un toque', lambda: tap(0x2F), 2.0)])

json.dump({'strip': FADER_STRIP, 'scenes': S_}, open(out_path, 'w', encoding='utf-8'), ensure_ascii=True, separators=(',', ':'))
print('ok', len(S_), 'scenes,', len(open(out_path).read()), 'bytes')
# a readable summary of the first change of every scene
for k, v in S_.items():
    st = v['steps'][0]['f']
    first = st[0] if st else None
    if first:
        top, bot, fs = first[1], first[2], first[4]
        mini = (top[7 * fs:7 * fs + 7].rstrip(), bot[7 * fs:7 * fs + 7].rstrip())
        same = all(top[i * 7:i * 7 + 7] == top[0:7] and bot[i * 7:i * 7 + 7] == bot[0:7] for i in range(8))
        print('%-7s %-28s mini=%-22r %s' % (k, v['steps'][0]['a'], mini, 'all 8' if same else 'squares'))
    else:
        print('%-7s %-28s (no change)' % (k, v['steps'][0]['a']))
