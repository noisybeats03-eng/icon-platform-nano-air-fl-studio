# name=iCON Platform Nano Air (custom)
# url=
# iCON Platform Nano Air script for FL Studio, release 1.0.1. Unofficial: not affiliated with Image-Line or iCON Pro Audio.
# Manual, tutorial and updates: https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio
# Based on the FL Studio stock "Mackie Control Universal" script (device_MackieCU.py, version 2026.1), (c) Image-Line Software.
# Image-Line's parts are not covered by this project's MIT license. This project's changes: Copyright (c) 2026 noisybeats03-eng,
# MIT License; full texts in LICENSE and NOTICE.md at the link above.
# Changes for the iCON Platform Nano Air:
#  - ZOOM latches: tap once and the wheel/arrows zoom, tap again to go back to normal (ZOOM LED shows the state).
#  - In zoom mode: up/down = vertical zoom (track height), left/right = horizontal zoom, jog wheel = horizontal zoom.
#  - Wheel-mode buttons (Pattern, Mixer, Channel, Tempo, Free1-4, Mark, Move, Window) latch like ZOOM (NanoLatchJogSources).
#  - Yellow 7 "Undo" (F7): tap = undo one step, hold + wheel = undo history.
#  - Transport LOOP: loop recording on/off; Shift + LOOP = snap on/off.
#  - Motor fader: optional overshoot push for small moves (NanoFaderKick, off by default).
#  - The single fader, Mute/Solo/Rec and the display follow FL's selected mixer track (NanoFollowSelected).
#  - Wheel-mode buttons: tap = stays on; hold while turning the wheel = off again on release.
#  - Small screen (NanoScreen): selected track + volume, short whole messages, the wheel mode and its item, BPM on the digits.
#    Drawn only from OnIdle (no flicker while the fader moves), real dB values, messages stay 1.5 s.
#    External 8-square screen (NanoStrips): one channel per square, the fader's square = the selected track.
#  - Fader: a resting finger's jitter is ignored; a newly selected track is taken over only when the fader reaches it.
#  - Stock-script bugs fixed: Shift + Solo NameError, Shift + F1-F8 release, ui.GetHintMsg typo, Free page fader value text.
# version 2026.1

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import channels

import midi
import utils
import time

MackieCU_KnobOffOnT = [(midi.MIDI_CONTROLCHANGE + (1 << 6)) << 16, midi.MIDI_CONTROLCHANGE + ((0xB + (2 << 4) + (1 << 6)) << 16)];
MackieCU_nFreeTracks = 64

#const
MackieCUNote_Undo = 0x3C
MackieCUNote_Pat = 0x3E
MackieCUNote_Mix = 0x3F
MackieCUNote_Chan = 0x40
MackieCUNote_Tempo = 0x41
MackieCUNote_Free1 = 0x42
MackieCUNote_Free2 = 0x43
MackieCUNote_Free3 = 0x44
MackieCUNote_Free4 = 0x45
MackieCUNote_Marker = 0x48
MackieCUNote_Zoom = 0x64
MackieCUNote_Move = 0x46
MackieCUNote_Window = 0x4C
# Nano Air: tap a wheel-mode button to switch the wheel to that mode, tap it again to switch back (False = FL's hold-to-use)
NanoLatchJogSources = True
# Nano Air: the motor fader ignores very small moves. When FL moves a fader by less than NanoFaderMinMove
# (14-bit units, 16383 = whole travel) and the value then stays still for NanoFaderSettle seconds, the script
# pushes the fader NanoFaderOvershoot past the target and NanoFaderReturn seconds later sends the exact position.
NanoFaderKick = False
NanoDebug = False # Nano Air: diagnostics in VIEW > Script output
# Nano Air: the single fader (with Mute/Solo/Rec and the name on the display) follows the mixer track selected in FL
NanoFollowSelected = True
# Nano Air: drive the small screen (2 lines of 7 characters; its top line shows MCU row 2, its bottom line MCU row 1)
NanoScreen = True
NanoScreenGap = 0.04 # Nano Air: shortest time between two screen updates (seconds)
# Nano Air: the external screen (8 squares) shows one bank channel per square; False = every square repeats the Nano's own screen
NanoStrips = True
# Nano Air: fader pitch-bend closer than this to the last one taken (14-bit units) is a resting finger, not a move
NanoFaderDeadband = 48
# Nano Air: after the selected track changes under a touched fader, it acts again once it is this close to the new level
NanoFaderPickup = 150
NanoFaderMinMove = 400
NanoFaderOvershoot = 450
NanoFaderTolerance = 48
NanoFaderSettle = 0.12
NanoFaderReturn = 0.15
NanoLatchNames = {0x3E: 'Pattern', 0x3F: 'Mixer track', 0x40: 'Channel', 0x41: 'Tempo', 0x42: 'Free 1', 0x43: 'Free 2', 0x44: 'Free 3', 0x45: 'Free 4', 0x48: 'Marker', 0x46: 'Move', 0x4C: 'Window'}
# Mackie CU pages
MackieCUPage_Pan = 0
MackieCUPage_Stereo = 1
MackieCUPage_Sends = 2
MackieCUPage_FX = 3
MackieCUPage_EQ = 4
MackieCUPage_Free = 5

ExtenderLeft = 0
ExtenderRight = 1

OffOnStr = ('off', 'on')

# Nano Air screen: wheel modes and what the top line calls them
NanoModeNames = {0x3E: 'PATTERN', 0x3F: 'MIXER', 0x40: 'CHANNEL', 0x41: 'TEMPO', 0x42: 'FREE 1', 0x43: 'FREE 2', 0x44: 'FREE 3', 0x45: 'FREE 4', 0x48: 'MARKER', 0x46: 'MOVE', 0x4C: 'WINDOW', 0x64: 'ZOOM', 0x3C: 'UNDO'}
NanoLiveModes = [0x3E, 0x3F, 0x40, 0x41, 0x4C, 0x3C] # modes whose bottom line shows the current item, always up to date
# Nano Air screen: how FL's messages start -> (top line, bottom line); None = the bottom line comes from the message
NanoMsgMap = [('mixer track', 'MIXER', None), ('channel', 'CHANNEL', None), ('pattern', 'PATTERN', None), ('tempo', 'TEMPO', None),
	('marker jump', 'MARKER', 'JUMP'), ('marker selection', 'MARKER', 'SELECT'), ('marker', 'MARKER', None), ('current window', 'WINDOW', None), ('window', 'WINDOW', None),
	('move', 'MOVE', None), ('zoom', 'ZOOM', None), ('undo history', 'UNDO', None),
	('free jog', 'FREE', None), ('free knob', 'FREE', None), ('free slider', 'FREE', None), ('free button', 'FREE', None), ('free 1', 'FREE 1', None), ('free 2', 'FREE 2', None), ('free 3', 'FREE 3', None), ('free 4', 'FREE 4', None),
	('control smoothing', 'SMOOTH', None), ('self.clicking', 'CLICK', None), ('audio editor ready', 'EDISON', 'LISTO'), ('linked to', 'FL', 'LISTO'), ('cannot send', 'NO SEND', ''), ('extender on', 'EXTENDR', None),
	('horizontal meters', 'METERS', 'HORIZ'), ('vertical meters', 'METERS', 'VERT'), ('disabled meters', 'METERS', 'OFF'),
	('panning', 'PAN', 'PAGINA'), ('stereo separation', 'STEREO', 'PAGINA'), ('sends for', 'SENDS', 'PAGINA'), ('effects for', 'EFFECTS', 'PAGINA'), ('eq for', 'EQ', 'PAGINA'), ('lotsa free', 'FREE', 'PAGINA')]
NanoFold = str.maketrans('\u00e1\u00e9\u00ed\u00f3\u00fa\u00e0\u00e8\u00ec\u00f2\u00f9\u00e4\u00eb\u00ef\u00f6\u00fc\u00e2\u00ea\u00ee\u00f4\u00fb\u00f1\u00e7\u00c1\u00c9\u00cd\u00d3\u00da\u00c0\u00c8\u00cc\u00d2\u00d9\u00c4\u00cb\u00cf\u00d6\u00dc\u00c2\u00ca\u00ce\u00d4\u00db\u00d1\u00c7', 'aeiouaeiouaeiouaeiouncAEIOUAEIOUAEIOUAEIOUNC')

def NanoFit(Text): # Nano Air: exactly 7 plain characters for one line of the screen
	Text = str(Text).translate(NanoFold)
	return ''.join(c if 32 <= ord(c) <= 127 else '?' for c in Text)[:7].ljust(7)

def NanoAbbrev(Text, Size = 7): # Nano Air: squeeze a name into 7 characters ('Insert 12' -> 'Ins 12', 'Kick Drum' -> 'KickDrm')
	Text = ' '.join(str(Text).translate(NanoFold).split())
	if len(Text) <= Size:
		return Text
	for Long, Short in (('Insert ', 'Ins '), ('Pattern ', 'Pat '), ('Channel ', 'Ch ')):
		Text = Text.replace(Long, Short)
	if len(Text) <= Size:
		return Text
	Chars = list(Text.replace(' ', ''))
	n = len(Chars) - 1
	while (len(Chars) > Size) and (n > 0): # drop vowels inside words, the last ones first
		if (Chars[n] in 'aeiou') and Chars[n - 1].isalpha():
			del Chars[n]
		n -= 1
	return ''.join(Chars)[:Size]

def NanoWrap(Text): # Nano Air: a long text on the two lines, whole words where they fit
	Words, Lines = str(Text).split(), []
	for Row in range(0, 2):
		Line = ''
		while Words and (len((Line + ' ' + Words[0]).strip()) <= 7):
			Line = (Line + ' ' + Words.pop(0)).strip()
		if (not Line) and Words:
			Line = NanoAbbrev(Words.pop(0))
		Lines.append(Line)
	return (Lines[0], Lines[1])

def NanoShort(Value): # Nano Air: squeeze an FL value ('-3.2 dB' -> '-3.2dB', '25% left' -> '25%L')
	Value = ' '.join(str(Value).translate(NanoFold).split())
	if Value.lower().startswith('-inf'):
		return '-INF dB'
	for Long, Short in ((' dB', 'dB'), ('% left', '%L'), ('% right', '%R'), ('Centered', 'C')):
		Value = Value.replace(Long, Short)
	if Value.lower() in ('on', 'off'):
		return Value.upper()
	return NanoAbbrev(Value)

def NanoOnOff(Value):
	return 'ON' if Value else 'OFF'

def NanoVolText(t): # Nano Air: a mixer track's volume in dB ('-7.5dB'); getEventValue's 0..2^30 scale makes getEventIDValueString give 'INFdB'
	try:
		if mixer.getTrackVolume(t) <= 0:
			return '-INF dB'
		d = round(mixer.getTrackVolume(t, 1), 1)
	except Exception:
		v = mixer.getTrackPluginId(t, 0) + midi.REC_Mixer_Vol
		return NanoShort(mixer.getEventIDValueString(v, mixer.getAutoSmoothEventValue(v)))
	if d <= -100:
		return '-INF dB'
	if d == 0:
		return '0.0dB'
	return ('+%.1fdB' if d > 0 else '%.1fdB') % d

def NanoTempo(): # Nano Air: the project tempo in BPM
	t = mixer.getCurrentTempo()
	if t >= 1000: # given as BPM x 1000
		t = t / 1000
	return t

def NanoTempoText():
	return ('%.3f' % NanoTempo()).rstrip('0').rstrip('.')

def NanoTempoDigits(): # Nano Air: the tempo for the 10-digit display: '140.00' on the bars and beats digits
	Whole, Frac = ('%.2f' % NanoTempo()).split('.')
	Whole = Whole[-3:].rjust(3)
	return Whole[:2] + chr(ord(Whole[2]) + 0x40) + Frac + '     ' # + 0x40 lights the dot

class TMackieCol:
	def __init__(self):
		self.TrackNum = 0
		self.BaseEventID = 0
		self.KnobEventID = 0 
		self.KnobPressEventID = 0
		self.KnobResetEventID = 0
		self.KnobResetValue = 0
		self.KnobMode = 0
		self.KnobCenter = 0
		self.SliderEventID = 0
		self.Peak = 0
		self.Tag = 0
		self.SliderName = ""
		self.KnobName = ""
		self.LastValueIndex = 0
		self.ZPeak = False
		self.Dirty = False
		self.KnobHeld = False
		self.NanoTgt = -1 # Nano Air: last fader position sent (14-bit)
		self.NanoPhys = -1 # Nano Air: where the motor fader most likely is
		self.NanoT = 0.0
		self.NanoKick = 0 # 0 = nothing pending, 1 = overshoot sent, 2 = done
		self.NanoKickT = 0.0
		self.NanoTouched = False
		self.NanoLastPB = -1 # Nano Air: the last fader position taken from the hand
		self.NanoDir = 0 # Nano Air: the direction of the last move taken (1 up, -1 down)
		self.NanoSid = -1 # Nano Air: the event the fader drove at its last message
		self.NanoHoldOff = False # Nano Air: ignore the fader until it reaches the newly selected track's level


class TMackieCU():
	def __init__(self):
		self.LastMsgLen =  0x37
		self.TempMsgT = ["", ""]
		self.LastTimeMsg = bytearray(10)

		self.Shift = False
		self.TempMsgDirty = False
		self.JogSource = 0
		self.UndoJogged = False
		self.UndoPrevJogSource = 0
		self.NanoLatchJogged = False
		self.NanoLatchWasOn = False
		self.NanoTemp = None # Nano Air screen: (top, bottom) of the message on the screen
		self.NanoTempUntil = 0.0
		self.NanoPending = None # (time, function): a state read back from FL a moment later
		self.NanoLast = [None, None]
		self.NanoClosing = False
		self.NanoNextIdle = 0.0
		self.NanoErr = False
		self.NanoDirty = True # Nano Air screen: something changed, drawn on the next OnIdle
		self.NanoNextWrite = 0.0
		self.NanoTempOwned = False # the message on the screen is the script's own confirmation
		self.NanoTempInput = 0 # NanoInput when that confirmation went up
		self.NanoInput = 0 # counts presses, wheel turns and fader moves
		self.NanoLastValid = None # the last normal view with a valid selected track
		self.NanoLastValidT = 0.0
		self.NanoStrip = -1 # the strip (0-7) the fader is on, learned from the controller; -1 = not known yet
		self.NanoTempSlot = False # the message belongs to the fader's square only
		self.NanoSelTrack = -1 # the selected track the last time FL said the selection changed
		self.NanoFKeys = set() # yellow keys pressed with Shift (released as the same F key)
		self.NanoUndoT = 0.0 # when the Undo key went down
		self.NanoLastMix = None # Mixer mode: the last valid track name and when it was seen
		self.NanoLastMixT = 0.0
		self.NanoMarkerText = '' # Marker mode: the last jump
		self.NanoLastValidInput = 0 # NanoInput when the last valid normal view was drawn
		self.NanoLastFlush = 0.0
		self.TempMsgCount = 0
		self.SliderHoldCount = 0
		self.FirstTrack = 0
		self.FirstTrackT = [0, 0]
		self.ColT = [0 for x in range(9)]
		for x in range(0, 9):
			self.ColT[x] = TMackieCol()

		self.FreeCtrlT = [0 for x in range(MackieCU_nFreeTracks - 1 + 2)]  # 64+1 sliders
		self.Clicking = False
		self.Scrub = False
		self.Flip = False
		self.MeterMode = 0
		self.CurMeterMode = 0
		self.Page = 0
		self.SmoothSpeed = 0
		self.MeterMax = 0
		self.ActivityMax = 0

		self.MackieCU_PageNameT = ('Panning                                (press to reset)', 'Stereo separation                      (press to reset)',  'Sends for selected track              (press to enable)', 'Effects for selected track            (press to enable)', 'EQ for selected track                  (press to reset)',  'Lotsa free controls')
		self.MackieCU_MeterModeNameT = ('Horizontal meters mode', 'Vertical meters mode', 'Disabled meters mode')
		self.MackieCU_ExtenderPosT = ('left', 'right')

		self.FreeEventID = 400
		self.ArrowsStr = chr(0x7F) + chr(0x7E) + chr(0x32)
		self.AlphaTrack_SliderMax = round(13072 * 16000 / 12800)
		self.ExtenderPos = ExtenderLeft

	def OnInit(self):

		self.FirstTrackT[0] = 1
		self.NanoClosing = False # Nano Air screen: draw everything again
		self.NanoLast = [None, None]
		self.NanoDirty = True
		self.FirstTrack = 0
		self.SmoothSpeed = 469
		self.Clicking = True

		device.setHasMeters()
		self.LastTimeMsg = bytearray(10)

		for m in range (0, len(self.FreeCtrlT)):
			self.FreeCtrlT[m] = 8192 # default free faders to center
		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0C, 1, 0xF7]))

		self.SetBackLight(2) # backlight timeout to 2 minutes
		self.UpdateClicking()
		self.UpdateMeterMode()

		self.SetPage(self.Page)
		self.SetJogSource(0)
		self.OnSendTempMsg('Linked to ' + ui.getProgTitle() + ' (' + ui.getVersion() + ')', 2000);
		if NanoScreen: # Nano Air: draw at once (FL may not call OnIdle while it loads a project)
			self.NanoFlush()
		print('OnInit ready')

	def OnDeInit(self):
		if NanoScreen: # Nano Air: leave the screen clean
			self.NanoClosing = True
			if device.isAssigned():
				self.NanoSendRaw(1, NanoFit('FL' if ui.isClosing() else '') * 8)
				self.NanoSendRaw(0, NanoFit('CERRADO' if ui.isClosing() else '') * 8)

		if device.isAssigned():

			for m in range(0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, 0, 0xF7]))

			if ui.isClosing():
				self.SendMsg(ui.getProgTitle() + ' session closed at ' + time.ctime(time.time()), 0)
			else:
				self.SendMsg('')

			self.SendMsg('', 1)
			self.SendTimeMsg('')
			self.SendAssignmentMsg('  ')

		print('OnDeInit ready')

	def OnDirtyMixerTrack(self, SetTrackNum):

		for m in range(0, len(self.ColT)):
			if (self.ColT[m].TrackNum == SetTrackNum) | (SetTrackNum == -1):
				self.ColT[m].Dirty = True
		if NanoFollowSelected and ((SetTrackNum == -1) or (SetTrackNum == mixer.trackNumber())): # Nano Air: the fader follows the selected track
			for m in range(0, 8):
				self.ColT[m].Dirty = True

	def OnRefresh(self, flags):

		if flags & midi.HW_Dirty_Mixer_Sel:
			self.UpdateMixer_Sel()
			if NanoFollowSelected: # Nano Air: the fader, Mute/Solo/Rec LEDs and the name move to the newly selected track
				t = mixer.trackNumber() # Nano Air: a new track under a touched fader: wait until the fader reaches its level
				if t != self.NanoSelTrack:
					self.NanoSelTrack = t
					for n in range(0, 8):
						if self.ColT[n].NanoTouched:
							self.ColT[n].NanoHoldOff = True
				for n in range(0, 8):
					self.UpdateCol(n)
				self.UpdateTextDisplay()

		if flags & midi.HW_Dirty_Mixer_Display:
			self.UpdateTextDisplay()
			self.UpdateColT()

		if flags & midi.HW_Dirty_Mixer_Controls:
			for n in range(0, len(self.ColT)):
				if self.ColT[n].Dirty:
					self.UpdateCol(n)

		# LEDs
		if flags & midi.HW_Dirty_LEDs:
			self.UpdateLEDs()
		if NanoScreen: # Nano Air: the selection, names or volume may have changed
			self.NanoRender()

	def TrackSel(self, Index, Step):

		Index = 2 - Index
		device.baseTrackSelect(Index, Step)
		if Index == 0:
			s = channels.getChannelName(channels.channelNumber())
			self.OnSendTempMsg(self.ArrowsStr + 'Channel: ' + s, 500);
		elif Index == 1:
			self.OnSendTempMsg(self.ArrowsStr + 'Mixer track: ' + mixer.getTrackName(mixer.trackNumber()), 500);
		elif Index == 2:
			s = patterns.getPatternName(patterns.patternNumber())
			self.OnSendTempMsg(self.ArrowsStr + 'Pattern: ' + s, 500);

	def Jog(self, event):

		if event.outEv != 0:
			self.NanoLatchJogged = True # Nano Air: the wheel was used while a mode button was held
		if self.JogSource == 0:
			transport.globalTransport(midi.FPT_Jog + int(self.Shift ^ self.Scrub), event.outEv, event.pmeFlags) # relocate
		elif self.JogSource == MackieCUNote_Move:
			transport.globalTransport(midi.FPT_MoveJog, event.outEv, event.pmeFlags)
		elif self.JogSource == MackieCUNote_Marker:
			if self.Shift:
				s = 'Marker selection'
			else:
				s = 'Marker jump'
			if event.outEv != 0:
				if transport.globalTransport(midi.FPT_MarkerJumpJog + int(self.Shift), event.outEv, event.pmeFlags) == midi.GT_Global:
					s = ui.getHintMsg()
			self.OnSendTempMsg(self.ArrowsStr + s, 500)

		elif self.JogSource == MackieCUNote_Undo:
			if event.outEv != 0:
				self.UndoJogged = True
			if event.outEv == 0:
				s = 'Undo history'
			elif transport.globalTransport(midi.FPT_UndoJog, event.outEv, event.pmeFlags) == midi.GT_Global:
				s = ui.getHintMsg() # Nano Air: was ui.GetHintMsg()
			self.OnSendTempMsg(self.ArrowsStr + s + ' (level ' + general.getUndoLevelHint() + ')', 500)

		elif self.JogSource == MackieCUNote_Zoom:
			if event.outEv != 0:
				transport.globalTransport(midi.FPT_HZoomJog + int(self.Shift), event.outEv, event.pmeFlags)

		elif self.JogSource == MackieCUNote_Window:

			if event.outEv != 0:
				transport.globalTransport(midi.FPT_WindowJog, event.outEv, event.pmeFlags)
			s = ui.getFocusedFormCaption()
			if s != "":
				self.OnSendTempMsg(self.ArrowsStr + 'Current window: ' + s, 500)

		elif (self.JogSource == MackieCUNote_Pat) | (self.JogSource == MackieCUNote_Mix) | (self.JogSource == MackieCUNote_Chan):
			self.TrackSel(self.JogSource - MackieCUNote_Pat, event.outEv)

		elif self.JogSource == MackieCUNote_Tempo:
			if event.outEv != 0:
				general.processRECEvent(midi.REC_Tempo, channels.incEventValue(midi.REC_Tempo, event.outEv, midi.EKRes), midi.PME_RECFlagsT[int(event.pmeFlags & midi.PME_LiveInput != 0)] - midi.REC_FromMIDI)
			self.OnSendTempMsg(self.ArrowsStr + 'Tempo: ' + mixer.getEventIDValueString(midi.REC_Tempo, mixer.getCurrentTempo()), 500)

		elif self.JogSource in [MackieCUNote_Free1, MackieCUNote_Free2, MackieCUNote_Free3, MackieCUNote_Free4]:
			# CC
			event.data1 = 390 + self.JogSource - MackieCUNote_Free1

			if event.outEv != 0:
				event.isIncrement = 1
				s = chr(0x7E + int(event.outEv < 0))
				self.OnSendTempMsg(self.ArrowsStr + 'Free jog ' + str(event.data1) + ': ' + s, 500)
				device.processMIDICC(event)
				return
			else:
				self.OnSendTempMsg(self.ArrowsStr + 'Free jog ' + str(event.data1), 500)


	def OnMidiMsg(self, event):
		if (event.midiId in [midi.MIDI_CONTROLCHANGE, midi.MIDI_PITCHBEND]) or ((event.midiId == midi.MIDI_NOTEON) and (event.data2 > 0)):
			self.NanoInput += 1 # Nano Air: a new touch on the controller (its message may replace an older one)
		if NanoStrips: # Nano Air: learn which strip the fader is on (fader, touch, Select, Mute, Solo, Rec all come from it)
			if (event.midiId == midi.MIDI_PITCHBEND) and (event.midiChan < 8):
				self.NanoSetStrip(event.midiChan)
			elif (event.midiId == midi.MIDI_NOTEON) and (event.data2 > 0) and ((event.data1 <= 0x1F) or (0x68 <= event.data1 <= 0x6F)):
				self.NanoSetStrip(event.data1 & 7)

		ArrowStepT = [2, -2, -1, 1]
		CutCopyMsgT = ('Cut', 'Copy', 'Paste', 'Insert', 'Delete')  #FPT_Cut..FPT_Delete

		if (event.midiId == midi.MIDI_CONTROLCHANGE):
			if (event.midiChan == 0):
				event.inEv = event.data2
				if event.inEv >= 0x40:
					event.outEv = -(event.inEv - 0x40)
				else:
					event.outEv = event.inEv

				if event.data1 == 0x3C:
					self.Jog(event)
					event.handled = True
					# knobs
				elif event.data1 in [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17]:
					r = utils.KnobAccelToRes2(event.outEv)  #todo outev signof
					Res = r * (1 / (40 * 2.5))
					if self.Page == MackieCUPage_Free:
						i = event.data1 - 0x10
						self.ColT[i].Peak = self.ActivityMax
						event.data1 = self.ColT[i].BaseEventID + int(self.ColT[i].KnobHeld)
						event.isIncrement = 1
						s = chr(0x7E + int(event.outEv < 0))
						self.OnSendTempMsg('Free knob ' + str(event.data1) + ': ' + s, 500)
						device.processMIDICC(event)
						device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
					else:
						self.SetKnobValue(event.data1 - 0x10, event.outEv, Res)
						event.handled = True
				else:
					event.handled = False # for extra CCs in emulators
			else:
				event.handled = False # for extra CCs in emulators

		elif event.midiId == midi.MIDI_PITCHBEND: # pitch bend (faders)

			if event.midiChan <= 8:
				event.inEv = event.data1 + (event.data2 << 7)
				event.outEv = (event.inEv << 16) // 16383
				event.inEv -= 0x2000

				if self.Page == MackieCUPage_Free:
					self.ColT[event.midiChan].Peak = self.ActivityMax
					self.FreeCtrlT[self.ColT[event.midiChan].TrackNum] = event.data1 + (event.data2 << 7)
					device.hardwareRefreshMixerTrack(self.ColT[event.midiChan].TrackNum)
					event.data1 = self.ColT[event.midiChan].BaseEventID + 7
					event.midiChan = 0
					event.midiChanEx = event.midiChanEx & (not 0xF)
					self.OnSendTempMsg('Free slider ' + str(event.data1) + ': ' + ui.getHintValue(event.outEv, 65536), 500)
					device.processMIDICC(event)
				elif self.ColT[event.midiChan].SliderEventID >= 0:
					# slider (mixer track volume)
					event.handled = True
					self.ColT[event.midiChan].NanoPhys = event.inEv + 0x2000 # Nano Air: the fader is where the hand put it
					if NanoDebug:
						print('IN  fader strip ' + str(event.midiChan + 1) + ' moved to ' + str(event.inEv + 0x2000))
					c = self.ColT[event.midiChan] # Nano Air: a resting finger's jitter is not a move; after a track change under the finger, wait for the fader
					Pos = event.inEv + 0x2000
					sid = self.NanoSliderEventID(event.midiChan)
					if c.NanoTouched and (c.NanoSid >= 0) and (sid != c.NanoSid): # the fader now drives another track while the finger stays on it
						c.NanoHoldOff = True
					c.NanoSid = sid
					if c.NanoHoldOff: # take the new track over only when the fader reaches its level (or after the finger lets go)
						if abs(Pos - self.AlphaTrack_LevelToSlider(mixer.getEventValue(sid))) > NanoFaderPickup:
							return
						c.NanoHoldOff = False
						c.NanoLastPB = -1
					if c.NanoLastPB >= 0:
						d = Pos - c.NanoLastPB
						if (abs(d) <= NanoFaderDeadband) or ((d * c.NanoDir < 0) and (abs(d) <= 2 * NanoFaderDeadband)):
							return # a resting finger: small steps, and a turn back must be bigger than a step forward
						c.NanoDir = 1 if d > 0 else -1
					c.NanoLastPB = Pos
					sid = self.NanoSliderEventID(event.midiChan) # Nano Air: the selected track when the fader follows the selection
					mixer.automateEvent(sid, self.AlphaTrack_SliderToLevel(event.inEv + 0x2000), midi.REC_MIDIController, self.SmoothSpeed)
					# hint
					n = mixer.getAutoSmoothEventValue(sid)
					s = mixer.getEventIDValueString(sid, n)
					if s != '':
						s = ': ' + s
					if NanoScreen: # Nano Air: one steady screen while the fader moves (FL's 'Vol' hint alternated with it)
						self.NanoFaderMsg(event.midiChan, s, event.inEv + 0x2000)
					else:
						self.OnSendTempMsg(self.NanoSliderName(event.midiChan) + s, 500)

		elif (event.midiId == midi.MIDI_NOTEON) | (event.midiId == midi.MIDI_NOTEOFF):  # NOTE
			if event.midiId == midi.MIDI_NOTEON:
				# slider hold
				if event.data1 in [0x68, 0x69, 0x70]:
					self.SliderHoldCount += -1 + (int(event.data2 > 0) * 2)
				if NanoDebug and (event.data2 > 0) and ((0x18 <= event.data1 <= 0x1F) or (event.data1 in [0x2E, 0x2F, 0x30, 0x31]) or (0x68 <= event.data1 <= 0x70)):
					print('IN  note ' + hex(event.data1) + (' select strip ' + str(event.data1 - 0x17) if 0x18 <= event.data1 <= 0x1F else '') + (' touch strip ' + str(event.data1 - 0x67) if 0x68 <= event.data1 <= 0x70 else ''))
				if (event.data1 >= 0x68) and (event.data1 <= 0x70): # Nano Air: fader touch (0x70 = master)
					self.ColT[event.data1 - 0x68].NanoTouched = event.data2 > 0
					if event.data2 == 0: # Nano Air: released: the next touch starts fresh
						c = self.ColT[event.data1 - 0x68]
						c.NanoLastPB = -1
						c.NanoHoldOff = False
						c.NanoSid = -1
						c.NanoDir = 0

				if (event.pmeFlags & midi.PME_System != 0):
					# F1..F8
					if (event.data1 in [0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]) and (self.Shift or (event.data1 in self.NanoFKeys)): # Nano Air: released as an F key even if Shift went up first
						if event.data2 > 0:
							self.NanoFKeys.add(event.data1)
						else:
							self.NanoFKeys.discard(event.data1)
						transport.globalTransport(midi.FPT_F1 - 0x36 + event.data1, int(event.data2 > 0) * 2, event.pmeFlags)
						event.data1 = 0xFF

					if event.data1 == 0x34: # display mode
						if event.data2 > 0:
							if self.Shift:
								self.ExtenderPos = abs(self.ExtenderPos - 1)
								self.FirstTrackT[self.FirstTrack] = 1
								self.SetPage(self.Page)
								self.OnSendTempMsg('Extender on ' + self.MackieCU_ExtenderPosT[self.ExtenderPos], 1500)
							else:
								self.MeterMode = (self.MeterMode + 1) % 3
								self.OnSendTempMsg(self.MackieCU_MeterModeNameT[self.MeterMode])
								self.UpdateMeterMode()
								device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )
					elif event.data1 == 0x35: # time format
						if event.data2 > 0:
							ui.setTimeDispMin()
							self.NanoLater(lambda: ('TIEMPO', 'MIN:SEG' if ui.getTimeDispMin() else 'COMPAS'))
					elif (event.data1 == 0x2E) | (event.data1 == 0x2F): # mixer bank
						if event.data2 > 0:
							self.SetFirstTrack(self.FirstTrackT[self.FirstTrack] - 8 + int(event.data1 == 0x2F) * 16)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16))
					elif (event.data1 == 0x30) | (event.data1 == 0x31):
						if event.data2 > 0:
							self.SetFirstTrack(self.FirstTrackT[self.FirstTrack] - 1 + int(event.data1 == 0x31) * 2)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )
					elif event.data1 == 0x32: # self.Flip
						if event.data2 > 0:
							self.Flip = not self.Flip
							self.NanoMsg('FLIP', NanoOnOff(self.Flip))
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16))
							self.UpdateColT()
							self.UpdateLEDs()
					elif event.data1 == 0x33: # smoothing
						if event.data2 > 0:
							self.SmoothSpeed = int(self.SmoothSpeed == 0) * 469
							self.UpdateLEDs()
							self.OnSendTempMsg('Control smoothing ' + OffOnStr[int(self.SmoothSpeed > 0)])
					elif event.data1 == 0x65: # self.Scrub
						if event.data2 > 0:
							self.Scrub = not self.Scrub
							self.NanoMsg('SCRUB', NanoOnOff(self.Scrub))
							self.UpdateLEDs()
							# jog sources
					elif event.data1 == MackieCUNote_Zoom: # Nano Air: ZOOM latches (tap on / tap off)
						if event.data2 > 0:
							if self.JogSource == MackieCUNote_Zoom:
								self.SetJogSource(0)
								self.OnSendTempMsg('Zoom off', 500)
							else:
								self.SetJogSource(MackieCUNote_Zoom)
								self.OnSendTempMsg('Zoom on: up/down = vertical, left/right = horizontal', 1500)
					elif event.data1 == MackieCUNote_Undo: # Nano Air: tap = undo one step, hold + wheel = undo history
						self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
						if event.data2 > 0:
							self.UndoJogged = False
							self.NanoUndoT = time.time()
							self.UndoPrevJogSource = self.JogSource if self.JogSource != MackieCUNote_Undo else 0
							self.SetJogSource(MackieCUNote_Undo)
						else:
							if self.JogSource == MackieCUNote_Undo:
								self.SetJogSource(self.UndoPrevJogSource)
							if not self.UndoJogged:
								if transport.globalTransport(midi.FPT_UndoUp, 1, event.pmeFlags) == midi.GT_Global:
									if time.time() - self.NanoUndoT >= 0.3: # Nano Air: the UNDO view was up while held: no flash of the normal view
										self.NanoMsg('UNDO', general.getUndoLevelHint())
									self.NanoLater(lambda: ('UNDO', general.getUndoLevelHint()))
									self.OnSendTempMsg(ui.getHintMsg() + ' (level ' + general.getUndoLevelHint() + ')')
					elif NanoLatchJogSources and (event.data1 in NanoLatchNames): # Nano Air: tap = stays on, hold + wheel = off on release
						if event.data2 > 0:
							self.NanoLatchJogged = False
							self.NanoLatchWasOn = self.JogSource == event.data1
							if not self.NanoLatchWasOn:
								self.SetJogSource(event.data1)
								self.OnSendTempMsg(NanoLatchNames[event.data1] + ' on: turn the wheel', 1000)
								event.outEv = 0
								self.Jog(event) # shows the current pattern / track / tempo, etc.
						elif self.JogSource == event.data1:
							if self.NanoLatchJogged or self.NanoLatchWasOn:
								self.NanoInput += 1 # Nano Air: turning a mode off is a new action (its OFF message may replace a confirmation)
								self.SetJogSource(0)
								if not self.NanoLatchJogged:
									self.OnSendTempMsg(NanoLatchNames[event.data1] + ' off', 500)
					elif event.data1 in [MackieCUNote_Undo, MackieCUNote_Pat, MackieCUNote_Mix, MackieCUNote_Chan, MackieCUNote_Tempo, MackieCUNote_Free1, MackieCUNote_Free2, MackieCUNote_Free3, MackieCUNote_Free4, MackieCUNote_Marker, MackieCUNote_Zoom, MackieCUNote_Move, MackieCUNote_Window]:
						# update jog source
						self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
						if event.data1 in [MackieCUNote_Zoom, MackieCUNote_Window]:
							device.directFeedback(event)
						if event.data2 == 0:
							if self.JogSource == event.data1:
								self.SetJogSource(0)
						else:
							self.SetJogSource(event.data1)
							event.outEv = 0
							self.Jog(event) # for visual feedback

					elif event.data1 in [0x60, 0x61, 0x62, 0x63]: # arrows
						if self.JogSource == 0:
							transport.globalTransport(midi.FPT_Up - 0x60 + event.data1, int(event.data2 > 0) * 2, event.pmeFlags)
						elif self.JogSource == MackieCUNote_Zoom: # Nano Air: up/down = vertical zoom (track height), left/right = horizontal zoom
							if event.data2 > 0:
								if event.data1 in [0x60, 0x61]:
									transport.globalTransport(midi.FPT_VZoomJog, 1 if event.data1 == 0x60 else -1, event.pmeFlags)
								else:
									transport.globalTransport(midi.FPT_HZoomJog, 1 if event.data1 == 0x63 else -1, event.pmeFlags)
						else:
							if event.data2 > 0:
								event.inEv = ArrowStepT[event.data1 - 0x60]
								event.outEv = event.inEv
								self.Jog(event)

					elif event.data1 in [0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D]: # self.Page
						self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
						if event.data2 > 0:
							n = event.data1 - 0x28
							self.OnSendTempMsg(self.MackieCU_PageNameT[n], 500)
							self.SetPage(n, False)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )

					elif event.data1 == 0x54: # self.Shift
						self.Shift = event.data2 > 0
						device.directFeedback(event)

					elif event.data1 == 0x55: # open audio editor in current mixer track
						device.directFeedback(event)
						if event.data2 > 0:
							ui.launchAudioEditor(False, '', mixer.trackNumber(), 'AudioLoggerTrack.fst', '')
							self.OnSendTempMsg('Audio editor ready')

					elif event.data1 == 0x57: # metronome/button self.Clicking
						if event.data2 > 0:
							if self.Shift:
								self.Clicking = not self.Clicking
								self.UpdateClicking()
								self.OnSendTempMsg('self.Clicking ' + OffOnStr[self.Clicking])
							else:
								transport.globalTransport(midi.FPT_Metronome, 1, event.pmeFlags)
								self.NanoLater(lambda: ('METRO', NanoOnOff(general.getUseMetronome())))

					elif event.data1 == 0x58: # precount
						if event.data2 > 0:
							transport.globalTransport(midi.FPT_CountDown, 1, event.pmeFlags)
							self.NanoLater(lambda: ('3..2..1', NanoOnOff(general.getPrecount())))

					elif event.data1 in [0x36, 0x37, 0x38, 0x39, 0x3A]: # cut/copy/paste/insert/delete
						transport.globalTransport(midi.FPT_Cut + event.data1 - 0x36, int(event.data2 > 0) * 2, event.pmeFlags)
						if event.data2 > 0:
							self.OnSendTempMsg(CutCopyMsgT[midi.FPT_Cut + event.data1 - 0x36 - 50])

					elif (event.data1 == 0x5B) | (event.data1 == 0x5c) : # << >>
						if self.Shift:
							if event.data2 == 0:
								v2 = 1
							elif event.data1 == 0x5B:
								v2 = 0.5
							else:
								v2 = 2
							transport.setPlaybackSpeed(v2)
						else:
							transport.globalTransport(midi.FPT_Rewind + int(event.data1 == 0x5C), int(event.data2 > 0) * 2, event.pmeFlags)
						device.directFeedback(event)

					elif event.data1 == 0x5D: # stop
						transport.globalTransport(midi.FPT_Stop, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5E: # play
						transport.globalTransport(midi.FPT_Play, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5F: # record
						transport.globalTransport(midi.FPT_Record, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5A: # song/loop
						transport.globalTransport(midi.FPT_Loop, int(event.data2 > 0) * 2, event.pmeFlags)
						if event.data2 > 0:
							self.NanoLater(lambda: ('MODO', 'PATTERN' if transport.getLoopMode() == midi.SM_Pat else 'SONG'))
					elif event.data1 == 0x59: # mode
						transport.globalTransport(midi.FPT_Mode, int(event.data2 > 0) * 2, event.pmeFlags)
						device.directFeedback(event)

					elif event.data1 == 0x56: # Nano Air: transport LOOP (Shift + LOOP = snap on/off)
						if self.Shift:
							transport.globalTransport(midi.FPT_Snap, int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.NanoLater(lambda: ('SNAP', NanoOnOff(ui.getSnapMode() != midi.Snap_None)))
						elif event.data2 > 0:
							transport.globalTransport(midi.FPT_LoopRecord, 1, event.pmeFlags)
							self.NanoLater(lambda: ('LOOPREC', NanoOnOff(ui.isLoopRecEnabled())))
							self.OnSendTempMsg(ui.getHintMsg(), 1000)

					elif event.data1 == 0x52: # ESC
						transport.globalTransport(midi.FPT_Escape + int(self.Shift) * 2, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x53: # ENTER
						transport.globalTransport(midi.FPT_Enter + int(self.Shift) * 2, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]: # knob reset
						if self.Page == MackieCUPage_Free:
							i = event.data1 - 0x20
							self.ColT[i].KnobHeld = event.data2 > 0
							if event.data2 > 0:
								self.ColT[i].Peak = self.ActivityMax
								event.data1 = self.ColT[i].BaseEventID + 2
								event.outEv = 0
								event.isIncrement = 2
								self.OnSendTempMsg('Free knob switch ' + str(event.data1), 500)
								device.processMIDICC(event)
							device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
							return
						elif event.data2 > 0:
							n = event.data1 - 0x20
							if self.Page == MackieCUPage_Sends:
								if mixer.setRouteTo(mixer.trackNumber(), self.ColT[n].TrackNum, -1) < 0:
									self.OnSendTempMsg('Cannot send to this track')
								else:
									mixer.afterRoutingChanged()
							else:
								self.SetKnobValue(n, midi.MaxInt)

					elif (event.data1 >= 0) & (event.data1 <= 0x1F): # free hold buttons
						if self.Page == MackieCUPage_Free:
							i = event.data1 % 8
							self.ColT[i].Peak = self.ActivityMax
							event.data1 = self.ColT[i].BaseEventID + 3 + event.data1 // 8
							event.inEv = event.data2
							event.outEv = int(event.inEv > 0) * midi.FromMIDI_Max
							self.OnSendTempMsg('Free button ' + str(event.data1) + ': ' + OffOnStr[event.outEv > 0], 500)
							device.processMIDICC(event)
							device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
							return

					if (event.pmeFlags & midi.PME_System_Safe != 0):
						if event.data1 == 0x47: # link selected channels to current mixer track
							if event.data2 > 0:
								if self.Shift:
									mixer.linkTrackToChannel(midi.ROUTE_StartingFromThis)
								else:
									mixer.linkTrackToChannel(midi.ROUTE_ToThis)
						elif event.data1 == 0x4A: # focus browser
							if event.data2 > 0:
								ui.showWindow(midi.widBrowser)

						elif event.data1 == 0x4B: # focus step seq
							if event.data2 > 0:
								ui.showWindow(midi.widChannelRack)

						elif event.data1 == 0x51: # menu
							transport.globalTransport(midi.FPT_Menu, int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.OnSendTempMsg('Menu', 10)

						elif event.data1 == 0x3B: # tools
							transport.globalTransport(midi.FPT_ItemMenu, int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.OnSendTempMsg('Tools', 10)

						elif event.data1 == 0x3D: # undo/redo
							if (transport.globalTransport(midi.FPT_Undo, int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global) & (event.data2 > 0):
								self.NanoLater(lambda: ('UN/REDO', general.getUndoLevelHint()))
								self.OnSendTempMsg(ui.getHintMsg() + ' (level ' + general.getUndoLevelHint() + ')')

						elif event.data1 in [0x4D, 0x4E, 0x4F]: # punch in/punch out/punch
							if event.data1 == 0x4F:
								n = midi.FPT_Punch
							else:
								n = midi.FPT_PunchIn + event.data1 - 0x4D
							if event.data1 >= 0x4E:
								self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
							if not ((event.data1 == 0x4D) & (event.data2 == 0)):
								device.directFeedback(event)
							if (event.data1 >= 0x4E) & (event.data2 >= int(event.data1 == 0x4E)):
								if device.isAssigned():
									device.midiOutMsg((0x4D << 8) + midi.TranzPort_OffOnT[False])
							if transport.globalTransport(n, int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global:
								t = -1
								if n == midi.FPT_Punch:
									if event.data2 != 1:
										t = int(event.data2 != 2)
								elif event.data2 > 0:
									t = int(n == midi.FPT_PunchOut)
								if t >= 0:
									self.OnSendTempMsg(ui.getHintMsg())

						elif event.data1 == 0x49: # marker add
							if (transport.globalTransport(midi.FPT_AddMarker + int(self.Shift), int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global) & (event.data2 > 0):
								self.OnSendTempMsg(ui.getHintMsg())
						elif (event.data1 >= 0x18) & (event.data1 <= 0x1F): # select mixer track
							if event.data2 > 0:
								i = event.data1 - 0x18

								ui.showWindow(midi.widMixer)
								mixer.setTrackNumber(self.ColT[i].TrackNum, midi.curfxScrollToMakeVisible | midi.curfxMinimalLatencyUpdate)

						elif (event.data1 >= 0x8) & (event.data1 <= 0xF): # solo
							if event.data2 > 0:
								i = event.data1 - 0x8
								self.ColT[i].solomode = midi.fxSoloModeWithDestTracks
								if self.Shift:
									self.ColT[i].solomode = self.ColT[i].solomode | midi.fxSoloModeWithSourceTracks # Nano Air: was Include(...), a NameError
								mixer.soloTrack(self.NanoTrack(i), midi.fxSoloToggle, self.ColT[i].solomode) # Nano Air: selected track when following
								self.NanoLater(lambda t = self.NanoTrack(i): ('SOLO', NanoOnOff(mixer.isTrackSolo(t))))
								mixer.setTrackNumber(self.NanoTrack(i), midi.curfxScrollToMakeVisible)

						elif (event.data1 >= 0x10) & (event.data1 <= 0x17): # mute
							if event.data2 > 0:
								mixer.enableTrack(self.NanoTrack(event.data1 - 0x10)) # Nano Air: selected track when following
								self.NanoLater(lambda t = self.NanoTrack(event.data1 - 0x10): ('MUTE', NanoOnOff(not mixer.isTrackEnabled(t))))

						elif (event.data1 >= 0x0) & (event.data1 <= 0x7): # arm
							if event.data2 > 0:
								tn = self.NanoTrack(event.data1) # Nano Air: selected track when following
								mixer.armTrack(tn)
								self.NanoLater(lambda t = tn: ('REC ARM', NanoOnOff(mixer.isTrackArmed(t))))
								if mixer.isTrackArmed(tn):
									self.OnSendTempMsg(mixer.getTrackName(tn) + ' recording to ' + mixer.getTrackRecordingFileName(tn), 2500)
								else:
									self.OnSendTempMsg(mixer.getTrackName(tn) + ' unarmed')

						elif event.data1 == 0x50: # save/save new
							transport.globalTransport(midi.FPT_Save + int(self.Shift), int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.NanoLater(lambda s = self.Shift: ('NEW VER' if s else 'SAVE', 'OK' if general.getChangedFlag() == 0 else ''), 0.4)

						event.handled = True
				else:
					event.handled = False
			else:
				event.handled = False

	def SendMsg(self, Msg, Row = 0):
		if NanoScreen: # Nano Air: the Nano screen is drawn by NanoRender
			if not self.NanoClosing:
				self.NanoRender()
			return
		sysex = bytearray([0xF0, 0x00, 0x00, 0x66, 0x14, 0x12, (self.LastMsgLen + 1) * Row]) + bytearray(Msg.ljust(self.LastMsgLen + 1, ' '), 'utf-8')
		sysex.append(0xF7)
		device.midiOutSysex(bytes(sysex))

	# update the CU time display
	def SendTimeMsg(self, Msg):

		TempMsg = bytearray(10)
		for n in range(0, len(Msg)):
			TempMsg[n] = ord(Msg[n])

		if device.isAssigned():
			#send chars that have changed
			for m in range(0, min(len(self.LastTimeMsg), len(TempMsg))):
				if self.LastTimeMsg[m] != TempMsg[m]:
					device.midiOutMsg(midi.MIDI_CONTROLCHANGE + ((0x49 - m) << 8) + ((TempMsg[m]) << 16))

		self.LastTimeMsg = TempMsg

	def SendAssignmentMsg(self, Msg):

		s_ansi = Msg + chr(0) #AnsiString(Msg);
		if device.isAssigned():
			for m in range(1, 3):
				device.midiOutMsg(midi.MIDI_CONTROLCHANGE + ((0x4C - m) << 8) + (ord(s_ansi[m]) << 16))

	def UpdateTempMsg(self):
		self.SendMsg(self.TempMsgT[int(self.TempMsgCount != 0)])

	def OnSendTempMsg(self, Msg, Duration = 1000):

		if NanoScreen: # Nano Air: a short version for the 2 x 7 screen
			self.NanoOnTemp(Msg, Duration)
		if self.CurMeterMode == 0:
			self.TempMsgCount = (Duration // 48) + 1
		self.TempMsgT[1] = Msg
		self.TempMsgDirty = True

	def OnUpdateBeatIndicator(self, Value):

		SyncLEDMsg = [ midi.MIDI_NOTEON + (0x5E << 8), midi.MIDI_NOTEON + (0x5E << 8) + (0x7F << 16), midi.MIDI_NOTEON + (0x5E << 8) + (0x7F << 16)]

		if device.isAssigned():
			device.midiOutNewMsg(SyncLEDMsg[Value], 128)

	def UpdateTextDisplay(self):

		s1 = ''
		for m in range(0, len(self.ColT) - 1):
			s = ''
			if self.Page == MackieCUPage_Free:
				s = '  ' + utils.Zeros(self.ColT[m].TrackNum + 1, 2, ' ')
			else:
				s = mixer.getTrackName(self.NanoTrack(m), 6) # Nano Air: selected track when following
			for n in range(1, 7 - len(s) + 1):
				s = s + ' '
			s1 = s1 + s

		self.TempMsgT[0] = s1

		if self.CurMeterMode == 0:
			if self.TempMsgCount == 0:
				self.UpdateTempMsg()
		else:
			self.SendMsg(s1, 1)

	def GetSplitMarks(self):
		s2 = '';
		for m in range(0, len(self.ColT) - 1):
			s2 = s2 + '      .'
		return s2

	def UpdateMeterMode(self):

		# force vertical (activity) meter mode for free controls self.Page
		if self.Page == MackieCUPage_Free:
			self.CurMeterMode = 1
		else:
			self.CurMeterMode = self.MeterMode

		if device.isAssigned():
			#clear peak indicators
			for m in range(0, len(self.ColT) - 1):
				device.midiOutMsg(midi.MIDI_CHANAFTERTOUCH + (0xF << 8) + (m << 12))
			# disable all meters
			for m in range (0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, 0, 0xF7]))

		# reset stuff
		if self.CurMeterMode > 0:
			self.TempMsgCount = -1
		else:
			self.TempMsgCount = 500 // 48 + 1

		self.MeterMax = 0xD + int(self.CurMeterMode == 1) # $D for horizontal, $E for vertical meters
		self.ActivityMax = 0xD - int(self.CurMeterMode == 1) * 6

		# meter split marks
		if self.CurMeterMode == 0:
			self.SendMsg(self.GetSplitMarks(), 1)
		else:
			self.UpdateTextDisplay()

		if device.isAssigned():
			# horizontal/vertical meter mode
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x21, int(self.CurMeterMode > 0), 0xF7]))

			# enable all meters
			if self.CurMeterMode == 2:
				n = 1
			else:
				n = 1 + 2;
			for m  in range(0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, n, 0xF7]))

	def SetPage(self, Value, UpdateTracks = True):

		oldPage = self.Page
		self.Page = Value

		self.FirstTrack = int(self.Page == MackieCUPage_Free)
		receiverCount = device.dispatchReceiverCount()
		if receiverCount == 0:
			self.SetFirstTrack(self.FirstTrackT[self.FirstTrack])
		elif UpdateTracks:
			if self.ExtenderPos == ExtenderLeft:
				for n in range(0, receiverCount):
					device.dispatch(n, midi.MIDI_NOTEON + (0x7F << 8) + (self.FirstTrackT[self.FirstTrack] + (n * 8) << 16))
				self.SetFirstTrack(self.FirstTrackT[self.FirstTrack] + receiverCount * 8)
			elif self.ExtenderPos == ExtenderRight:
				self.SetFirstTrack(self.FirstTrackT[self.FirstTrack])
				for n in range(0, receiverCount):
					device.dispatch(n, midi.MIDI_NOTEON + (0x7F << 8) + (self.FirstTrackT[self.FirstTrack] + ((n + 1) * 8) << 16))

		if self.Page == MackieCUPage_Free:

			BaseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, self.FreeEventID + 7)
			for n in range(0,  len(self.FreeCtrlT)):
				d = mixer.remoteFindEventValue(BaseID + n * 8, 1)
				if d >= 0:
					self.FreeCtrlT[n] = min(round(d * 16384), 16384)

		if (oldPage == MackieCUPage_Free) | (self.Page == MackieCUPage_Free):
			self.UpdateMeterMode()
		self.UpdateColT()
		self.UpdateLEDs()
		self.UpdateTextDisplay()

	def UpdateMixer_Sel(self):

		if self.Page !=  MackieCUPage_Free:
			if device.isAssigned():
				for m in range(0, len(self.ColT) - 1):
					device.midiOutNewMsg(((0x18 + m) << 8) + midi.TranzPort_OffOnT[self.ColT[m].TrackNum == mixer.trackNumber()], self.ColT[m].LastValueIndex + 4)

			if self.Page in [MackieCUPage_Sends, MackieCUPage_FX]:
				self.UpdateColT()

	def UpdateCol(self, Num):

		data1 = 0
		data2 = 0
		baseID = 0
		center = 0
		b = False

		if device.isAssigned():
			if self.Page == MackieCUPage_Free:
				baseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, self.ColT[Num].BaseEventID)
				# slider
				m = self.FreeCtrlT[self.ColT[Num].TrackNum]
				device.midiOutNewMsg(midi.MIDI_PITCHBEND + Num + ((m & 0x7F) << 8) + ((m >> 7) << 16), self.ColT[Num].LastValueIndex + 5)
				if Num < 8:
					# ring
					d = mixer.remoteFindEventValue(baseID + int(self.ColT[Num].KnobHeld))
					if d >= 0:
						m = 1 + round(d * 10)
					else:
						m = int(self.ColT[Num].KnobHeld) * (11 + (2 << 4))
					device.midiOutNewMsg(midi.MIDI_CONTROLCHANGE + ((0x30 + Num) << 8) + (m << 16), self.ColT[Num].LastValueIndex)
					# buttons
					for n in range(0, 4)            :
						d = mixer.remoteFindEventValue(baseID + 3 + n)
						if d >= 0:
							b = d >= 0.5
						else:
							b = False

						device.midiOutNewMsg(((n * 8 + Num) << 8) + midi.TranzPort_OffOnT[b], self.ColT[Num].LastValueIndex + 1 + n)
			else:
				sv = mixer.getEventValue(self.NanoSliderEventID(Num)) # Nano Air: selected track when following

				if Num < 8:
					# V-Pot
					center = self.ColT[Num].KnobCenter
					if self.ColT[Num].KnobEventID >= 0:
						m = mixer.getEventValue(self.ColT[Num].KnobEventID, midi.MaxInt, False)
						if center < 0:
							if self.ColT[Num].KnobResetEventID == self.ColT[Num].KnobEventID:
								center = int(m !=  self.ColT[Num].KnobResetValue)
							else:
								center = int(sv !=  self.ColT[Num].KnobResetValue)

						if self.ColT[Num].KnobMode < 2:
							data1 = 1 + round(m * (10 / midi.FromMIDI_Max))
						else:
							data1 = round(m * (11 / midi.FromMIDI_Max))
						if self.ColT[Num].KnobMode > 3:
							data1 = (center << 6)
						else:
							data1 = data1 + (self.ColT[Num].KnobMode << 4) + (center << 6)
					else:
						Data1 = 0

					device.midiOutNewMsg(midi.MIDI_CONTROLCHANGE + ((0x30 + Num) << 8) + (data1 << 16), self.ColT[Num].LastValueIndex)

					# arm, solo, mute
					device.midiOutNewMsg( ((0x00 + Num) << 8) + midi.TranzPort_OffOnBlinkT[int(mixer.isTrackArmed(self.NanoTrack(Num))) * (1 + int(transport.isRecording()))], self.ColT[Num].LastValueIndex + 1)
					device.midiOutNewMsg( ((0x08 + Num) << 8) + midi.TranzPort_OffOnT[mixer.isTrackSolo(self.NanoTrack(Num))], self.ColT[Num].LastValueIndex + 2)
					device.midiOutNewMsg( ((0x10 + Num) << 8) + midi.TranzPort_OffOnT[not mixer.isTrackEnabled(self.NanoTrack(Num))], self.ColT[Num].LastValueIndex + 3)

				# slider
				self.NanoFaderTarget(Num, self.AlphaTrack_LevelToSlider(sv))

			Dirty = False

	def NanoRender(self): # Nano Air: the screen changed; it is drawn on the next OnIdle, so a burst of changes shows only its end
		self.NanoDirty = True

	def NanoFlush(self): # Nano Air: draw the screens (top line = MCU row 2, bottom line = MCU row 1; one 7-character square per strip)
		if self.NanoClosing or not device.isAssigned():
			return
		self.NanoLastFlush = time.time()
		try:
			Temp = None
			if self.NanoTemp and (time.time() < self.NanoTempUntil):
				Temp = self.NanoTemp
				if callable(Temp[1]): # a live value, such as the volume while the fader moves
					Temp = (Temp[0], Temp[1]())
			else:
				self.NanoTemp = None
			Fader = Temp if (Temp and self.NanoTempSlot) else self.NanoBase()
			if Temp and not self.NanoTempSlot:
				Segs = [Temp] * 8 # a message: every square
			elif NanoStrips and (0 <= self.NanoStrip < 8):
				Segs = [self.NanoStripView(k) for k in range(0, 8)]
				Segs[self.NanoStrip] = Fader # the fader's square (the Nano's own screen shows this one)
			else:
				Segs = [Fader] * 8 # the fader's strip is not known yet: every square shows the fader's view
		except Exception as e:
			if not self.NanoErr: # report once, in VIEW > Script output
				self.NanoErr = True
				print('Nano Air screen: ' + repr(e))
			return
		for Row, Index in ((1, 0), (0, 1)):
			Text = ''.join(NanoFit(s[Index]) for s in Segs)
			if self.NanoLast[Row] != Text:
				self.NanoLast[Row] = Text
				self.NanoSendRaw(Row, Text)

	def NanoStripView(self, Num): # Nano Air: square Num of the external screen: its channel and what its knob does on this page
		c = self.ColT[Num]
		if self.Page == MackieCUPage_Free:
			return ('Knob %d' % (c.TrackNum + 1), '')
		if self.Page == MackieCUPage_FX:
			Top = 'FX %d' % (Num + 1)
		elif self.Page == MackieCUPage_EQ:
			Top = NanoAbbrev(c.KnobName) if c.KnobEventID >= 0 else ''
		else:
			Top = NanoAbbrev(mixer.getTrackName(c.TrackNum))
		if (c.KnobEventID < 0) or (c.KnobMode == 4):
			return (Top, '-' if Top else '')
		return (Top, NanoShort(mixer.getEventIDValueString(c.KnobEventID, mixer.getAutoSmoothEventValue(c.KnobEventID))))

	def NanoSetStrip(self, Num): # Nano Air: the strip the fader is on; its square shows the selected track
		if Num != self.NanoStrip:
			First = self.NanoStrip < 0
			self.NanoStrip = Num
			self.NanoRender()
			if First:
				try:
					print('Nano Air screen: fader on strip %d; squares %r' % (Num + 1, [self.NanoStripView(k) for k in range(0, 8)]))
				except Exception as e:
					print('Nano Air screen: ' + repr(e))

	def NanoSendRaw(self, Row, Text): # Nano Air: one whole LCD row of 56 characters
		sysex = bytearray([0xF0, 0x00, 0x00, 0x66, 0x14, 0x12, (self.LastMsgLen + 1) * Row]) + bytearray(Text.ljust(56)[:56], 'ascii', 'replace')
		sysex.append(0xF7)
		device.midiOutSysex(bytes(sysex))

	def NanoBase(self): # Nano Air: what the screen shows when no message is up
		if (self.JogSource in NanoModeNames) and not ((self.JogSource == MackieCUNote_Undo) and (not self.UndoJogged) and (time.time() - self.NanoUndoT < 0.3)):
			return (NanoModeNames[self.JogSource], self.NanoModeValue(self.JogSource)) # (a quick Undo tap shows no UNDO view: only its result)
		if self.Flip:
			return ('FLIP', 'ON')
		if self.Page == MackieCUPage_Free:
			return ('FREE', 'CTRL')
		t = mixer.trackNumber()
		if not (0 <= t < mixer.trackCount()):
			if self.NanoLastValid and (time.time() - self.NanoLastValidT < 0.5) and (self.NanoLastValidInput == self.NanoInput):
				return self.NanoLastValid # FL is switching tracks: no flash of 'MIXER -'
			return ('MIXER', '-')
		if self.Page == MackieCUPage_EQ:
			Lines = ('EQ', NanoAbbrev(mixer.getTrackName(t)))
		else:
			Lines = (NanoAbbrev(mixer.getTrackName(t)), NanoVolText(t))
		self.NanoLastValid = Lines
		self.NanoLastValidT = time.time()
		self.NanoLastValidInput = self.NanoInput
		return Lines

	def NanoModeValue(self, Mode): # Nano Air: what the wheel changes in this mode, right now
		try:
			if Mode == MackieCUNote_Mix:
				t = mixer.trackNumber()
				if 0 <= t < mixer.trackCount():
					self.NanoLastMix = NanoAbbrev(mixer.getTrackName(t))
					self.NanoLastMixT = time.time()
					return self.NanoLastMix
				if self.NanoLastMix and (time.time() - self.NanoLastMixT < 0.5):
					return self.NanoLastMix # FL is switching tracks: no flash of '-'
				return '-'
			if Mode == MackieCUNote_Chan:
				c = channels.channelNumber()
				return NanoAbbrev(channels.getChannelName(c)) if c >= 0 else '-'
			if Mode == MackieCUNote_Pat:
				return NanoAbbrev(patterns.getPatternName(patterns.patternNumber()))
			if Mode == MackieCUNote_Tempo:
				return NanoTempoText()
			if Mode == MackieCUNote_Window:
				return NanoAbbrev(ui.getFocusedFormCaption().split(' - ')[0]) or '-'
			if Mode == MackieCUNote_Undo:
				return general.getUndoLevelHint()
		except Exception:
			return '-'
		if Mode == MackieCUNote_Marker:
			return self.NanoMarkerText or 'JUMP'
		return 'ON'

	def NanoParse(self, Msg): # Nano Air: an FL message as (top, bottom), or None when the live view says it better
		Text = ' '.join(str(Msg).replace(self.ArrowsStr, ' ').split())
		Level = ''
		if '(level ' in Text:
			Text, Level = Text.split('(level ', 1)
			Text, Level = Text.strip(), Level.strip(' )')
		Name, Value = Text, ''
		if ': ' in Text:
			Name, Value = Text.split(': ', 1)
		Low = Name.lower()
		Lines = None
		for Prefix, Top, Bottom in NanoMsgMap:
			if Low.startswith(Prefix) and ((len(Low) == len(Prefix)) or (Low[len(Prefix)] in ' (')):
				Rest = Name[len(Prefix):].strip()
				if Prefix == 'free jog':
					if NanoModeNames.get(self.JogSource, '').startswith('FREE'):
						return None # Nano Air: a Free mode's wheel click: its view (FREE n / ON) stays
					Lines = (NanoModeNames.get(self.JogSource, 'FREE'), Value or 'ON')
				elif Bottom is not None:
					Lines = (Top, Bottom)
				elif Rest.lower() in ('on', 'off'):
					Lines = (Top, Rest.upper())
				else:
					Lines = (Top, NanoShort(Value or Rest))
				break
		if Lines is None:
			if Value:
				Lines = (NanoAbbrev(Name.split(' - ')[-1]), NanoShort(Value))
			elif len(Text) <= 7:
				Lines = (Text, '')
			elif ' - ' in Text: # FL's menu hints ('Menu - View ~'): the two halves
				A, B = Text.split(' - ', 1)
				Lines = (NanoAbbrev(A.strip(' ~')), NanoFit(B.strip(' ~')).strip())
			else:
				Lines = NanoWrap(Text)
		if Level and not Lines[1]:
			Lines = (Lines[0], Level)
		if (self.JogSource == MackieCUNote_Marker) and ((Lines[0] == 'MARKER') or str(Msg).startswith(self.ArrowsStr)):
			self.NanoMarkerText = Lines[1] if Lines[0] == 'MARKER' else NanoAbbrev((Lines[0] + ' ' + Lines[1]).strip()) # Nano Air: the marker mode's view shows the last jump
			return None
		if (self.JogSource == MackieCUNote_Undo) or ((self.JogSource in NanoLiveModes) and (Lines[0] == NanoModeNames[self.JogSource]) and (Lines[1] not in ('ON', 'OFF'))):
			return None # the wheel mode's own message: its live view shows the same, always up to date
		return Lines

	def NanoOnTemp(self, Msg, Duration): # Nano Air: FL wants to show a message
		now = time.time()
		if not ' '.join(str(Msg).replace(self.ArrowsStr, ' ').split()):
			return # an empty text does not blank the screen
		if self.NanoPending and (now < self.NanoPending[0]) and (self.NanoPending[2] == self.NanoInput):
			return # a state read back from FL for this same touch replaces it in a moment
		if self.NanoTemp and self.NanoTempOwned and (self.NanoTempInput == self.NanoInput) and (now < self.NanoTempUntil) and not ui.isInPopupMenu():
			return # a confirmation is up and nothing new was touched since: it stays readable (FL's menu hints still show)
		try:
			Lines = self.NanoParse(Msg)
		except Exception as e:
			Lines = None
			if not self.NanoErr:
				self.NanoErr = True
				print('Nano Air screen: ' + repr(e))
		self.NanoTemp = Lines
		self.NanoTempOwned = False
		self.NanoTempInput = self.NanoInput
		self.NanoTempSlot = bool(Lines) and (Lines[0] in NanoModeNames.values()) # a wheel mode's own message: the fader's square only
		self.NanoTempUntil = now + max(Duration, 1200) / 1000
		self.NanoRender()

	def NanoMsg(self, Top, Bottom, Duration = 1500, Slot = False): # Nano Air: a short message (Bottom may be a function: a live value; Slot: the fader's square only)
		self.NanoTemp = (Top, Bottom)
		self.NanoTempUntil = time.time() + Duration / 1000
		self.NanoTempOwned = True
		self.NanoTempInput = self.NanoInput
		self.NanoTempSlot = Slot
		self.NanoRender()

	def NanoLater(self, Fn, Delay = 0.12): # Nano Air: read a state back from FL a moment later, then show it (tagged with the touch that asked)
		self.NanoPending = (time.time() + Delay, Fn, self.NanoInput)

	def NanoScreenIdle(self): # Nano Air: read-backs, message time-outs and live values; the only regular place the screen is drawn
		if not NanoScreen:
			return
		now = time.time()
		if self.NanoNextIdle > now + 0.1: # the clock went back: do not wait for the old deadlines
			self.NanoNextIdle = now
		if self.NanoNextWrite > now + NanoScreenGap:
			self.NanoNextWrite = now
		if self.NanoPending and (now >= self.NanoPending[0]):
			Fn, Input = self.NanoPending[1], self.NanoPending[2]
			self.NanoPending = None
			if not (self.NanoTemp and (self.NanoTempInput > Input) and (now < self.NanoTempUntil)): # a newer touch already shows its own message
				try:
					Lines = Fn()
				except Exception:
					Lines = None
				if Lines:
					self.NanoMsg(Lines[0], Lines[1])
					self.NanoTempInput = Input
		if self.NanoTemp and (not self.NanoTempOwned) and ui.isInPopupMenu(): # FL's menu hint stays while its menu is open
			self.NanoTempUntil = max(self.NanoTempUntil, now + 0.3)
		if (self.NanoDirty and (now >= self.NanoNextWrite)) or (now >= self.NanoNextIdle):
			self.NanoDirty = False
			self.NanoNextIdle = now + 0.1
			self.NanoNextWrite = now + NanoScreenGap
			self.NanoFlush()

	def NanoFlushSoon(self): # Nano Air: while the fader streams, draw even if FL is slow to call OnIdle
		now = time.time()
		if (now - self.NanoLastFlush >= 0.1) and (now >= self.NanoNextWrite):
			self.NanoDirty = False
			self.NanoNextWrite = now + NanoScreenGap
			self.NanoFlush()

	def NanoFaderMsg(self, Num, Value, Pos): # Nano Air: the screen while the fader moves: one steady view, only the value changes
		if Num == 8:
			self.NanoMsg('MASTER', '%d%%' % round(self.AlphaTrack_SliderToLevel(Pos) * 100 / midi.FromMIDI_Max), 1000, True)
		elif self.NanoFollow(Num):
			t = mixer.trackNumber()
			if self.JogSource in NanoModeNames: # a wheel mode is on the screen: the track and its live volume for a moment
				self.NanoMsg(NanoAbbrev(mixer.getTrackName(t)), lambda t = t: NanoVolText(t), 1000, True)
			else: # the normal view already shows the selected track and its live volume (the newest touch wins)
				self.NanoTemp = None
				self.NanoRender()
		else: # Flip or the free page: what the fader moves and FL's value text
			self.NanoMsg(NanoAbbrev(self.NanoSliderName(Num).split(' - ')[-1]), NanoShort(Value[2:] if Value.startswith(': ') else Value), 1000, True)
		self.NanoFlushSoon()

	def NanoFollow(self, Num): # Nano Air: does strip Num follow the mixer track selected in FL?
		return NanoFollowSelected and (Num < 8) and (not self.Flip) and (self.Page in [MackieCUPage_Pan, MackieCUPage_Stereo, MackieCUPage_Sends, MackieCUPage_FX]) and (0 <= mixer.trackNumber() < mixer.trackCount())

	def NanoTrack(self, Num):
		if self.NanoFollow(Num):
			return mixer.trackNumber()
		return self.ColT[Num].TrackNum

	def NanoSliderEventID(self, Num):
		if self.NanoFollow(Num):
			return mixer.getTrackPluginId(mixer.trackNumber(), 0) + midi.REC_Mixer_Vol
		return self.ColT[Num].SliderEventID

	def NanoSliderName(self, Num):
		if self.NanoFollow(Num):
			return mixer.getTrackName(mixer.trackNumber()) + ' - Vol'
		return self.ColT[Num].SliderName

	def NanoFaderTarget(self, Num, v): # Nano Air: send a fader position and remember it for the small-move push
		c = self.ColT[Num]
		if NanoDebug and (v != c.NanoTgt):
			print('OUT fader strip ' + str(Num + 1) + ' (' + self.NanoSliderName(Num) + ') = ' + str(v) + ' (' + str(round(v * 100 / 16383)) + '%)')
		device.midiOutNewMsg(midi.MIDI_PITCHBEND + Num + ((v & 127) << 8) + ((v >> 7) << 16), c.LastValueIndex + 5)
		if v != c.NanoTgt:
			c.NanoTgt = v
			c.NanoT = time.time()
			c.NanoKick = 0
			if (c.NanoPhys < 0) or (abs(v - c.NanoPhys) >= NanoFaderMinMove):
				c.NanoPhys = v # big enough: the motor moves on its own

	def NanoSendPB(self, Num, v):
		device.midiOutMsg(midi.MIDI_PITCHBEND + Num + ((v & 127) << 8) + ((v >> 7) << 16))

	def NanoFaderIdle(self): # Nano Air: push the motor fader after small moves
		if (not NanoFaderKick) or (not device.isAssigned()) or (self.Page == MackieCUPage_Free):
			return
		now = time.time()
		for Num in range(0, len(self.ColT)):
			c = self.ColT[Num]
			if (c.NanoTgt < 0) or (c.NanoPhys < 0) or c.NanoTouched:
				continue
			if c.NanoKick == 0:
				if (abs(c.NanoTgt - c.NanoPhys) > NanoFaderTolerance) and (now - c.NanoT >= NanoFaderSettle):
					d = NanoFaderOvershoot if c.NanoTgt > c.NanoPhys else -NanoFaderOvershoot
					self.NanoSendPB(Num, min(max(c.NanoTgt + d, 0), 16383))
					c.NanoKick = 1
					c.NanoKickT = now
			elif c.NanoKick == 1:
				if now - c.NanoKickT >= NanoFaderReturn:
					self.NanoSendPB(Num, c.NanoTgt)
					c.NanoPhys = c.NanoTgt
					c.NanoKick = 2

	def AlphaTrack_LevelToSlider(self, Value, Max = midi.FromMIDI_Max):

		return round(Value / Max * self.AlphaTrack_SliderMax)

	def AlphaTrack_SliderToLevel(self, Value, Max = midi.FromMIDI_Max):

		return min(round(Value / self.AlphaTrack_SliderMax * Max), Max)

	def UpdateColT(self):

		f = self.FirstTrackT[self.FirstTrack]
		CurID = mixer.getTrackPluginId(mixer.trackNumber(), 0)

		for m in range(0, len(self.ColT)):
			if self.Page == MackieCUPage_Free:
				# free controls
				if m == 8:
					self.ColT[m].TrackNum = MackieCU_nFreeTracks
				else:
					self.ColT[m].TrackNum = (f + m) % MackieCU_nFreeTracks

				self.ColT[m].KnobName = 'Knob ' + str(self.ColT[m].TrackNum + 1)
				self.ColT[m].SliderName = 'Slider ' + str(self.ColT[m].TrackNum + 1)

				self.ColT[m].BaseEventID = self.FreeEventID + self.ColT[m].TrackNum * 8 # first virtual CC
			else:
				self.ColT[m].KnobPressEventID = -1

				# mixer
				if m == 8:
					self.ColT[m].TrackNum = -2
					self.ColT[m].BaseEventID = midi.REC_MainVol
					self.ColT[m].SliderEventID = self.ColT[m].BaseEventID
					self.ColT[m].SliderName = 'Master Vol'
				else:
					self.ColT[m].TrackNum = midi.TrackNum_Master + ((f + m) % mixer.trackCount())
					self.ColT[m].BaseEventID = mixer.getTrackPluginId(self.ColT[m].TrackNum, 0)
					self.ColT[m].SliderEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_Vol
					s = mixer.getTrackName(self.ColT[m].TrackNum)
					self.ColT[m].SliderName = s + ' - Vol'

					self.ColT[m].KnobEventID = -1
					self.ColT[m].KnobResetEventID = -1
					self.ColT[m].KnobResetValue = midi.FromMIDI_Max >> 1
					self.ColT[m].KnobName = ''
					self.ColT[m].KnobMode = 1 # parameter, pan, volume, off
					self.ColT[m].KnobCenter = -1

					if self.Page == MackieCUPage_Pan:
						self.ColT[m].KnobEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_Pan
						self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID
						self.ColT[m].KnobName = mixer.getTrackName( self.ColT[m].TrackNum) + ' - ' + 'Pan'
					elif self.Page == MackieCUPage_Stereo:
						self.ColT[m].KnobEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_SS
						self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID
						self.ColT[m].KnobName = mixer.getTrackName(self.ColT[m].TrackNum) + ' - ' + 'Sep'
					elif self.Page == MackieCUPage_Sends:
						self.ColT[m].KnobEventID = CurID + midi.REC_Mixer_Send_First + self.ColT[m].TrackNum
						s = mixer.getEventIDName(self.ColT[m].KnobEventID)
						self.ColT[m].KnobName = s
						self.ColT[m].KnobResetValue = round(12800 * midi.FromMIDI_Max / 16000)
						self.ColT[m].KnobCenter = mixer.getRouteSendActive(mixer.trackNumber(),self.ColT[m].TrackNum)
						if self.ColT[m].KnobCenter == 0:
							self.ColT[m].KnobMode = 4
						else:
							self.ColT[m].KnobMode = 2
					elif self.Page == MackieCUPage_FX:
						CurID = mixer.getTrackPluginId(mixer.trackNumber(), m)
						self.ColT[m].KnobEventID = CurID + midi.REC_Plug_MixLevel
						s = mixer.getEventIDName(self.ColT[m].KnobEventID)
						self.ColT[m].KnobName = s
						self.ColT[m].KnobResetValue = midi.FromMIDI_Max

						IsValid = mixer.isTrackPluginValid(mixer.trackNumber(), m)
						IsEnabledAuto = mixer.isTrackAutomationEnabled(mixer.trackNumber(), m)
						if IsValid:
							self.ColT[m].KnobMode = 2
							self.ColT[m].KnobPressEventID = CurID + midi.REC_Plug_Mute
						else:
							self.ColT[m].KnobMode = 4
						self.ColT[m].KnobCenter = int(IsValid & IsEnabledAuto)
					elif self.Page == MackieCUPage_EQ:
						if m < 3:
							# gain & freq
							self.ColT[m].SliderEventID = CurID + midi.REC_Mixer_EQ_Gain + m
							self.ColT[m].KnobResetEventID = self.ColT[m].SliderEventID
							s = mixer.getEventIDName(self.ColT[m].SliderEventID)
							self.ColT[m].SliderName = s
							self.ColT[m].KnobEventID = CurID + midi.REC_Mixer_EQ_Freq + m
							s = mixer.getEventIDName(self.ColT[m].KnobEventID)
							self.ColT[m].KnobName = s
							self.ColT[m].KnobResetValue = midi.FromMIDI_Max >> 1
							self.ColT[m].KnobCenter = -2
							self.ColT[m].KnobMode = 0
						else:
							if m < 6:
								# Q
								self.ColT[m].SliderEventID = CurID + midi.REC_Mixer_EQ_Q + m - 3
								self.ColT[m].KnobResetEventID = self.ColT[m].SliderEventID
								s = mixer.getEventIDName(self.ColT[m].SliderEventID)
								self.ColT[m].SliderName = s
								self.ColT[m].KnobEventID = self.ColT[m].SliderEventID
								self.ColT[m].KnobName = self.ColT[m].SliderName
								self.ColT[m].KnobResetValue = 17500
								self.ColT[m].KnobCenter = -1
								self.ColT[m].KnobMode = 2
							else:
								self.ColT[m].SliderEventID = -1
								self.ColT[m].KnobEventID = -1
								self.ColT[m].KnobMode = 4

					# self.Flip knob & slider
					if self.Flip:
						self.ColT[m].KnobEventID, self.ColT[m].SliderEventID = utils.SwapInt(self.ColT[m].KnobEventID, self.ColT[m].SliderEventID)
						s = self.ColT[m].SliderName
						self.ColT[m].SliderName = self.ColT[m].KnobName
						self.ColT[m].KnobName = s
						self.ColT[m].KnobMode = 2
						if not (self.Page in [MackieCUPage_Sends, MackieCUPage_FX, MackieCUPage_EQ]):
							self.ColT[m].KnobCenter = -1
							self.ColT[m].KnobResetValue = round(12800 * midi.FromMIDI_Max / 16000)
							self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID

			self.ColT[m].LastValueIndex = 48 + m * 6
			self.ColT[m].Peak = 0
			self.ColT[m].ZPeak = False
			self.UpdateCol(m)

	def SetKnobValue(self, Num, Value, Res = midi.EKRes):

		if (self.ColT[Num].KnobEventID >= 0) & (self.ColT[Num].KnobMode < 4):
			if Value == midi.MaxInt:
				if self.Page == MackieCUPage_FX:
					if self.ColT[Num].KnobPressEventID >= 0:

						Value = channels.incEventValue(self.ColT[Num].KnobPressEventID, 0, midi.EKRes)
						general.processRECEvent(self.ColT[Num].KnobPressEventID, Value, midi.REC_Controller)
						s = mixer.getEventIDName(self.ColT[Num].KnobPressEventID)
						self.OnSendTempMsg(s)
					return
				else:
					mixer.automateEvent(self.ColT[Num].KnobResetEventID, self.ColT[Num].KnobResetValue, midi.REC_MIDIController, self.SmoothSpeed)
			else:
				mixer.automateEvent(self.ColT[Num].KnobEventID, Value, midi.REC_Controller, self.SmoothSpeed, 1, Res)

			# hint
			n = mixer.getAutoSmoothEventValue(self.ColT[Num].KnobEventID)
			s = mixer.getEventIDValueString(self.ColT[Num].KnobEventID, n)
			if s !=  '':
				s = ': ' + s
			if NanoScreen and NanoStrips and (0 <= self.NanoStrip < 8): # Nano Air: the knob's square shows the new value
				if Num == self.NanoStrip: # that square shows the fader's track: the knob's channel and value there for a moment
					self.NanoMsg(self.NanoStripView(Num)[0], lambda Num = Num: self.NanoStripView(Num)[1], 1000, True)
				else:
					self.NanoRender()
			else:
				self.OnSendTempMsg(self.ColT[Num].KnobName + s)

	def SetFirstTrack(self, Value):

		if self.Page == MackieCUPage_Free:
			self.FirstTrackT[self.FirstTrack] = (Value + MackieCU_nFreeTracks) % MackieCU_nFreeTracks
			s = utils.Zeros(self.FirstTrackT[self.FirstTrack] + 1, 2, ' ')
		else:
			self.FirstTrackT[self.FirstTrack] = (Value + mixer.trackCount()) % mixer.trackCount()
			s = utils.Zeros(self.FirstTrackT[self.FirstTrack], 2, ' ')
		self.UpdateColT()
		self.SendAssignmentMsg(s)
		device.hardwareRefreshMixerTrack(-1)

	def OnUpdateMeters(self):

		if self.Page != MackieCUPage_Free:
			for m in range(0, len(self.ColT) - 1):
				self.ColT[m].Peak = max(self.ColT[m].Peak, round(mixer.getTrackPeaks(self.ColT[m].TrackNum, midi.PEAK_LR_INV)	* self.MeterMax))

	def OnIdle(self):

		# refresh meters
		if device.isAssigned():
			f = self.Page == MackieCUPage_Free
			for m in range(0,  len(self.ColT) - 1):
				self.ColT[m].Tag = utils.Limited(self.ColT[m].Peak, 0, self.MeterMax)
				self.ColT[m].Peak = 0
				if self.ColT[m].Tag == 0:
					if self.ColT[m].ZPeak:
						continue
					else:
						self.ColT[m].ZPeak = True
				else:
					self.ColT[m].ZPeak = f
				device.midiOutMsg(midi.MIDI_CHANAFTERTOUCH + (self.ColT[m].Tag << 8) + (m << 12))
		self.NanoFaderIdle() # Nano Air
		self.NanoScreenIdle() # Nano Air: screen read-backs, message time-outs and live values
		# time display
		if ui.getTimeDispMin():
			# HHH.MM.SS.CC_
			if playlist.getVisTimeBar() == -midi.MaxInt:
				s = '-   0'
			else:
				n = abs(playlist.getVisTimeBar())
				h, m = utils.DivModU(n, 60)
				s = utils.Zeros_Strict((h * 100 + m) * utils.SignOf(playlist.getVisTimeBar()), 5, ' ') #todo sign of...

			s = s + utils.Zeros_Strict(abs(playlist.getVisTimeStep()), 2) + utils.Zeros_Strict(playlist.getVisTimeTick(), 2) + ' '
		else:
			# BBB.BB.__.TTT
			s = utils.Zeros_Strict(playlist.getVisTimeBar(), 3, ' ') + utils.Zeros_Strict(abs(playlist.getVisTimeStep()), 2) + '  ' + utils.Zeros_Strict(playlist.getVisTimeTick(), 3)

		if NanoScreen and (self.JogSource == MackieCUNote_Tempo): # Nano Air: BPM on the digits in Tempo mode
			s = NanoTempoDigits()
		self.SendTimeMsg(s)

		# temp message
		if self.TempMsgDirty:
			self.UpdateTempMsg()
			self.TempMsgDirty = False

		if (self.TempMsgCount > 0) & (self.SliderHoldCount <= 0)  & (not ui.isInPopupMenu()):
			self.TempMsgCount -= 1
			if self.TempMsgCount == 0:
				self.UpdateTempMsg()
				if self.CurMeterMode == 0:
					self.SendMsg(self.GetSplitMarks(), 1)

	def UpdateLEDs(self):

		if device.isAssigned():
			# stop
			device.midiOutNewMsg((0x5D << 8) + midi.TranzPort_OffOnT[transport.isPlaying() == midi.PM_Stopped], 0)
			# loop
			device.midiOutNewMsg((0x5A << 8) + midi.TranzPort_OffOnT[transport.getLoopMode() == midi.SM_Pat], 1)
			# record
			r = transport.isRecording()
			device.midiOutNewMsg((0x5F << 8) + midi.TranzPort_OffOnT[r], 2)
			# SMPTE/BEATS
			device.midiOutNewMsg((0x71 << 8) + midi.TranzPort_OffOnT[ui.getTimeDispMin()], 3)
			device.midiOutNewMsg((0x72 << 8) + midi.TranzPort_OffOnT[not ui.getTimeDispMin()], 4)
			# self.Page
			for m in range(0,  6):
			  device.midiOutNewMsg(((0x28 + m) << 8) + midi.TranzPort_OffOnT[m == self.Page], 5 + m)
			# changed flag
			device.midiOutNewMsg((0x50 << 8) + midi.TranzPort_OffOnT[general.getChangedFlag() > 0], 11)
			# metronome
			device.midiOutNewMsg((0x57 << 8) + midi.TranzPort_OffOnT[general.getUseMetronome()], 12)
			# rec precount
			device.midiOutNewMsg((0x58 << 8) + midi.TranzPort_OffOnT[general.getPrecount()], 13)
			# self.Scrub
			device.midiOutNewMsg((0x65 << 8) + midi.TranzPort_OffOnT[self.Scrub], 15)
			# use RUDE SOLO to show if any track is armed for recording
			b = 0
			for m in range(0,  mixer.trackCount()):
			  if mixer.isTrackArmed(m):
			    b = 1 + int(r)
			    break

			device.midiOutNewMsg((0x73 << 8) + midi.TranzPort_OffOnBlinkT[b], 16)
			# smoothing
			device.midiOutNewMsg((0x33 << 8) + midi.TranzPort_OffOnT[self.SmoothSpeed > 0], 17)
			# self.Flip
			device.midiOutNewMsg((0x32 << 8) + midi.TranzPort_OffOnT[self.Flip], 18)
			# snap
			device.midiOutNewMsg((0x56 << 8) + midi.TranzPort_OffOnT[ui.isLoopRecEnabled()], 19) # Nano Air: LOOP LED = loop recording
			# focused windows
			device.midiOutNewMsg((0x4A << 8) + midi.TranzPort_OffOnT[ui.getFocused(midi.widBrowser)], 20)
			device.midiOutNewMsg((0x4B << 8) + midi.TranzPort_OffOnT[ui.getFocused(midi.widChannelRack)], 21)


	def SetJogSource(self, Value):
		Old = self.JogSource
		self.JogSource = Value
		if device.isAssigned(): # Nano Air: the active wheel-mode button (ZOOM included) stays lit
			if (Old != 0) and (Old != Value):
				device.midiOutMsg(midi.TranzPort_OffOnT[False] + (Old << 8))
			if Value != 0:
				device.midiOutMsg(midi.TranzPort_OffOnT[True] + (Value << 8))
			elif Old == 0:
				device.midiOutMsg(midi.TranzPort_OffOnT[False] + (MackieCUNote_Zoom << 8))
		if NanoScreen: # Nano Air: the screen shows the wheel mode
			self.NanoRender()

	def OnWaitingForInput(self):

	  self.SendTimeMsg('..........')

	def UpdateClicking(self): # switch self.Clicking for transport buttons

		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0A, int(self.Clicking), 0xF7]))

	def SetBackLight(self, Minutes): # set backlight timeout (0 should switch off immediately, but doesn't really work well)

		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0B, Minutes, 0xF7]))

MackieCU = TMackieCU()

def OnInit():
	MackieCU.OnInit()

def OnDeInit():
	MackieCU.OnDeInit()

def OnDirtyMixerTrack(SetTrackNum):
	MackieCU.OnDirtyMixerTrack(SetTrackNum)

def OnRefresh(Flags):
	MackieCU.OnRefresh(Flags)

def OnMidiMsg(event):
	MackieCU.OnMidiMsg(event)

def OnSendTempMsg(Msg, Duration = 1000):
	MackieCU.OnSendTempMsg(Msg, Duration)

def OnUpdateBeatIndicator(Value):
	MackieCU.OnUpdateBeatIndicator(Value)

def OnUpdateMeters():
	MackieCU.OnUpdateMeters()

def OnIdle():
	MackieCU.OnIdle()

def OnWaitingForInput():
	MackieCU.OnWaitingForInput()





