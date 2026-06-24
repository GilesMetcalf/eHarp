# Lughnasadh eHarp
This is the ongoing eHarp project. 

The eharp is a full-featured MIDI controller that offers the following functions:
- 32 notes that can be played
- Fully polyphonic
- Multi-level menu system
- A choice of 32 different scales (modes)
- A choice of MIDI channels
- Transposition from -6 to +6 intervals. Essentially any key in the octave.
- 11 selectable velocity settings
- Pitch and Bend controls
- Self-calibration to compensate for background light levels
- Several self-diagnostic features

## Architecture and principles
The eHarp is based on a scanned matrix of small lasers to detect an interruption to the beam (by sticking fingers into the beam!). 
The interruption is detected by a phototransistor which feeds an analogue level amplifier and a digital comparator. 
A microcontroller (a Raspberry Pi Pico 2) runs CircuitPython code to detect the interruption, identify which laser is on at the time,
makes appropriate adjustments depending on the selected scale, velocity, bend value and transposition, and them emits MIDI messages to
whatever device is on the end. 

The lasers are small 5mW diodes (such as are used in laser pointers), scanned sequentially by the microcontroller. Only "active" diodes are scanned, so
any which are not part of the scale, or that have been identified as blocked or faulty by the calibration routines are not illuminated and are 
skipped from the scan. This reduces any latency in generating notes, as well as preventing spurious notes playing.


*My thanks also to Adam Metcalf for the original inspiration, as well as much sage advice during the design and build of this project*
