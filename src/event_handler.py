from midi_controller import MidiController, Note, Control, ControlValue, Color, Invert
from serial_hamlib import SerialHamlib
from enum import Enum

from mode_conversion import ConvertZZAC_Step_2_P1, ConvertZZAC_P1_2_Step
from midi_controller import Convert_BandNote_2_Value, Convert_Value_2_BandNote

MIDI_DEBUG = 1

class EventHandler:

    def __init__(self, controller: MidiController, serial: SerialHamlib) -> None:
        self._controller = controller
        self._serial = serial
        self._midi_in_port = None

    def setup(self):
        self._midi_in_port = self._controller.open_input(self.handle_midi_message)

    def reset_band_buttoms(self):
        for i in Convert_BandNote_2_Value:
            if i.value != 256:
                self._controller.note_on(i, 0)

    def reset_mode_buttoms(self):
        modes = [Note.MODE_CW, Note.MODE_SSB, Note.MODE_AM, Note.MODE_FM]
        for i in modes:
            self._controller.note_on(i, 0)

    def read_quisk_and_set_surface(self):
        f = self._serial.get_frequency()

        # gate band and map band to note buttom
        b = self._serial.get_band()
        self._controller.note_on(Convert_Value_2_BandNote.get(b), 127)

        ag = self._serial.get_audio_gain()
        self._controller.control_change(Control.FADER, int(ag*127/100))

        mode = self._serial.get_mode()
        if mode == 0 or mode == 1:
            self._controller.note_on(Note.MODE_SSB, 127)
        if mode == 3 or mode == 4:
            self._controller.note_on(Note.MODE_CW, 127)
        if mode == 5:
            self._controller.note_on(Note.MODE_FM, 127)
        if mode == 6:
            self._controller.note_on(Note.MODE_AM, 127)

        if MIDI_DEBUG: print('f= ', f, ' b= ', b, ' ag= ', ag, ' mode= ', mode)

    def stop(self):
        if self._midi_in_port is not None:
            self._midi_in_port.close()

    def update_display(self) -> None:
        pass

    def handle_midi_message(self, message) -> None:
        if message.type == 'note_on' and message.velocity != 0:
            if MIDI_DEBUG: print(message.note, ' ### ')

            if message.note == 34:
                print(self._serial.get_frequency())
                print(self._serial.get_audio_gain())
                print(self._serial.get_band())

            if message.note == Note.MODE_SSB.value:
                self.reset_mode_buttoms()
                self._controller.note_on(Note.MODE_SSB, 127)
                if self._serial.get_band() > 30:
                    self._serial.set_mode(0)
                else:
                    self._serial.set_mode(1)

            if message.note == Note.MODE_CW.value:
                self.reset_mode_buttoms()
                self._controller.note_on(Note.MODE_CW, 127)
                if self._serial.get_band() > 30:
                    self._serial.set_mode(3)
                else:
                    self._serial.set_mode(4)

            if message.note == Note.MODE_FM.value:
                self.reset_mode_buttoms()
                self._controller.note_on(Note.MODE_FM, 127)
                self._serial.set_mode(5)

            if message.note == Note.MODE_AM.value:
                self.reset_mode_buttoms()
                self._controller.note_on(Note.MODE_AM, 127)
                self._serial.set_mode(6)

            if message.note == Note.MOX.value:
                if self._serial.get_mox_status() == 0:
                    self._controller.note_on(Note.MOX, 127)
                    self._serial.set_mox_status(1)
                elif self._serial.get_mox_status() == 1:
                    self._controller.note_on(Note.MOX, 0)
                    self._serial.set_mox_status(0)

            if message.note == Note.TUNE_STEP_UP.value:
                #  band ++
                stepsize = (self._serial.get_stepsize() + 1) % 15
                if MIDI_DEBUG: print(ConvertZZAC_P1_2_Step.get(stepsize))
                self._serial.set_stepsize(stepsize)

            if message.note == Note.TUNE_STEP_DOWN.value:
                # band --
                stepsize = (self._serial.get_stepsize() - 1) % 15
                if MIDI_DEBUG: print(ConvertZZAC_P1_2_Step.get(stepsize))
                self._serial.set_stepsize(stepsize)

            if message.note == Note.BAND_80.value:
                self._serial.set_band(80)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_80, 127)
            if message.note == Note.BAND_60.value:
                self._serial.set_band(60)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_60, 127)
            if message.note == Note.BAND_40.value:
                self._serial.set_band(40)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_40, 127)
            if message.note == Note.BAND_30.value:
                self._serial.set_band(30)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_30, 127)
            if message.note == Note.BAND_20.value:
                self._serial.set_band(20)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_20, 127)
            if message.note == Note.BAND_15.value:
                self._serial.set_band(15)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_15, 127)
            if message.note == Note.BAND_12.value:
                self._serial.set_band(12)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_12, 127)
            if message.note == Note.BAND_10.value:
                self._serial.set_band(10)
                self.reset_band_buttoms()
                self._controller.note_on(Note.BAND_10, 127)

            if message.note == 30:
                bbbb = self._serial.get_band()
                print(bbbb)

            if message.note == 32:
                print(self._serial.get_stepsize())

        if message.type == 'note_on' and message.velocity == 0:
            #print(message.note)
            pass

        if message.type == 'control_change':
            if MIDI_DEBUG: print(message.control, ' ### ', message.value)
            if message.control == Control.WHEEL.value:
                if message.value == ControlValue.LEFT.value:
                    self._serial.step_down()
                if message.value == ControlValue.RIGHT.value:
                    self._serial.step_up()
            if message.control == Control.FADER.value:
                # TODO remove magic number
                self._serial.set_audio_gain(int(message.value/127*100))

