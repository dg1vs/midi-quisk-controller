import mido
from lcd_7bit_font import lcd_7bit_render
from unidecode import unidecode
from typing import List
from enum import Enum


class Control(Enum):
    FADER = 70
    LED_RING = 80
    WHEEL = 88
    LED_METER = 90


class ControlValue(Enum):
    LEFT = 1
    RIGHT = 65
    # FADER = 70 # TODO check this value


class Note(Enum):
    LED_KNOB = 0
    MODE_CW = 3
    MODE_SSB = 4
    MODE_AM = 5
    MODE_FM = 6
    BAND_160 = 256  # 256 means nor used
    BAND_80 = 13
    BAND_60 = 256
    BAND_40 = 14
    BAND_30 = 15
    BAND_20 = 16
    BAND_17 = 256
    BAND_15 = 17
    BAND_12 = 18
    BAND_10 = 19
    MOX = 29
    TUNE_STEP_DOWN = 31
    TUNE_STEP_UP = 33
    FADER = 110



Convert_BandNote_2_Value = {Note.BAND_160: 160,
                            Note.BAND_80:   80,
                            Note.BAND_60:   60,
                            Note.BAND_40:   40,
                            Note.BAND_30:   30,
                            Note.BAND_20:   20,
                            Note.BAND_17:   17,
                            Note.BAND_15:   15,
                            Note.BAND_12:   12,
                            Note.BAND_10:   10}

Convert_Value_2_BandNote = {160: Note.BAND_160,
                             80: Note.BAND_80,
                             60: Note.BAND_60,
                             40: Note.BAND_40,
                             30: Note.BAND_30,
                             20: Note.BAND_20,
                             17: Note.BAND_17,
                             15: Note.BAND_15,
                             12: Note.BAND_12,
                             10: Note.BAND_10}

class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


class Invert(Enum):
    NONE = 0
    TOP = 1
    BOTTOM = 2
    BOTH = 3


class MidiController:
    def __init__(self, name: str) -> None:
        self._name = self.find_midi_input(name)
        self._port_out = mido.open_output(self._name)

    @staticmethod
    def find_midi_input(name) -> str:
        for input_name in mido.get_input_names():
            if input_name.startswith(name):
                return input_name

        raise Exception('No input found with name %s' % name)

    def open_input(self, callback: callable):
        return mido.open_input(self._name, callback=callback)

    def reset(self) -> None:
        for n in range(1, 35):
            self._send(mido.Message('note_on', note=n, velocity=0))

        self.control_change(Control.LED_RING, 64)
        self.control_change(Control.LED_METER, 0)

        self.sysex(self.create_segment_display_data('  HiQSDR'))
        self.sysex(self.create_lcd_display_data('HiQSDR'))

    def note_on(self, note: Note, velocity: int) -> None:
        self._send(mido.Message('note_on', note=note.value, velocity=velocity))

    def note_off(self, note: Note, velocity: int) -> None:
        self._send(mido.Message('note_off', note=note.value, velocity=velocity))

    def control_change(self, control: Control, value: int) -> None:
        self._send(mido.Message('control_change', control=control.value, value=value))

    def sysex(self, data: List[int]) -> None:
        self._send(mido.Message('sysex', data=data))

    def _send(self, message: mido.Message) -> None:
        self._port_out.send(message)

    def create_lcd_display_data(self, characters: str, color: Color = Color.WHITE, invert: Invert = Invert.NONE) -> List[int]:
        characters = unidecode(characters)
        character_data = self._pad_to(list(map(ord, characters[:14])), 14)
        color_code = color.value | (invert.value << 4)

        return [0x00, 0x20, 0x32, 0x41, 0x4c, 0x00, color_code] + character_data

    def create_segment_display_data(self, characters: str) -> List[int]:
        characters = unidecode(characters)
        character_data = self._pad_to(lcd_7bit_render(characters[:12]), 12)

        return [0x00, 0x20, 0x32, 0x41, 0x37] + character_data + [0x00, 0x00]

    @staticmethod
    def _pad_to(data: List[int], n: int) -> List[int]:
        trimmed = data[:n]
        return trimmed + [0] * (n - len(trimmed))
