from midi_controller import MidiController, Note, Control, ControlValue, Color, Invert
from serial_hamlib import SerialHamlib
from enum import Enum

from mode_conversion import ConvertZZAC_Step_2_P1, ConvertZZAC_P1_2_Step

class DisplayMethod(Enum):
    ARTIST_TITLE = 0
    ARTIST = 1
    TITLE = 2
    ALBUM = 3

    def next(self):
        return DisplayMethod((self.value + 1) % 4)


class EventHandler:
    _display_mode = DisplayMethod.ARTIST_TITLE
    _display_scroll = 0

    _player_color_map = {
        'spotify': Color.GREEN,
        'chrome': Color.YELLOW,
        'rhythmbox': Color.CYAN,
    }

    def __init__(self, controller: MidiController, serial: SerialHamlib) -> None:
        self._controller = controller
        self._serial = serial
        self._midi_in_port = None

    def setup(self):
        self._midi_in_port = self._controller.open_input(self.handle_midi_message)

    def read_quisk_and_set_surface(self):
        f = self._serial.get_frequency()

        b = self._serial.get_band()
        # map f 2 note buttom
        nb = Note.BAND_20
        self._controller.note_on(nb, 127)

        ag = self._serial.get_audio_gain()
        self._controller.control_change(Control.FADER, int(ag*127/100))

        print('f= ', f, ' b= ', b, ' ag= ', ag)

    def stop(self):
        if self._midi_in_port is not None:
            self._midi_in_port.close()

    def update_display(self) -> None:
        pass

    def handle_midi_message(self, message) -> None:
        if message.type == 'note_on' and message.velocity != 0:
            print(message.note, ' ### ')
            if message.note == 34:
                print(self._serial.get_frequency())
                print(self._serial.get_audio_gain())
                print(self._serial.get_band())

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
                print(ConvertZZAC_P1_2_Step.get(stepsize))
                self._serial.set_stepsize(stepsize)

            if message.note == Note.TUNE_STEP_DOWN.value:
                # band --
                stepsize = (self._serial.get_stepsize() - 1) % 15
                print(ConvertZZAC_P1_2_Step.get(stepsize))
                self._serial.set_stepsize(stepsize)

            if message.note == Note.BAND_80.value:
                self._serial.set_band(80)
            if message.note == Note.BAND_60.value:
                self._serial.set_band(60)
            if message.note == Note.BAND_40.value:
                self._serial.set_band(40)
            if message.note == Note.BAND_30.value:
                self._serial.set_band(30)
            if message.note == Note.BAND_20.value:
                self._serial.set_band(20)
            if message.note == Note.BAND_15.value:
                self._serial.set_band(15)
            if message.note == Note.BAND_12.value:
                self._serial.set_band(12)
            if message.note == Note.BAND_10.value:
                self._serial.set_band(10)

            if message.note == 30:
                bbbb = self._serial.get_band()
                print(bbbb)

            if message.note == 32:
                print(self._serial.get_stepsize())

        if message.type == 'note_on' and message.velocity == 0:
            #print(message.note)
            pass

        if message.type == 'control_change':
            print(message.control, ' ### ', message.value)
            if message.control == Control.WHEEL.value:
                if message.value == ControlValue.LEFT.value:
                    self._serial.step_down()
                if message.value == ControlValue.RIGHT.value:
                    self._serial.step_up()
            if message.control == Control.FADER.value:
                # TODO remove magic number
                self._serial.set_audio_gain(int(message.value/127*100))

