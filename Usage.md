# Using the eHarp

## IMPORTANT SAFETY NOTE!!!
This instrument uses lasers. Lots of lasers!
Although the laser diodes are relatively low power (<5mW), they are still sufficient to cause eye injury if stared into. **DO NOT LOOK DIRECTLY INTO THE LASER ARRAY!**

## The menus
There are a number of menus available that allow the user to select various settings for playing, as well as giving access to some diagnostic and calibration features.

### Save and Load menu
The user can store up to 8 sets of parameters, and recall them as needed. The parameters stored are:
- Scale / mode
- MIDI channel
- Velocity
- Transpositions
- Octave

When selecting one of these option, there are 8 slots labelled Song 1 through to Song 8. Each can hold a different set of parameters. 
Note that selecting to save in a slot that has been used before will overwrite any existing parameters.

### Scales menu
There are 23 different scales or modes that can be selected from the **Scales** menu:
- Chromatic
- Major
- Minor
- Lydian
- Aeolian
- Super Locrian
- Augmented
- Bebop Dominant
- Blues
- Dorian
- Double Harmonic
- Enigmatic
- Flamenco
- Gypsy
- Half Diminished
- Harmonic Major
- Harmonic Minor
- Istrian
- Locrian
- Lydian Augmented
- Lydian Diminished
- Mixolydian
- Phrygian

Selecting one of these modes will restrict the MIDI output to only notes within that scale. Other notes and incidentals will not play.

### Tuning menu
The eHarp is naturally tuned to C (that is, the lowest note is C3). The tuning menu will allow transposition to any other key in semitones. That will also apply to any mode or scale that has been selected.

### Channel mneu
This control selects the MIDI channel that messages are output on. By default, this is set to channel 0, but any channel up to 10 can be selected. Currently, it is not possible to select "all", although this may be implemented in the future.

### Velocity menu
MIDI velocity is a numerical representation of how hard a note is hit. Since this is not something that can be physically implemnted for interrupting a light beam, the **Velocity** menu allows the user to manually select one of 11 different velocity settings between 8 (really soft) and 127 (really hard). The default value is 64.

### Diagnostics menu
The **Diagnostics** menu provides access to a number of further features for recalibrating the eHarp, and some options that can be used when diagnosing issues or setting up the eHarp.

- _Calibration:_  This option reruns the automated calibration and valid note checks. It can be used if notes stop working, or notes play unasked. 
- _Slow Scan:_  This performs a slow scan of all the lasers in the array 5 times. It can be used to determine if all the laser diodes are working, as well as for setting the threshold for the comparator. MIDI messages will not be generated during this process, so no notes will play.
- _Single Step:_  Each laser is lit one at a time. The *"menu up"* and *"menu down"* buttons will step on to the next laser in the array. The *"menu back"* button will abort this process and return to the **Diagnosics** menu. MIDI messages will not be generated during this process, so no notes will play.
- _Mute Lasers:_  This option turns off all the lasers and precvents scanning for up to 1 minute. This is useful when setting the comparator threshold. At the end of the minute, or if any menu button is pressed before that, the process is aborted and the user returned to the **Diagnostics** menu.

Once all diagnostics have been completed, pressing the *"menu back"* button will return to the main menu, and normal operations will continue.

## The MIDI mod and octave controls
The **MOD** panel provides controls for changing the notes wheil playing.

### Octave buttons
The *Octave up* and *Octave down* buttons allow the user to transpose the output up or down full octaves (up to three octaves up or down from the nornal value, or between C1 to C6 for the lowest note). Scale/mode choice and any transposition remain unchanged when the octave is changed. 

### Mod/Bend control
The joystick performs three functions when playing. In one direction (marked on the panel) it bends the note playing up or down. In this fashion it performs in the same way as a Pitch Bend wheel on a normal keyboard.
In the orthogonal direction, the joystick acts as a Mod wheel, applying any modification (such as filter changes or vibrato) defined by the MIDI instrument being controlled. The **Mod** control is slightly different from the **Bend** control in that it works in the same way whichever way it is pushed.

Finally, If the joystick is pushed in, this turns on the sustain in the same way as using a sustain pedal.

## Connections
Three connections are provided.

### USB connection
The USB connection is used for both powering the eHarp, as well as providing a MIDI-over-USB communications with the MIDI instrument being used. This might be a DAW or a VST host, but equally it might be a hardware instrument such as a synth. Some sort of MIDI routing might be required (such as MIDIDash) to make sure that the messages appear where they should. This is dependent on your setup.

### MIDI output
There is also a 5-pin DIN standard MIDI connector in the schematic. I have not yet configured this in the software, but this will eventually mirror the USB MIDI output for more conventional connections.

### Sustain pedal
There is a 1/4-inch jack socket for a standard normally-off sustain pedal. 


