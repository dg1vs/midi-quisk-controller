# Control Quisk with a Behringer X-Touch One

For my ham activities I'm mainly using Quisk, a fantastic software from Jim N2ADR. One missing part was the opportunity to use a midi-control surface. Recently I bought a Behringer X-Touch One MIDI DAW controller for different applications.

After playing around and trying different approaches I wrote a small python software which is able to control Quisk. The main cool feature now is to have a real wheel to tune the transceiver. Furthermore, some important task mapped to different keys on the DAW controller, like mode switching.

The software is based on a solution from Bert Hekman (https://github.com/DemonTPx/midi-dbus-controller) for controlling Spotify and Pulseaudio with a Behringer X-Touch One. 

The software python software handles the Midi-communication and transform the Midi commands to CAT-command based on the PowerSDR™ 2.x CAT command-set.

![alt text](https://github.com/dg1vs/midi-quisk-controller/blob/main/doc/quisk_daw.jpg?raw=true)
