# Lughnasadh eHarp
This is the ongoing eHarp project. 

## feature summary
The eharp is a full-featured MIDI controller that offers the following functions:
- Up to 32 notes that can be played
- Fully polyphonic
- A choice of 23 different scales (modes)
- A choice of MIDI channels
- Transposition from -6 to +6 intervals. Essentially any key in the octave.
- Selectable octave settings from -3 to +3
- 11 selectable velocity settings
- Pitch and Bend controls
- Sustain pedal input
- Multi-level menu system
- Self-calibration to compensate for background light levels
- Several self-diagnostic features

## Architecture and principles
The eHarp is based on a scanned matrix of small lasers to detect an interruption to the beam (by sticking fingers into the beam!). The interruption is detected by a phototransistor which feeds an baseline-compensated analogue level amplifier and a digital comparator. A microcontroller (a Raspberry Pi Pico 2) runs CircuitPython code to detect the interruption, identify which laser is on at the time, makes appropriate adjustments depending on the selected scale, velocity, bend value and transposition, and them emits MIDI messages to whatever device is on the end. 

The lasers are small 5mW diodes (such as are used in laser pointers), scanned sequentially by the microcontroller. Only "active" diodes are scanned, so any which are not part of the scale, or that have been identified as blocked or faulty by the calibration routines are not illuminated and are skipped from the scan. This reduces any latency in generating notes, as well as preventing spurious notes playing.

## Boot and run sequences
### Boot up and calibration
On initially powering the eHarp up, the (numerous) I/O ports are initialised and the baseline offset output set to a default value of approximately 150mV. A flag is set to prevent any MIDI output (this stops random notes playing during calibration). A nice splash screen is displayed for a few seconds. This serves no purpose other than being flash, and can be aborted by pressing any button on the menu panel. The software twiddles it's little digital thumbs while this is displayed.
Once the splash expires, the eHarp drops into it's automated calibration routine. There are two elements to this. Firstly the baseline offset is adjusted to allow for the current ambient light by reading the sensor output (post amplification) with no lasers on. The offset voltage is adjusted to approximately 30-50mV above zero to give a bit of stability. 
Following the offset adjustment, all the lasers are scanned to check that they are producing an output and that the sensor is detecting them. (This assumes that there are no fingers in the way for this part!) Any which fail for any reason (poor and failing output - always a danger with cheap laser diodes! - misalignments or blockages, etc.) are marked as inactive and removed from normal scans. 
Finally, the main menu is displayed and the main scan routines are initiated.

### Run cycle
The run cycle essentially runs forever, and consists of three elements:
- The menu buttons are scanned. If any have been pressed, the menu subsystem executes whatever menu option is selected. This might be to change to a submenu, reset a state value (such as scale or key), or execute a calibration or diagnostic function. Once the action has been carried out, the menu returns to the parent level (or the main level, depending where it is in the heirarchy), and normal scanning continues.
- The laser matrix is scanned. All the available cells (0 to 31) are processed in sequence, and for each cell if the selected scale array and active note array both indicate that the cell is valid, the laser is illuminated. The sensor input is read, and if the beam is interrupted the current MIDI state for that note is checked. There are several possible outcomes at this stage:
  - The beam is not interrupted and the note is not active; do nothing and move on to the next cell.
  - The beam is not interrupted but the note was active; emit a <samp>NoteOff</samp> MIDI message.
  - The beam is interrupted and the note was active; do nothing and move on to the next cell.
  - The beam is interrupted and the note was not active; emit a <samp>NoteOn</samp> MIDI message.
- Once the cell has been  processed, the laser is turned off and the sequence moves to the next cell.
- Finally, once all the cells have been processed, the MIDI state (bend/mod controls and octave selection buttons) are scanned. Any changes are detected and state variables set accordingly. The bend and mod controls are analogue inputs from a joystick and are captured using the Pico's built-in ADC.

### MIDI generation
For each MIDI note generation event, before the <samp>NoteOn</samp> event is emitted, some adjustments and enhancements are needed. The <samp>NoteOn</samp> event contains several parameters:
- The actual note number, which is calculated from the cell number (0 to 31) plus the MIDI offset to get to the actual note (C3 for the bottom note). This is then appended with the transposition value (-6 to +6) and the octave value to give the required note.
- The velocity value (how hard the 'key' has been struck). This comes from the selected velocity value
- The MIDI channel number. This comes from the selected channel value.
  
On top of that, there are some MIDI control events that also need to be emitted, although these are not directly associated with a specific note:
- If the Bend control value has changed, a <samp>PitchBend</samp> event is emitted.
- If the Mod control value has changed, a <samp>ControlChange(1)</samp> event is emitted.
- If the Sustain pedal is pressed, a <samp>ControlChange(64)</samp> event is emitted with a parameter of 127 (sustain on).
- If the Sustain pedal is released, a <samp>ControlChange(64)</samp> event is emitted with a parameter of 0 (sustain off).


*My thanks also to Adam Metcalf for the original inspiration, as well as much sage advice during the design and build of this project (and not laughing at my terrible electronics!)*
