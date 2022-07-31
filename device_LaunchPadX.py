# name=Novation Launchpad X
# https://forum.image-line.com/viewtopic.php?f=1994&t=228184 MODIFIED TO WORK WITH X BY MiLO83 ("MiLO1983" on Image-Line Forums)
# Version 1.0
import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import midi
import utils
import math
import time

MaxInt = 2147483647
PadsW = 10
PadsH = 10
BtnMapLength = PadsH * PadsW
# clips
ClipsX = 1
ClipsY = 1
ClipsW = 9
ClipsH = 9
SceneY = 8
# solid clips
SClipsX = 1
SClipsY = 1
SClipsW = 8
SClipsH = 8
# overview
OverX = 1
OverY = 1
OverW = 8
OverH = 8
# overlay
LayX = ClipsX
LayY = ClipsY
LayW = ClipsW
LayH = ClipsH
# stride
PadsStride = 10
ForbiddenPads = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90]

MaxPads = PadsW * PadsH
NumBtns = 15

Btn_Up = 0x5B
Btn_Down = 0x5C
Btn_Left = 0x5D
Btn_Right = 0x5E

# BEGIN--------
Btn_Session = 0x5F
Btn_Note = 0x60
Btn_Custom = 0x61
Btn_CapMidi = 0x62

Btn_SpareHex = 0x63
Btn_Volume = 0x59
Btn_Pan = 0x4F
Btn_SendA = 0x45
Btn_SendB = 0x3B
Btn_StopClip = 0x31
Btn_Mute = 0x27
Btn_Solo = 0x1D
Btn_RecordArm = 0x13
# END--------

Btn_Snap = 0
Btn_ScenePlus = 1
Btn_Scene = 2
Btn_Queue = 3
Btn_Overview = 4
Btn_Spare = 5
Btn_Play = 6
Btn_Stop = 7
Btn_TapTempo = 8
Btn_TempoNudgePlus = 9
Btn_TempoNudgeMin = 10
Btn_VelLock = 11
Btn_Drums = 12
Btn_Keys = 13
Btn_User = 14

LPBlinkShift = 24
LPBlink1 = 1 << LPBlinkShift
LPBlink2 = 2 << LPBlinkShift
LPBlink3 = 3 << LPBlinkShift
LPBlink4 = 4 << LPBlinkShift
LPBlinkMask = 0xFF << LPBlinkShift

class TBtnInfo():
	def __init__(self, Id, Num, Flags, Col):
		print('\nTBtnInfo func')
		self.Id = Id
		self.Num = Num
		self.Flags = Flags
		self.Col = Col  # off, on, held

	def GetYX(self):
		print('GetYX func')
		return utils.DivModU(self.Num, PadsW)

BtnInfo = [TBtnInfo(Btn_Snap, 3, 0 ,(0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_ScenePlus, 8 ,1 ,(0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Scene, 7, 1, (0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Queue, 6, 1, (0x000100, 0x000A00 | LPBlink4, 0x002C10)), TBtnInfo(Btn_Overview, 5, 1 ,(0x000004, 0x000020 | LPBlink4, 0x00023F)), TBtnInfo(Btn_Spare, 6, 0, (0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_Play, 70, 0, (0, 0, 0)), TBtnInfo(Btn_Stop, 80, 0, (0x000200, 0x001C00, 0x000000)), TBtnInfo(Btn_TapTempo, 30, 0, (0x000102, 0x00163F, 0x000000)), TBtnInfo(Btn_TempoNudgePlus, 40, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_TempoNudgeMin, 50, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_VelLock, 60, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Drums, 96, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Keys, 97, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_User, 98, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20))]
LeftBtnInfo = [TBtnInfo(Btn_Snap, 3, 0 ,(0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_ScenePlus, 8 ,1 ,(0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Scene, 7, 1, (0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Queue, 6, 1, (0x000100, 0x000A00 | LPBlink4, 0x002C10)), TBtnInfo(Btn_Overview, 5, 1 ,(0x000004, 0x000020 | LPBlink4, 0x00023F)), TBtnInfo(Btn_Spare, 6, 0, (0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_Play, 70, 0, (0, 0, 0)), TBtnInfo(Btn_Stop, 80, 0, (0x000200, 0x001C00, 0x000000)), TBtnInfo(Btn_TapTempo, 30, 0, (0x000102, 0x00163F, 0x000000)), TBtnInfo(Btn_TempoNudgePlus, 40, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_TempoNudgeMin, 50, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_VelLock, 60, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Drums, 96, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Keys, 97, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_User, 98, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20))]
RightBtnInfo = [TBtnInfo(Btn_Snap, 3, 0 ,(0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_ScenePlus, 8 ,1 ,(0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Scene, 7, 1, (0x020000, 0x1C0000 | LPBlink4, 0x3F0A00)), TBtnInfo(Btn_Queue, 6, 1, (0x000100, 0x000A00 | LPBlink4, 0x002C10)), TBtnInfo(Btn_Overview, 5, 1 ,(0x000004, 0x000020 | LPBlink4, 0x00023F)), TBtnInfo(Btn_Spare, 6, 0, (0x040404, 0x3F3F3F, 0x000000)), TBtnInfo(Btn_Play, 79, 0, (0, 0, 0)), TBtnInfo(Btn_Stop, 89, 0, (0x000200, 0x001C00, 0x000000)), TBtnInfo(Btn_TapTempo, 39, 0, (0x000102, 0x00163F, 0x000000)), TBtnInfo(Btn_TempoNudgePlus, 49, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_TempoNudgeMin, 59, 0, (0x000102, 0x00163F | LPBlink4, 0x000000)), TBtnInfo(Btn_VelLock, 69, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Drums, 96, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_Keys, 97, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20)), TBtnInfo(Btn_User, 98, 1, (0x020001, 0x1C0010 | LPBlink4, 0x3F0A20))]

BlinkColT = ((0x280102, 0x3F3F3F), (0x100002, 0x18002F), (0x100100, 0x181000), (0x000000, 0x3F3F3F))

class TLaunchPadPro():
	def __init__(self):
		self.Shift = False
		self.ClipOfs = 0
		self.TrackOfs = 0
		self.TrackOfs_Spare = 0
		self.ClipOfs_Spare = 0
		self.BlockOfs = False # make arrows work in pages
		self.PrevClipOfs = 0
		self.ClipOfsPerfomance = 0
		self.TrackOfsPerfomance = 0
		self.BtnT = bytearray(NumBtns)
		self.ArrowT = bytearray(4)
		self.BlinkOnBars = 0
		self.BtnLastClip = [[0 for x in range(PadsW)] for y in range(PadsH)]
		self.BtnLastPressure = [[0 for x in range(PadsW)] for y in range(PadsH)]

		self.BtnMap = [[0 for x in range(PadsW)] for y in range(PadsH)]
		self.AnimBtnMap = [[0 for x in range(PadsW)] for y in range(PadsH)]
		self.ScreenCapBtnMap= [[0 for x in range(PadsW)] for y in range(PadsH)]
		self.OldBtnMap = [[0 for x in range(PadsW)] for y in range(PadsH)]

		self.NoFullRefresh = False
		self.BeatPos = 0
		self.BlinkLight = 2
		self.CurLayout = 0

		self.BtnMapMode = 0 #animation
		self.BtnMapModeRefCount = 0

		self.ScreenCapZoom = 32
		#todo ScreenCapDIB1, ScreenCapDIB2: TDIB
		#todo ScreenDC: HDC
		self.ScreenCapTime = 0
		self.ColScaleT = bytearray(256) 
		
		self.LeftBtnColumnToggle = False
		print('Lets goooooo')

	def ResetBtnLastClip(self):
		print('\nResetBtnLastClip func')
		for y in range(0, PadsW):
			for x in range(0, PadsH):
				self.BtnLastClip[x][y] = utils.TClipLauncherLastClip(MaxInt, MaxInt, MaxInt)

	def ResetBtnMap(self, BtnMapObj, val):
		print('\nResetBtnMap func')
		for y in range(0, PadsH):
			for x in range(0, PadsW):
				BtnMapObj[y][x] = val

	def UpdateBlinking(self):  #check if any blinking button
		# print('\nUpdateBlinking func')
		for y in range(0, PadsH):
			for x in range(0, PadsW):
				if self.BtnMap[y][x] > 1:
					self.FullRefresh_Btn()
					return

	def OnMidiIn(self, event):
		print ('\nOnMidiIn func', event.status )
		if event.status == midi.MIDI_BEGINSYSEX:
			# print ('midi in sysex', len(event.sysex), event.sysex[0], event.sysex[1], event.sysex[2], event.sysex[3], event.sysex[4], event.sysex[5], event.sysex[6], event.sysex[7], event.sysex[8], event.sysex[9]) #, event.sysex[10], event.sysex[11], event.sysex[12], event.sysex[13], event.sysex[14], event.sysex[15], event.sysex[16])
			#layout change
			if (len(event.sysex) == 11) & (event.sysex[5] == 0x0C):
				print('layout change')
				self.CurLayout = event.sysex[7]
			event.handled = True
		else:
			print('onmidiin else')
			event.handled = False

	def Reset(self):
		print('\nReset func')
		self.ResetBtnMap(self.BtnMap, 0)
		self.ResetBtnMap(self.AnimBtnMap, 0)
		self.ResetBtnMap(self.ScreenCapBtnMap, 0)
		self.ResetBtnMap(self.OldBtnMap, 0xFF)
		self.ResetBtnLastClip()

	def OnMidiMsg(self, event):
		print('\n\nOnMidiMsg func')
		print (event.status, event.data1, event.data2)
		ColT = (0x000000, 0x2F0018 | LPBlink2)

		if event.midiChan > 0:
			print('OnMidiMsg - midiChan > 0')
			return
		
		if (event.data1 == Btn_Note):  # drums button
			print('\nOnMidiMsg - drums (Note) clickd')
			event.handled = True
			event.midiId = midi.MIDI_CONTROLCHANGE
			
			a = event.data1 - Btn_Note
			event.handled = True
			BlockPages = (self.BtnT[Btn_Overview] > 0) | self.BlockOfs
			m = 150 + int(BlockPages) * 350 # faster in 1-pad increments
			device.repeatMidiEvent(event, m, m)
			if (event.data2 > 0) & (event.pmeFlags & midi.PME_System != 0):
				print('OnMidiMsg - data2 > 0')
				if (self.PrevClipOfs != -3):
					print('OnMidiMsg - PrevClipOfs != -3')
					self.ClipOfs = -3
				else:
					print('OnMidiMsg - PrevClipOfs else')
					self.ClipOfs = -2
				self.PrevClipOfs = self.ClipOfs
				
				m = (a) * 2 - 1
				o = self.ClipOfs + m
				self.SetOfs(self.TrackOfs, o)
				self.BtnT[Btn_Overview] = int(self.BtnT[Btn_Overview] > 0) * 2 # so that session btn works as held
				device.stopRepeatMidiEvent()
			
			self.ArrowT[2 + a] = event.data2			
			self.ArrowT[3] = event.data2
			self.CheckSpecialSwitches()
			playlist.lockDisplayZone(1 + a, event.data2 > 0)
			return
			
		if (event.data1 == Btn_Custom):  # keys button
			print('\nOnMidiMsg - Keys (Custom) clickd')
			event.handled = True
			event.midiId = midi.MIDI_CONTROLCHANGE
			
			a = event.data1 - Btn_CapMidi
			event.handled = True
			BlockPages = (self.BtnT[Btn_Overview] > 0) | self.BlockOfs
			m = 150 + int(BlockPages) * 350 # faster in 1-pad increments
			device.repeatMidiEvent(event, m, m)
			if (event.data2 > 0) & (event.pmeFlags & midi.PME_System != 0):
				if (self.PrevClipOfs != -7):
					self.ClipOfs = -7
				else:
					self.ClipOfs = 1
				self.PrevClipOfs = self.ClipOfs
				
				m = (a) * 2 - 1
				o = self.ClipOfs + m
				self.SetOfs(self.TrackOfs, o)
				self.BtnT[Btn_Overview] = int(self.BtnT[Btn_Overview] > 0) * 2 # so that session btn works as held
				device.stopRepeatMidiEvent()
			
			self.ArrowT[2 + a] = event.data2			
			self.ArrowT[3] = event.data2
			self.CheckSpecialSwitches()
			playlist.lockDisplayZone(1 + a, event.data2 > 0)
			return
			
		if (event.data1 == Btn_CapMidi):  # user button
			print('\nOnMidiMsg - USer (Capture Midi) cllickd')
			event.handled = True
			event.midiId = midi.MIDI_CONTROLCHANGE
			
			a = 0
			event.handled = True
			if (event.data2 > 0) & (event.pmeFlags & midi.PME_System != 0):
					
				if (self.ClipOfs != self.ClipOfsPerfomance) & (self.PrevClipOfs != -10) & (self.PrevClipOfs != -11):
					self.ClipOfs = self.ClipOfsPerfomance
					
				if (self.PrevClipOfs == self.ClipOfsPerfomance):
					self.ClipOfs = -11
				elif (self.PrevClipOfs == -11):
					self.ClipOfs = -12
				elif (self.PrevClipOfs == -12):
					self.ClipOfs = self.ClipOfsPerfomance
				
				self.PrevClipOfs = self.ClipOfs
				
				self.SetOfs(self.TrackOfs, self.ClipOfs)
				self.BtnT[Btn_Overview] = int(self.BtnT[Btn_Overview] > 0) * 2 # so that session btn works as held
				device.stopRepeatMidiEvent()
			
			#self.ArrowT[2 + a] = event.data2			
			#self.ArrowT[3] = event.data2
			self.CheckSpecialSwitches()
			playlist.lockDisplayZone(0, event.data2 > 0)
			return
			
		if event.midiId == midi.MIDI_CHANAFTERTOUCH:
			print('\nOnMidiMsg - midiId == midi.MIDI_CHANAFTERTOUCH')
			event.midiId = midi.MIDI_CONTROLCHANGE
			event.status = event.status & 0x0F | event.midiId
			event.inEv = event.data1
			event.outEv = round(event.inEv * (midi.FromMIDI_Max / 127))

			if self.ClipOfs < -1:
				event.midiChan = 15
				event.data1 = midi.CC_Special - 1 - self.ClipOfs
			else:
			  # clips: 1 for all clips in channel aftertouch
				event.midiChan = 0
				event.data1 = midi.CC_Special

			event.midiChanEx = event.midiChan + ((device.getPortNumber() + 1) << 6)
			device.processMIDICC(event)
			return

		elif event.midiId == midi.MIDI_KEYAFTERTOUCH:
			print('\nOnMidiMsg - else midiId == midi.MIDI_KEYAFTERTOUCH')
			event.midiId = midi.MIDI_CONTROLCHANGE
			event.status = event.status & 0x0F | event.midiId

			y = event.data1 // PadsStride
			x = event.data1 - y * PadsStride - ClipsX
			y = ClipsH - ClipsY - y
			if (x >= PadsW) | (y >= PadsH):
				return

			self.BtnLastPressure[y][x] = event.data2

			if self.ClipOfs < -1:
				x2 = y * LayW + x # get the custom page item index
				if (x2 < 0) | (x2 > High(LaunchMapPages[-self.ClipOfs - 2].Items)):
					return					
				if launchMapPages.getMapItemAftertouch(-self.ClipOfs - 2, x2) < 0: # no aftertouch CC defined, default behavior
					# special pages: 1 per page
					event.midiChan = 15
					event.data1 = midi.CC_Special - 1 - self.ClipOfs
					for m in range(0, ClipsH):
						for n in range(0, ClipsW):
							event.data2 = max(event.data2, self.BtnLastPressure[m][n]) # max of the page
				else:
					# pierre : per clip aftertouch, if defined for that item in the custom page
					event.midiChan = 15					
					event.data1 = launchMapPages.getMapItemAftertouch(-ClipOfs - 2, x2)
			else:
				event.midiChan = 0
				# clips: 1 per track
				event.data1 = midi.CC_Special + 8 + y * 16
				for n in range(0, ClipsW):
					event.data2 = max(event.data2, self.BtnLastPressure[y][n]) # max of the track
			
			event.midiChanEx = event.midiChan + ((device.getPortNumber() + 1) << 6)

			event.inEv = event.data2
			event.outEv = round(event.inEv * (midi.FromMIDI_Max / 127))
			device.processMIDICC(event)
			return

		elif event.midiId in [midi.MIDI_NOTEON, midi.MIDI_NOTEOFF, midi.MIDI_CONTROLCHANGE]: #All but Note, Custom, Capture MiDI
			print('\nOnMidiMsg - SESSION ?? event.midiId in [midi.MIDI_NOTEON:   _NoteON:', event.midiId == midi.MIDI_NOTEON,'_NoteOFF:',event.midiId == midi.MIDI_NOTEOFF,'_ControlCHANGE:',event.midiId == midi.MIDI_CONTROLCHANGE)
			if event.midiId == midi.MIDI_NOTEOFF:
				print('OnMidiMsg - SESSION event.midiId == midi.MIDI_NOTEOFF')
				event.data2 = 0
			elif (self.BtnT[Btn_VelLock] > 0) & (event.data2 > 0):
				print('OnMidiMsg - SESSION (self.BtnT[Btn_VelLock] > 0) & (even')
				event.data2 = 0x7F

			y = event.data1 // PadsStride
			x = event.data1 + 90 - y * PadsStride * 2 # top-down index
			# system buttons
			for n in range(1, len(BtnInfo)):
				# print('\nOnMidiMsg - SESSION LOOP rolling')
				if BtnInfo[n].Num == x:
					print('OnMidiMsg - SESSION 00 BtnInfo[n].Num == x')
					event.handled = True
					m2 = self.BtnT[n]
					if (m2 >= 2) & (event.data2 > 0):
						print('OnMidiMsg - SESSION 01 (m2 >= 2) & (event.data')
						m = 0
						m2 = 0
					else:
						print('OnMidiMsg - SESSION 02 (m2 >= 2) & (event.data ELSEE')
						m = int(event.data2 > 0)
						if (BtnInfo[n].Flags & 1 != 0) & (m > 0) & device.isDoubleClick(event.data1) & ((self.ClipOfs >= -1) | (n != 2)):
							print('OnMidiMsg - SESSION BtnInfo[n].Flags & 1 != 0)')
							m += 1

					o = int(event.data2 > 0) * 2
					if n == Btn_Play:
						print('OnMidiMsg - SESSION n == Btn_Play')
						#transport.globalTransport(midi.FPT_Play, o, event.pmeFlags)
						device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x29, 0x02, 0x0C, 0x00, 0x02, 0x00, 0x00, 0xF7]))
						device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x29, 0x02, 0x0C, 0x00, 0xF7]))
					elif n == Btn_Stop:
						print('OnMidiMsg - SESSION n == Btn_Stop')
						transport.globalTransport(midi.FPT_Stop, o, event.pmeFlags)
					elif n == Btn_TapTempo:
						print('OnMidiMsg - SESSION n == Btn_TapTempo')
						transport.globalTransport(midi.FPT_TapTempo, o, event.pmeFlags)
					elif n == Btn_TempoNudgePlus:
						print('OnMidiMsg - SESSION n == Btn_TempoNudgePlus')
						transport.globalTransport(midi.FPT_NudgePlus, o, event.pmeFlags)
					elif n == Btn_TempoNudgeMin:
						print('OnMidiMsg - SESSION n == Btn_TempoNudgeMin')
						transport.globalTransport(midi.FPT_NudgeMinus, o, event.pmeFlags)
					if (m > 0) | (m2 <= 1):
						print('OnMidiMsg - SESSION 03 (m > 0) | (m2 <= 1)')
						self.SetBtn(n, m)
					if (n == 2) & (self.ClipOfs < -1) & (event.data2 > 0):
						print('OnMidiMsg - SESSION 04 (n == 2) & (self.ClipOfs < -1) & (event.data2 > 0)')
						launchMapPages.releaseMapItem(event, -self.ClipOfs - 2)
					return
			#system
			# track offset
			if (event.data1 == Btn_Up) | (event.data1 == Btn_Down):
				print('\nOnMidiMsg - track offset UP or DOWN')
				if (event.data1 == Btn_Up):
					print('OnMidiMsg - track Btn_Up')
					a = 0
				else:	
					print('OnMidiMsg - track Btn_Down')
					a = 1
				event.handled = True
				BlockPages = (self.BtnT[Btn_Overview] > 0) | self.BlockOfs
				m = 150 + int(BlockPages) * 350 # faster in 1-pad increments
				device.repeatMidiEvent(event, m, m)
				if (event.data2 > 0) & (event.pmeFlags & midi.PME_System != 0):
					print('OnMidiMsg - track event.data2 > 0) & (event.pmeFlags & midi.PME_System')
					m = a * 2 - 1
					if BlockPages:
						print('OnMidiMsg - track BlockPages')
						m = m * OverH
					self.SetOfs(self.TrackOfs + m, self.ClipOfs)
					self.BtnT[Btn_Overview] = int(self.BtnT[Btn_Overview] > 0) * 2 # so that session btn works as held
					if self.ClipOfs >= 0:
						print('OnMidiMsg - track self.ClipOfs >= 0')
						self.ClipOfsPerfomance = self.ClipOfs
					self.TrackOfsPerfomance = self.TrackOfs
				self.ArrowT[a] = event.data2
				self.CheckSpecialSwitches()
				playlist.lockDisplayZone(1 + a, event.data2 > 0)
				return

			# clip offset
			elif (event.data1 == Btn_Left) | (event.data1 == Btn_Right):
				print('\nOnMidiMsg - clipoofset L or R')
				a = event.data1 - Btn_Left
				event.handled = True
				BlockPages = (self.BtnT[Btn_Overview] > 0) | self.BlockOfs
				m = 150 + int(BlockPages) * 350 # faster in 1-pad increments
				device.repeatMidiEvent(event, m, m)
				if (event.data2 > 0) & (event.pmeFlags & midi.PME_System != 0):
					print('OnMidiMsg - clip data2 > 0')
					m = (a) * 2 - 1
					if self.ClipOfs >= 0:
						print('OnMidiMsg - clip clipOfs >= 0')
						if (self.ClipOfs == 0) & (m == -1):
							print('OnMidiMsg - clip self.ClipOfs == 0) & (m == -1 SWITCHED TO NEW PAGE')
							o = -1
						else:
							print('OnMidiMsg - clip elsezz')
							if BlockPages:
								print('OnMidiMsg - clip BlockPages')
								m = m * OverW
							o = max(self.ClipOfs + m, 0)
					else:
						print('OnMidiMsg - clip self.ClipOfs < 0')
						o = self.ClipOfs + m
					self.SetOfs(self.TrackOfs, o)
					self.BtnT[Btn_Overview] = int(self.BtnT[Btn_Overview] > 0) * 2 # so that session btn works as held
					self.TrackOfsPerfomance = self.TrackOfs
					if self.ClipOfs >= 0:
						print('OnMidiMsg - clip still ClipOfs >= 0')
						self.ClipOfsPerfomance = self.ClipOfs
					self.PrevClipOfs = self.ClipOfs
					if self.ClipOfs <= 0:
						print('OnMidiMsg - clip well ClipOfs <= 0')
						device.stopRepeatMidiEvent()
				self.ArrowT[2 + a] = event.data2
				
				self.ArrowT[3] = event.data2
				self.CheckSpecialSwitches()
				playlist.lockDisplayZone(1 + a, event.data2 > 0)
				return
			elif (event.data1 == Btn_Overview):  # overview
				print('\nOnMidiMsg - overview event.data1 == Btn_Overview)')
				event.handled = True
				if (event.pmeFlags & midi.PME_System != 0):
					if event.data2 > 0:
						print('OnMidiMsg - overview event.data2 > 0')
						self.SetBtn(Btn_Overview, int(self.BtnT[Btn_Overview] > 0) ^ 1)
					elif self.BtnT[Btn_Overview] == 2:
						print('OnMidiMsg - overview self.BtnT[Btn_Overview] == 2:')
						self.SetBtn(Btn_Overview, 0)
				return
			
			elif (event.data1 == Btn_CapMidi):  # Left/Right Column Toggle
				print('\nOnMidiMsg - column toggle LR event.data1 == Btn_CapMidi')
				# event.handled = True
				# if (event.pmeFlags & midi.PME_System != 0):
				# 	if event.data2 > 0:
				# 		if (self.LeftBtnColumnToggle):
				# 			for n in range(0, NumBtns):
				# 				BtnInfo[n].Num	= RightBtnInfo[n].Num
				# 			self.LeftBtnColumnToggle = False
				# 		else:
				# 			for n in range(0, NumBtns):
				# 				BtnInfo[n].Num	= LeftBtnInfo[n].Num
				# 			self.LeftBtnColumnToggle = True
				return
			elif (event.data1 == Btn_SpareHex): # spare state
				print('\nOnMidiMsg - spare st (event.data1 == Btn_SpareHex')
				event.handled = True
				if (event.pmeFlags & midi.PME_System != 0):
					print('OnMidiMsg - spare st (event.pmeFlags & midi.PME_System != 0)')
					if event.data2 > 0:
						print('OnMidiMsg - spare stevent.data2 > 0')
						self.SetBtn(Btn_Spare, int(event.data2 > 0))
				return
			
			elif ((event.data1 >= Btn_SpareHex) & (event.data1 <= 0x7F)) | (event.data1 in	[0x0A, 0x14, 0x1E, 0x28, 0x32, 0x3C, 0x46, 0x50]):
				print('\n----------------OnMidiMsg - elif ((event.data1 >= Btn_SpareHex) & (event.data1 <= ', 0x63 == Btn_SpareHex)
				return

			# live mode
			x = event.data1 - y * PadsStride - ClipsX
			y = ClipsH - ClipsY - y
			if (x >= PadsW) | (y >= PadsH):
				print('\nOnMidiMsg - Live x >= PadsW) | (y >= Pad')
				return

			# clip release safety
			if event.data2 == 0:
				print('OnMidiMsg - Clip release safely event.data2 == ')
				if self.BtnLastClip[y][x].TrackNum != MaxInt:
					print('OnMidiMsg - Clip release safely 00 BtnLastClip[y][x].TrackNum != MaxInt')
					if (event.pmeFlags & midi.PME_System_Safe != 0):
						print('OnMidiMsg - Clip release safely 001 pmeFlags & midi.PME_System_Safe != 0')
						playlist.triggerLiveClip(self.BtnLastClip[y][x].TrackNum, self.BtnLastClip[y][x].SubNum, self.BtnLastClip[y][x].Flags | midi.TLC_Release)
					if self.BtnLastClip[y][x].TrackNum == 0:
						print('OnMidiMsg - Clip release safely 002 elf.BtnLastClip[y][x].TrackNum == 0')
						self.BtnMap[SClipsY + y][SClipsX + x] = ColT[0]
						self.FullRefresh_Btn

					self.BtnLastClip[y][x].TrackNum = MaxInt
					event.handled = True
					return

			if self.BtnT[Btn_Overview] > 0:
				print('\nOnMidiMsg - Overview PICK self.BtnT[Btn_Overview] > 0')
				# overview pick
				if event.data2 > 0:
					if y < OverH - 1:
						if x >= OverW:
							self.SetOfs(self.TrackOfs, -y - 1)
						else:
							self.SetOfs(y * OverH, x * OverW)
					elif x < OverW:
						self.SetOfs(self.TrackOfs, -(x + 8) - 1)
				else:
					self.SetBtn(Btn_Overview, 0)
				event.handled = True
			else:
				print('\nOnMidiMsg - Overview PICK else')
				if self.ClipOfs < -1:
					print('OnMidiMsg - Overview PICK else - custom pg')
					# custom pages
					x2 = y * LayW + x
					m = -self.ClipOfs - 2
					if x2 <= launchMapPages.getMapCount(m):
						print('OnMidiMsg - Overview PICK x2<= launchmappages')
						o = launchMapPages.getMapItemChannel(m, x2)
						if o > -128:
							print('OnMidiMsg - Overview PICK else > -128')
							m2 = event.data2
							if (m2 == 0) & (self.BtnT[Btn_ScenePlus] > 0):
								print('OnMidiMsg - Overview PICK m2 === 0 & Btn_sceneplus')
								m2 = -MaxInt # user1=hold
							launchMapPages.processMapItem(event, m, x2, m2)
				else:
					print('OnMidiMsg - Overview PICK else NOT custom pg')
					if self.ClipOfs >= 0:
						print('OnMidiMsg - Overview PICK else 1st change')
						# first chance
						launchMapPages.processMapItem(event, -1, y * PadsW + x, event.data2)
						self.ClipOfsPerfomance = self.ClipOfs
						if event.handled:
							print('OnMidiMsg - Overview PICK else handled')
							return

					if (event.pmeFlags & midi.PME_System_Safe != 0):
						print('OnMidiMsg - Overview PICK else event.pmeFlags & midi.PME_System_Safe != 0)')
						x2 = x
						y2 = y + self.TrackOfs + 1
						if self.ClipOfs >= 0:
							if event.data2 > 0:
								print('OnMidiMsg - Overview PICK else lunch clip')
								# clip launch
								m = midi.TLC_MuteOthers | midi.TLC_Fill
								if y >= SceneY:
									print('OnMidiMsg - Overview PICK else scene Y')
									y2 = 0
									m = m | midi.TLC_ColumnMode # column mode

								if x2 >= SClipsW:
									x2 = -1
								else:
									x2 += self.ClipOfs
								m = midi.TLC_MuteOthers | midi.TLC_Fill
								if self.BtnT[Btn_Queue] > 0:
									m = m | midi.TLC_Queue
								if self.BtnT[Btn_Snap] > 0:
									m = m | TLC_GlobalSnap # snap
								if self.BtnT[Btn_ScenePlus] | (self.BtnT[Btn_Scene] > 0):
									m = m | midi.TLC_ColumnMode # column mode
									if self.BtnT[Btn_ScenePlus] == 0:
										m = m | midi.TLC_WeakColumnMode # weak
									elif self.BtnT[Btn_Scene] > 0:
										m = m | midi.TLC_TriggerCheckColumnMode # trigger-check

								if (self.BtnT[Btn_VelLock] > 0):
									playlist.triggerLiveClip(y2, x2, m)
								else:
									playlist.triggerLiveClip(y2, x2, m, event.data2 * (1 / 127))

								self.BtnLastClip[y][x].TrackNum = y2
								self.BtnLastClip[y][x].SubNum = x2
								self.BtnLastClip[y][x].Flags = m
						elif event.data2 > 0:
							# track properties
							if (x2 == 2) | (x2 == 3):
								playlist.incLivePosSnap(y2, (x2 - 2) * 2 - 1)
							elif (x2 == 4) | (x2 == 5):
								playlist.incLiveTrigSnap(y2, (x2 - 4) * 2 - 1)
							elif (x2 == 6) | (x2 == 7):
								playlist.incLiveLoopMode(y2, (x2 - 6) * 2 - 1)
							elif x2 == 8        :
								playlist.incLiveTrigMode(y2, 1)

							playlist.refreshLiveClips()
						event.handled = True
			self.PrevClipOfs = self.ClipOfs
		else:
			event.handled = False

	def OnMidiOutMsg(self, event):
		print('\n\nOnMidiOutMsg func')

		print (event.status, event.data1, event.data2)
		event.handled = True
		ID = event.midiId
		n = 0
		if (ID == midi.MIDI_NOTEOFF) | (ID == midi.MIDI_NOTEON):
			NoteNum = event.note
			if ID == midi.MIDI_NOTEOFF:
				Velocity = 0
			else:
				Velocity = event.velocity

			if NoteNum >= 125:
				if NoteNum == 125:
					if ID == midi.MIDI_NOTEON:
						self.ScreenCapZoom = 1 + (Velocity >> 1)
				else:
					if NoteNum == 126:
						if ID == midi.MIDI_NOTEON:
							self.BtnMapModeRefCount += 1
							if self.BtnMapModeRefCount == 1:
								device.fullRefresh()
						else:
							self.BtnMapModeRefCount -= 1
							if self.BtnMapModeRefCount == 0:
								device.fullRefresh()
					elif ID == midi.MIDI_NOTEON:
						m = Velocity >> 5
						if self.BtnMapMode != m:
							if m >= 3:
								self.ScreenCapTime = time.time()
							self.BtnMapMode = m
							device.fullRefresh()
			else:
				# change pad
				Chan = event.midiChan
				if Chan < 3:
					if (Chan > 0) & (ID == midi.MIDI_NOTEOFF):
						return

				o, n = utils.DivModU(NoteNum, 12)
				if o < PadsH:
					o = PadsH - 1 - o

				if utils.InterNoSwap(o, 0, PadsH) & utils.InterNoSwap(n, 0, PadsW - 1) & ((o < PadsH) | (n < PadsW - 1)): #light shouldn't be touched'
					r, g, b = utils.ColorToRGB(self.AnimBtnMap[o][n])
					if Chan == 0:
						r = Velocity
					elif Chan == 1:
						g = Velocity
					else:
						b = Velocity
					self.AnimBtnMap[o][n] = utils.RGBToColor(r, g, b)
					self.FullRefresh_Anim()

		elif ID != midi.MIDI_CONTROLCHANGE:
			event.handled = False

	def OnDoFullRefresh(self):
		# print('\n\nOnDoFullRefresh func')
		TempBtnMap = [[0 for x in range(PadsW)] for y in range(PadsH + 1)]
		TempAnimBtnMap = [[0 for x in range(PadsW)] for y in range(PadsH + 1)]

		if (self.CurLayout == 3) & device.isAssigned():
			TempBtnMapMode = self.BtnMapMode

			if TempBtnMapMode >= 3:
				for y in range(0, PadsH):
					for x in range(0, PadsW):
						TempBtnMap[y][x] = self.BtnMap[y][x]
				TempBtnMap[0][PadsW - 1] = self.BtnMap[0][PadsW - 1] # bottom light
			else:
				if TempBtnMapMode < 2:
					if self.BtnMapModeRefCount == 0:
						for y in range(0, PadsH):
							for x in range(0, PadsW):
								TempBtnMap[y][x] = self.BtnMap[y][x]
					else:
						TempBtnMapMode = 2
						TempBtnMap[0][PadsW - 1] = self.BtnMap[0][PadsW - 1] # bottom light

				if TempBtnMapMode > 0:
					for y in range(0, PadsH):
						for x in range(0, PadsW):
							TempAnimBtnMap[y][x] = self.AnimBtnMap[y][x]

				# adapt anim map
				if TempBtnMapMode > 0:
					for y in range(0, PadsH):
						for x in range(0, PadsW):
							r, g, b = utils.ColorToRGB(TempAnimBtnMap[y, x])
							c = utils.HLSToRGB(g * Div127, r * Div127, b * Div127)
							c = self.FixColor(c)
							if (TempBtnMapMode >= 2) | (c > 0):
								TempBtnMap[y][ x] = c

			# update blinking
			for y in range(0, PadsH):
				for x in range(0, PadsW):
					o = TempBtnMap[y][x]
					if o & LPBlinkMask != 0:
						TempBtnMap[y][x] = utils.FadeColor(o, BlinkColT[min(o >> LPBlinkShift, 3)][0], self.BlinkLight)

			# build SysEx
			t = (0x030C02292000F0).to_bytes(8 + 5 * MaxPads, byteorder='little')
			s = bytearray(t)
			m = 7

			for y in range(0, PadsH):
				y2 = y * 10
				for x in range(0, PadsW):
					p = 90 - y2 + x
					# add to the list
					if (TempBtnMap[y][x] != self.OldBtnMap[y][x]) & (not (p in ForbiddenPads)):
						s[m] = 3
						s[m + 1] = 90 - y2 + x
						s[m + 2], s[m + 3], s[m + 4] = utils.ColorToRGB(TempBtnMap[y][x])
						m += 5

			# send it
			if m > 8:
				s[m] = 0xF7
				s = s[: m + 1]
				device.midiOutSysex(bytes(s))
				'''
				sf = ''
				for y in range(7, len(s)):
					sf = sf + str(s[y]) + ', '
					if (y - 6) % 5 == 0:
						print(sf)
						sf = ''
				print('---------------------')
				'''

			# backup
			for y in range(0, PadsH):
				for x in range(0, PadsW):
					self.OldBtnMap[y][x] = TempBtnMap[y][x]

	def FullRefresh_Btn(self):
		# print('\n\nFullRefresh_Btn func')
		if (self.BtnMapMode < 2) & (self.BtnMapModeRefCount == 0):
			device.fullRefresh()

	def FullRefresh_Anim(self):
		print('\n\nFullRefresh_Anim func')
		if ((self.BtnMapMode > 0) & (self.BtnMapMode < 3)) | (self.BtnMapModeRefCount != 0):
			device.fullRefresh()

	def SetOfs(self, SetTrackOfs, SetClipOfs):
		print('\n\nSetOfs func')
		Col1 = 0x010900
		Col2 = 0x090100


		self.TrackOfs = utils.Limited(SetTrackOfs, 0, playlist.trackCount() - PadsH)
		self.ClipOfs = utils.Limited(SetClipOfs, -launchMapPages.length() - 1, 0x10000)
		if device.isAssigned():
			# page buttons
			o = self.TrackOfs + 4
			v = utils.Limited(o, 0, 256)
			self.BtnMap[1][0] = utils.FadeColor(Col2, Col1, v)
			self.BtnMap[2][0] = utils.FadeColor(Col1, Col2, v)

			o = abs(self.ClipOfs) * 4
			if self.ClipOfs < 0:
				o = o * 4
			v = utils.Limited(o, 0, 256)
			self.BtnMap[0][1] = utils.FadeColor(Col2, Col1, v)
			self.BtnMap[0][2] = utils.FadeColor(Col1, Col2, v)

			if self.ClipOfs < -1:
				launchMapPages.updateMap(-self.ClipOfs - 2)
			else:
				launchMapPages.checkMapForHiddenItem()
			self.OnUpdateLiveMode(playlist.trackCount())			

		if playlist.getDisplayZone() != 0:
			self.OnDisplayZone()

	def OnDisplayZone(self):
		print('\n\nOnDisplayZone func')
		if (self.ClipOfs >= 0) & (playlist.getDisplayZone() != 0):
			playlist.liveDisplayZone(self.ClipOfs, self.TrackOfs + 1, self.ClipOfs + PadsW - 1, self.TrackOfs + 1 + PadsH)
		else:
			playlist.liveDisplayZone(-1, -1, -1, -1)

	def CheckSpecialSwitches(self):
		print('CheckSpecialSwitches func')
		if (self.ArrowT[0] + self.ArrowT[1] + self.ArrowT[2] + self.ArrowT[3]) >= 0x7F * 4:
			self.BlockOfs = not self.BlockOfs
			self.SetOfs(0, 0)
			device.stopRepeatMidiEvent()

	def SetBtn(self, Index, Value):
		print('\n\nSetBtn func')
		self.BtnT[Index] = Value

		v = BtnInfo[Index].Col[utils.Limited(Value, 0, 2)]
		if v != -1:
			y, x = BtnInfo[Index].GetYX()
			self.BtnMap[y][x] = v
			self.FullRefresh_Btn()

		if Index > Btn_Overview:
			if Index == Btn_Spare:
				if Value > 0:
					utils.SwapInt(self.TrackOfs, self.TrackOfs_Spare)
					utils.SwapInt(self.ClipOfs, self.ClipOfs_Spare)
					self.SetOfs(self.TrackOfs, self.ClipOfs)

				self.SetBtn(Btn_Overview, Value)
		else:
			#overview
			self.OnUpdateLiveMode(playlist.trackCount())
			device.stopRepeatMidiEvent() #  in case arrows were held
			playlist.lockDisplayZone(0, Value > 0)
		
	def OnIdle(self):
		# print('\n\nOnIdle func')
		BlinkSpeed = 0x20

		if device.isAssigned():
			# beat cycle (smooth fade)
			if transport.isPlaying() != midi.PM_Playing:
				v2 = math.sin((time.time() % BlinkSpeed) * math.pi / BlinkSpeed)
			else:
				v2 = mixer.getSongTickPos(midi.ST_Beat)
				v2 = math.sin(v2 * (math.pi / 2))

			v3 = mixer.getSongTickPos(midi.ST_PGB)
			v3 = 1 - v3
			c = utils.FadeColor(0x003F30, 0x000138, round(v3 * v3 * 256))

			# activity meters
			if (self.ClipOfs == -1) & (self.BtnT[Btn_Overview] == 0):
				for y in range(0, SClipsH):
					m = self.TrackOfs + y + 1
					v3 = playlist.getTrackActivityLevelVis(m) * 2
					for x in range(SClipsX, SClipsX + 2):
						self.BtnMap[SClipsY + y][ x] = utils.FadeColor(0x3F303F, 0x000000, utils.Limited(round(v3 * 256), 0, 256))
						v3 = v3 - 1

			if not self.NoFullRefresh:
				if self.BtnMapMode == 3:
					print('time to full refr')
					self.FullRefresh_Btn()

				self.BlinkLight = round(v2 * v2 * 256)
				if (self.BtnMap[0][3] != c) | (self.BtnMap[0][PadsW - 1] != c):
					y, x = BtnInfo[Btn_Play].GetYX()
					self.BtnMap[y][x] = c
					self.BtnMap[0][PadsW - 1] = c
					self.FullRefresh_Btn()
				else:
					self.UpdateBlinking()
													
				for x in range(0, 9):
					if (self.BtnMap[0][x] != c):
						self.BtnMap[0][x] = c
						self.FullRefresh_Btn()
					else:
						self.UpdateBlinking()

	def OnRefresh(self, flags):
		# print('\n\nOnRefresh func')
		if flags & midi.HW_Dirty_RemoteLinks != 0:
			if self.ClipOfs < -1:
				self.SetOfs(self.TrackOfs, self.ClipOfs)
			launchMapPages.updateMap(-1)

	def SwitchLedsOff(self):
		print('\n\nSwitchLedsOff func')
		t = (0x030C02292000F0).to_bytes(7 + 3 * MaxPads, byteorder='little')
		s = bytearray(t)
		m = 7
		for y in range(0, PadsH):
			y2 = y * 10
			for x in range(0, PadsW):
				p = 90 - y2 + x
				ForbiddenPads = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90]
				if (not (p in ForbiddenPads)):
					s[m] = 0
					s[m + 1] = y2 + x
					s[m + 2] = 0
					m += 3
		s[m] = 0xF7
		s = s[: m + 1]
		device.midiOutSysex(bytes(s))

	def OnSysEx(self, event):
		print('\n\nOnSysEx func')
		print('onSysex', event.sysex, event.senderId)


	def OnInit(self):
		print('\n\nOnInit func')
		NameStr = 'Novation Launchpad X'

		for n in range(0, len(self.ColScaleT)):
			v = n / 255
			self.ColScaleT[n] = min(round(v * v * v * 255 * 0.9), 63)

		# init mapping
		launchMapPages.createOverlayMap(1, 8, LayW, LayH)

		for y in range(0, LayH):
			for x in range(0, LayW):
					launchMapPages.setMapItemTarget(-1, y * LayW + x, y * PadsStride + x + 1)

		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))
			# set programmer mode
			device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x29, 0x02, 0x0C, 0x0E, 0x01, 0xF7]))
			# switch off all LEDs
			self.SwitchLedsOff()
			self.CurLayout = 3

		# load mapping
		launchMapPages.init(NameStr, LayW, LayH)

		self.Reset()
		device.createRefreshThread()
		for n in range(1, len(self.BtnT)):
			self.SetBtn(n, self.BtnT[n])
		self.OnUpdateLiveMode(playlist.trackCount())
		self.SetOfs(self.TrackOfs, self.ClipOfs)

	def OnDeInit(self):
		print('\n\nOnDeInit func')
		device.destroyRefreshThread()
		self.Reset()

		if device.isAssigned():
			if self.CurLayout == 3:
				self.SwitchLedsOff()
			# set b   ack to live mode
			device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x29, 0x02, 0x0C, 0x0E, 0x00, 0xF7]))

	def FixColor(self, Color):
		print('\n\nFixColor func')
		r, g, b = utils.ColorToRGB(Color)
		r = self.ColScaleT[r]
		g = self.ColScaleT[g]
		b = self.ColScaleT[b]
		#r = round((r / 256) * 127)
		#g = round((g / 256) * 127)
		#b = round((b / 256) * 127)
		return utils.RGBToColor(r, g, b)

	def OnUpdateLiveMode(self, LastTrackNum):
		print('\n\nOnUpdateLiveMode func')
		FirstTrackNum = 1
		StatusColT = [0, 0, 0, 0]
		LoopBtnColT = (0x3F0000, 0x002400, 0x000110, 0x000228, 0x00033F, 0x180018, 0x3F003F)
		TrigColT = (0x001000, 0x280800, 0x200018, 0x202020)
		SnapColT = (0x000420, 0x180000, 0x3F0000, 0x300808, 0x201010, 0x101818, 0x002020)
		OverviewColT = ((0x000000, 0x200000, 0x4200000), (0x000110, 0x00063F, 0x400063F))
		OnLight = 0x48
		OffLight = -0x60 #-0x1A
		R = utils.TRect(0, 0, 0, 0)
		R2 = utils.TRect(0, 0, 0, 0)

		if device.isAssigned():
			if (self.ClipOfs >= -1) | (self.BtnT[Btn_Overview] > 0):
				if self.BtnT[Btn_Overview] > 0:
					# overview
					R2.Left = self.ClipOfs
					if R2.Left < 0:
						R2.Left -= 128
					R2.Right = R2.Left + SClipsW - 1
					R2.Top = 1 + self.TrackOfs
					R2.Bottom = R2.Top + SClipsH - 1
					for y in range(0, OverH + 1):
						for x in range(0, OverW + 1):
							v = OverviewColT[0][0]
							if (x < OverW) & (y < OverH):
								R.Left = x * SClipsW
								R.Right = R.Left + SClipsW - 1
								R.Top = 1 + y * SClipsH
								R.Bottom = R.Top + SClipsH - 1
								o = patterns.getBlockSetStatus(R.Left, R.Top, R.Right, R.Bottom)
								v = OverviewColT[utils.RectOverlapEqual(R, R2)][o]
							elif (x == SClipsW) & (y < SClipsH):
								v = OverviewColT[y == (-1 - self.ClipOfs)][int(y <= launchMapPages.length())]
							elif (y == SClipsH) & (x < SClipsW):
								v = OverviewColT[x + 8 == (-1 - self.ClipOfs)][int(x + 8 <= launchMapPages.length())]
							self.BtnMap[OverY + y][OverX + x] = v
				else:
					# scene buttons
					y = SClipsH + 1
					for x in range(0, ClipsW):
						v = launchMapPages.getMapItemColor(-1,(y - 1) * ClipsW + x)
						if v < 0:
							v = 0x010000
						else:
							v = self.FixColor(v)
						self.BtnMap[SClipsY + y - 1][SClipsX + x] = v


					Ofs = self.TrackOfs
					for y in range(max(FirstTrackNum - Ofs, 1), min(LastTrackNum - Ofs, SClipsH) + 1):  #todo
						StatusColT[2] = TrigColT[playlist.getLiveTriggerMode(y + Ofs)]

						if self.ClipOfs >= 0:
							# clips
							for x in range(0, ClipsW):
								v = launchMapPages.getMapItemColor(-1, (y - 1) * ClipsW + x)
								if v < 0:
									if x < SClipsW:
										m = self.ClipOfs + x
										o = playlist.getLiveBlockStatus(y + Ofs, m, midi.LB_Status_Simple)
										if o == 0:
											v = 0
										else:
											v = playlist.getLiveBlockColor(y + Ofs, m)
											if o > 1:
												v = utils.LightenColor(v, OnLight)
											else:
												v = utils.LightenColor(v, OffLight)

											v = self.FixColor(v)
										if o == 2:
											v = v | LPBlink1
									else:
										o = playlist.getLiveStatus(y + Ofs, midi.LB_Status_Simple)
										if o == 0:
											v = 0
										else:
											v = playlist.getLiveBlockColor(y + Ofs, -1)
											if o == 2:
												v = utils.LightenColor(v, 0x20)
											elif o > 1:
												v = utils.LightenColor(v, OnLight)
											else:
												v = utils.LightenColor(v, OffLight)

											v = self.FixColor(v)
								else:
									v = self.FixColor(v)
								self.BtnMap[SClipsY + y - 1][SClipsX + x] = v
						else:
							# track properties
							v = 0
							for x in range(0, ClipsW):
								if (x == 2) | (x == 3):
									v = SnapColT[min(playlist.getLivePosSnap(y + Ofs), len(SnapColT))-1]
								elif (x == 4) | (x == 5):
									v = SnapColT[min(playlist.getLiveTrigSnap(y + Ofs), len(SnapColT))-1]
								elif (x == 6) | (x == 7):
									v = LoopBtnColT[playlist.getLiveLoopMode(y + Ofs)]
								elif x == 8:
									v = StatusColT[2]
								else:
									continue
								self.BtnMap[SClipsY + y - 1][SClipsX + x] = v
								

							self.NoFullRefresh = True
							self.OnIdle() # activity meters
							self.NoFullRefresh = False
			else:
				#custom pages
				for y in range(0, LayH):
					for x in range(0, LayW):
						self.BtnMap[LayY + y][LayX + x] = self.FixColor(launchMapPages.getMapItemColor(-self.ClipOfs - 2, y * LayW + x))

			self.FullRefresh_Btn()

LaunchPadPro = TLaunchPadPro()

def OnInit():
	print('initoo')
	LaunchPadPro.OnInit()

def OnDeInit():
	print('deinitoo')
	LaunchPadPro.OnDeInit()

def OnMidiMsg(event):
	print('midi in msg')
	LaunchPadPro.OnMidiMsg(event)

def OnMidiOutMsg(event):
	print('midi o msg')
	LaunchPadPro.OnMidiOutMsg(event)

def OnDoFullRefresh():
	# print('full refr')
	LaunchPadPro.OnDoFullRefresh()

def OnDisplayZone():
	print('displ zon')
	LaunchPadPro.OnDisplayZone()

def OnIdle():
	# print('idle')
	LaunchPadPro.OnIdle()

def OnRefresh(Flags):
	print('refr')
	LaunchPadPro.OnRefresh(Flags)

def OnUpdateLiveMode(LastTrackNum):
	print('up  live')
	LaunchPadPro.OnUpdateLiveMode(LastTrackNum)

def OnMidiIn(event):
	print('\n\nBEGIN-----')
	data = event.data1
	print('presssed w data1:', data, '  -->', hex(data))
	if data  == Btn_Up:
		print('presssed Btn_Up')
	elif data == Btn_Down:
		print('presssed Btn_Down')
	elif data == Btn_Left:
		print('presssed Btn_Left')
	elif data == Btn_Right:
		print('presssed Btn_Right')
	elif data == Btn_Session:
		print('presssed Btn_Session')
	elif data == Btn_Note:
		print('presssed Btn_Note')
	elif data == Btn_Custom:
		print('presssed Btn_Custom')
	elif data == Btn_CapMidi:
		print('presssed Btn_CapMidi')
	elif data == Btn_SpareHex:
		print('presssed Btn_SpareHex')
	elif data == Btn_Volume:
		print('presssed Btn_Volume')
	elif data == Btn_Pan:
		print('presssed Btn_Pan')
	elif data == Btn_SendA:
		print('presssed Btn_Btn_SendA')
	elif data == Btn_SendB:
		print('presssed Btn_SendB')
	elif data == Btn_StopClip:
		print('presssed Btn_StopClip')
	elif data == Btn_Mute:
		print('presssed Btn_Mute')
	elif data == Btn_Solo:
		print('presssed Btn_Solo')
	elif data == Btn_RecordArm:
		print('presssed Btn_RecordArm')
	# print('getting midiooo:',event)
	# print('controlNum:',event.controlNum)
	# print('controlVal:',event.controlVal)
	# print('data1:',event.data1)
	# print('data2:',event.data2)
	# print('handled:',event.handled)
	# print('inEv:',event.inEv)
	# print('isIncrement:',event.isIncrement)
	# print('midiChan:',event.midiChan)
	# print('midiChanEx:',event.midiChanEx)
	# print('midiId:',event.midiId)
	# print('note:',event.note)
	# print('outEv:',event.outEv)
	# print('pitchBend:',event.pitchBend)
	# print('pmeFlags:',event.pmeFlags)
	# print('port:',event.port)
	# print('pressure:',event.pressure)
	# print('progNum:',event.progNum)
	# print('res:',event.res)
	# print('senderId:',event.senderId)
	# print('status:',event.status)
	# print('sysex:',event.sysex)
	# print('timestamp:',event.timestamp)
	# print('velocity:',event.velocity)
	# print('write:',event.write)
	
	LaunchPadPro.OnMidiIn(event)
	print('END-----\n')

def OnSysEx(event):
	print('syeEX')
	LaunchPadPro.OnSysEx(event)



