import mido
import signal

from gi.repository import GLib
from midi_controller import MidiController
from event_handler import EventHandler
from serial_hamlib import SerialHamlib


#TODO Setup
serialport = SerialHamlib('/tmp/QuiskTTY0')

# TODO Setup
mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
# TODO Setup
controller = MidiController('X-Touch One')

controller.reset()

handler = EventHandler(controller, serialport)
handler.setup()
handler.read_quisk_and_set_surface()

loop = GLib.MainLoop()


def sigint_handler(sig, frame):
    if sig == signal.SIGINT:
        loop.quit()


signal.signal(signal.SIGINT, sigint_handler)
loop.run()

handler.stop()
controller.reset()
