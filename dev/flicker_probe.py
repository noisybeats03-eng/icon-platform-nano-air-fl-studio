"""Record every change of the Nano's small screen (top/bottom line) over time, to see flicker.

Usage: python -I flicker_probe.py <flsim.py> <script.py>
Runs flsim's setup (stubs, sections A/B), then scenarios that print the screen timeline.
FL's control smoothing is modelled: getEventValue lags behind the value the fader asked for.
"""
import sys

sim_path, script_path = sys.argv[1], sys.argv[2]
src = open(sim_path, encoding='utf-8').read()
cut = src.index("if getattr(nano, 'NanoScreen', False):")
sys.argv = [sim_path, script_path]
ns = {'__name__': 'flsim_setup'}
exec(compile(src[:cut], sim_path, 'exec'), ns)

S, midi, state, clock, Ev, mixer, device = ns['S'], ns['midi'], ns['state'], ns['clock'], ns['Ev'], ns['mixer'], ns['device']
screen, note, cc = ns['screen'], ns['note'], ns['cc']

# --- smoothing model: automateEvent sets a target, the real value moves towards it on every idle tick
target = {}


def automate(eid, value, *a):
    target[eid] = value / midi.FromMIDI_Max
    if not (len(a) >= 2 and a[1]):  # no smoothing speed -> jump
        state['vol'][eid] = target[eid]
    return 0


def smooth_value(eid):
    return round(target.get(eid, state['vol'].get(eid, 0.5)) * midi.FromMIDI_Max)


mixer._over['automateEvent'] = automate
mixer._over['getAutoSmoothEventValue'] = smooth_value

timeline = []
orig_sysex = device._over['midiOutSysex']


def sysex(b):
    orig_sysex(b)
    if bytes(b[:6]) == bytes([0xF0, 0, 0, 0x66, 0x14, 0x12]):
        timeline.append((clock.t, screen()))


device._over['midiOutSysex'] = sysex


def tick(seconds):
    end = clock.t + seconds
    while clock.t < end - 1e-9:
        clock.t = min(end, clock.t + 0.02)
        for eid, tv in target.items():
            cur = state['vol'].get(eid, tv)
            state['vol'][eid] = cur + (tv - cur) * 0.25
        S.OnIdle()


def run(title, fn, settle=2.0):
    timeline.clear()
    t0 = clock.t
    fn()
    tick(settle)
    print('\n=== ' + title)
    shown = []
    for t, scr in timeline:
        if not shown or shown[-1][1] != scr:
            shown.append((t, scr))
    for i, (t, scr) in enumerate(shown):
        dur = (shown[i + 1][0] if i + 1 < len(shown) else clock.t) - t
        print('  +%6.3fs  %-9r %-9r  visible %.3fs' % (t - t0, scr[0], scr[1], dur))
    short = [s for i, s in enumerate(shown[:-1]) if shown[i + 1][0] - s[0] < 0.3]
    print('  -> %d screen changes, %d of them visible < 0.3 s' % (len(shown), len(short)))
    return shown


vid = 20 * 1000 + midi.REC_Mixer_Vol
state['vol'][vid] = 0.8
state['sel'] = 20
S.OnRefresh(midi.HW_Dirty_Mixer_Sel)
tick(3)


def fader_move():
    for k in range(15):  # the hand pulls the fader down, one event every 30 ms
        v = 12000 - k * 250
        S.OnMidiMsg(Ev(0xE0, v & 0x7F, v >> 7))
        tick(0.03)


run('fader moved by hand (normal view)', fader_move)


def metro():
    note(0x57, 127)
    tick(0.05)
    note(0x57, 0)


run('Metronome tapped (50 ms press)', metro)


def mixer_mode_on():
    note(0x3F, 127)
    tick(0.05)
    note(0x3F, 0)


run('Mixer mode on', mixer_mode_on)


def wheel():
    for k in range(3):
        cc(0x3C, 1)
        tick(0.15)


run('wheel turned 3 clicks in Mixer mode', wheel)
run('fader moved in Mixer mode', fader_move)
run('Mixer mode off', mixer_mode_on)


def undo():
    note(0x3C, 127)
    tick(0.05)
    note(0x3C, 0)


run('yellow Undo tapped', undo)


def mute():
    note(0x10, 127)
    tick(0.05)
    note(0x10, 0)


run('Mute tapped', mute)
