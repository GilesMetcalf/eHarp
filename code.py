# eHarp in CircuitPython

import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1107
import busio
import digitalio
import time
import analogio
import pwmio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange

# +------------------------------+
# | Constants and menu constants |
# +------------------------------+

# IO ports (menu buttons)
button_up = digitalio.DigitalInOut(board.GP2)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP
button_dn = digitalio.DigitalInOut(board.GP3)
button_dn.direction = digitalio.Direction.INPUT
button_dn.pull = digitalio.Pull.UP
button_bck = digitalio.DigitalInOut(board.GP0)
button_bck.direction = digitalio.Direction.INPUT
button_bck.pull = digitalio.Pull.UP
button_sel = digitalio.DigitalInOut(board.GP1)
button_sel.direction = digitalio.Direction.INPUT
button_sel.pull = digitalio.Pull.UP

# IO ports (MIDI controls)
button_oct_up = digitalio.DigitalInOut(board.GP22)
button_oct_up.direction = digitalio.Direction.INPUT
button_oct_up.pull = digitalio.Pull.UP
button_oct_dn = digitalio.DigitalInOut(board.GP21)
button_oct_dn.direction = digitalio.Direction.INPUT
button_oct_dn.pull = digitalio.Pull.UP
button_stn = digitalio.DigitalInOut(board.GP19)
button_stn.direction = digitalio.Direction.INPUT
button_stn.pull = digitalio.Pull.UP
mod_in = analogio.AnalogIn(board.A1)
bend_in = analogio.AnalogIn(board.A2)

# IO ports (note scanning)
row_s0 = digitalio.DigitalInOut(board.GP10)
row_s0.direction = digitalio.Direction.OUTPUT
row_s1 = digitalio.DigitalInOut(board.GP11)
row_s1.direction = digitalio.Direction.OUTPUT
row_s2 = digitalio.DigitalInOut(board.GP12)
row_s2.direction = digitalio.Direction.OUTPUT
col_s0 = digitalio.DigitalInOut(board.GP6)
col_s0.direction = digitalio.Direction.OUTPUT
col_s1 = digitalio.DigitalInOut(board.GP7)
col_s1.direction = digitalio.Direction.OUTPUT
col_s2 = digitalio.DigitalInOut(board.GP8)
col_s2.direction = digitalio.Direction.OUTPUT
scan_in = digitalio.DigitalInOut(board.GP17)
scan_in.direction = digitalio.Direction.INPUT
lsr_enbl = digitalio.DigitalInOut(board.GP9)
lsr_enbl.direction = digitalio.Direction.OUTPUT

# Scanning constants
num_notes = 32
num_rows = 6
num_cols = 6
calibration_scans = 10 
note_on_logic = 0 # input value for "on" note
output_enable = False
slow_scan_count = 5   # number of cycles for slow scan
slow_scan_speed = 0.25 # number of seconds for each step in slow scan

# Menu constants
len_main = 3
len_scale = 23
len_tuning = 13
len_channel = 11
display_window = 10
current_top = 0
current_menu = 0
current_pointer = 0
button_pressed = [0,0,0,0]
last_button_state = [0,0,0,0]

# State values
state_menu = 0
state_scale = 0
state_tune = 6
state_channel = 1
state_octave = 0
state_velocity = 6
# state_system = 0

# Menus
main_menu = [
  "Scale / mode",
  "Tuning",
  "MIDI channel",
  "Velocity",
  "System"
]

scales = [
  "Chromatic",
  "Major",
  "Minor",
  "Lydian",
  "Aeolian",
  "Super Locrian",
  "Augmented",
  "Bebop Dominant",
  "Blues",
  "Dorian",
  "Double Harmonic",
  "Enigmatic",
  "Flamenco",
  "Gypsy",
  "Half Diminished",
  "Harmonic Major",
  "Harmonic Minor",
  "Istrian",
  "Locrian",
  "Lydian Augmented",
  "Lydian Diminished",
  "Mixolydian",
  "Phrygian"
]

tuning = ["-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "6"]

channel = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

velocity = ["8", "16", "24", "32", "48", "64","72", "80", "96", "112", "127"]

system_menu = ["Calibration","SlowScan"]

# Mapping scales
scale_map = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # Chromatic
  [1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1],  # Major
  [1,0,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,1],  # Minor
  [1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1],  # Lydian
  [1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0],  # Aeolian
  [1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0],  # Super Locrian
  [1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1],  # Augmented
  [1,0,1,0,1,1,0,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1],  # Bebop Dominant
  [1,0,0,1,0,1,1,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,1],  # Blues
  [1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0],  # Dorian
  [1,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1],  # Double Harmonic
  [1,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,1],  # Enigmatic
  [1,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1],  # Flamenco
  [1,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0],  # Gypsy
  [1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0],  # Half Diminished
  [1,0,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1],  # Harmonic Major
  [1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,1],  # Harmonic Minor
  [1,1,0,1,1,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,0,0,0],  # Istrian
  [1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0],  # Locrian
  [1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],  # Lydian Augmented
  [1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1],  # Lydian Diminished
  [1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0],  # Mixolydian
  [1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0]   # Phrygian
]

# MIDI constants and variables
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=state_channel)
midi_offset = 48
ignore_jitter = 500
max_octave = 3
min_octave = -3
current_octave = 0
last_octave_up = 0
last_octave_down = 0
last_sustain = 0
last_mod = 0
last_bend = 0
note_active = [0 for i in range(num_notes)]
note_valid = [1 for i in range(num_notes)]

# Display constants
WIDTH = 128
HEIGHT = 128
BORDER = 2
displayio.release_displays()
i2c = busio.I2C(board.GP5, board.GP4)  # Update pins if needed
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)
display.rotation = 180
splash_time = 10  # Splashscreen display time

# +----------------------------+
# | Menu and display functions |
# +----------------------------+

def show_splash():
  splash_group = displayio.Group()
  bitmap = displayio.OnDiskBitmap("/logo.bmp")
  tile_grid = displayio.TileGrid(
      bitmap,
      pixel_shader=bitmap.pixel_shader
  )
  splash_group.append(tile_grid)
  display.root_group = splash_group
  time.sleep(splash_time)

def get_window(this_menu, this_pointer):
  item_count = len(this_menu)
  this_pointer = max(0, min(this_pointer, item_count - 1))
  start = (this_pointer // display_window) * display_window
  end = min(start + display_window, item_count)
  return start, end

def show_menu(menu, pointer):
  global current_top
  menu_group = displayio.Group(x=15, y=-10)
  if menu == 0 :
    working_menu = main_menu
  elif menu == 1 :
    working_menu = scales
  elif menu == 2 :
    working_menu = tuning
  elif menu == 3 :
    working_menu = channel
  elif menu == 4 :
    working_menu = velocity
  elif menu == 5 :
    working_menu = system_menu
  start, end = get_window(working_menu, pointer)

  for i in range(start, end):
    y_pos = 20 + ((i-start) * 12)
    if i == pointer:
      bg_width = len(working_menu[i]) * 7
      bg_bitmap = displayio.Bitmap(bg_width, 10, 2)
      bg_palette = displayio.Palette(2)
      bg_palette[0] = 0xFFFFFF
      bg_palette[1] = 0x000000
      bg_tilegrid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=20, y=y_pos-3)
      menu_group.append(bg_tilegrid)
      text_label = label.Label(terminalio.FONT, text=working_menu[i], color=0x000000, x=20, y=y_pos+2)
    else:
      text_label = label.Label(terminalio.FONT, text=working_menu[i], color=0xFFFFFF, x=20, y=y_pos+2)
    menu_group.append(text_label)
  display.root_group = menu_group

def set_main_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 0
  current_pointer = 0
  state_menu = 0
  show_menu(current_menu, current_pointer)

def set_scale_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 1
  current_pointer = state_scale
  state_menu = 1
  show_menu(current_menu, current_pointer)

def set_tune_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 2
  current_pointer = state_tune
  state_menu = 2
  show_menu(current_menu, current_pointer)

def set_midi_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 3
  current_pointer = state_channel
  state_menu = 3
  show_menu(current_menu, current_pointer)

def set_velocity_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 4
  current_pointer = state_velocity
  state_menu = 4
  show_menu(current_menu, current_pointer)

def set_system_menu():
  global current_menu, current_pointer, state_menu
  current_menu = 5
  current_pointer = 0
  state_menu = 5
  show_menu(current_menu, current_pointer)

# Menu control handling
def select_item():
  global state_scale, state_tune, state_channel, state_velocity, state_system, output_enable
  # Menu logic
  if current_menu==0:
    if current_pointer==0:  # Main menu -> Scales
      set_scale_menu()
    if current_pointer==1:  # Main menu -> Tuning
      set_tune_menu()
    if current_pointer==2: # Main menu -> MIDI channel
      set_midi_menu()
    if current_pointer==3: # Main menu -> Velocity
      set_velocity_menu()
    if current_pointer==4: # Main menu -> System
      set_system_menu()   

  if current_menu==1:
    state_scale = current_pointer
  if current_menu==2:
    state_tune = current_pointer
  if current_menu==3:
     state_channel = current_pointer
  if current_menu==4:
    state_velocity = current_pointer
  if current_menu==5:
    state_system = current_pointer
    if current_pointer==0:  # Calibration
      output_enable = False
      checkForValidNotes()
      output_enable = True
    elif current_pointer==1:  # Slow scan
      slow_scan()

def  back_to_main():
  set_main_menu()

def step_up():
  global current_pointer
  current_pointer = current_pointer + 1
  if current_menu==0:
    if current_pointer>len(main_menu)-1:
      current_pointer = len(main_menu)-1
  if current_menu==1:
    if current_pointer>len(scales)-1:
      current_pointer = len(scales)-1
  if current_menu==2:
    if current_pointer>len(tuning)-1:
      current_pointer = len(tuning)-1
  if current_menu==3:
    if current_pointer>len(channel)-1:
      current_pointer = len(channel)-1
  if current_menu==4:
    if current_pointer>len(velocity):
      current_pointer = len(velocity)-1
  if current_menu==5:
    if current_pointer>len(system_menu):
      current_pointer = len(system_menu)-1
  show_menu(current_menu, current_pointer)

def step_down():
  global current_pointer
  current_pointer = current_pointer - 1
  if current_pointer<0:
    current_pointer = 0
  show_menu(current_menu, current_pointer)

def test_menu_buttons():
  global last_button_state
  if button_up.value==0 and last_button_state[0]==0:
    last_button_state[0] = 1
    step_up()
  if button_dn.value==0 and last_button_state[1]==0:
    last_button_state[1] = 1
    step_down()
  if button_sel.value==0 and last_button_state[2]==0:
    last_button_state[2] = 1
    select_item()
  if button_bck.value==0 and last_button_state[3]==0:
    last_button_state[3] = 1
    back_to_main()
  if button_up.value==1 and last_button_state[0]==1:
    last_button_state[0] = 0
    step_up
  if button_dn.value==1 and last_button_state[1]==1:
    last_button_state[1] = 0
    step_down
  if button_sel.value==1 and last_button_state[2]==1:
    last_button_state[2] = 0
    select_item()
  if button_bck.value==1 and last_button_state[3]==1:
    last_button_state[3] = 0  


# +----------------+
# | MIDI functions |
# +----------------+

def get_tuning():
  return int(tuning[state_tune])

def get_velocity():
  return int(velocity[state_velocity])

def get_channel():
  return int(channel[state_channel])-1

def getNote(note):
  pitch = note + midi_offset
  pitch = pitch + get_tuning()
  pitch = pitch + (12 * state_octave)
  return pitch

def playNote(in_pitch):
  if output_enable:
    midi.send(NoteOn(getNote(in_pitch), get_velocity()), get_channel())

def releaseNote(in_pitch):
  midi.send(NoteOff(getNote(in_pitch), 0), get_channel())

def testScale(note):
  if scale_map[state_scale][note] == 1:
    playNote(note)
  elif scale_map[state_scale][note] == 0 and note_active[note] == 1:
    releaseNote(note)

def sustainOn():
  midi.send(ControlChange(64, 127), get_channel())

def sustainOff():
  midi.send(ControlChange(64, 0), get_channel())

def modChange(mod):
  midi.send(ControlChange(1, mod), get_channel())

def bend(bend_val):
  midi.send(PitchBend(int(bend_val)), get_channel())



# +----------------------+
# | Laser scan functions |
# +----------------------+

def selectMuxChannel(s0, s1, s2, mux):
  s0.value = (mux & 0x01) > 0  # Set LSB
  s1.value = (mux & 0x02) > 0  # Set second bit
  s2.value = (mux & 0x04) > 0  # Set third bit

def checkForValidNotes():
  global note_valid
    # Loop around the array and look for blocked/non-working lasers
    # Non-working notes will be ignored in scans so that they don't play continuously.
  for _ in range(calibration_scans):
    for cell in range(0,num_notes):
      row = cell % num_rows
      col = cell // num_rows
      lsr_enbl.value = 0
      selectMuxChannel(row_s0, row_s1, row_s2, row)
      selectMuxChannel(col_s0, col_s1, col_s2, col)
      time.sleep(0.001) # Settle time
      current_sensor = scan_in.value
      lsr_enbl.value = 1
      if current_sensor == note_on_logic:   # Laser is not reaching the sensor
        note_valid[cell] = 0    # Mark the note as dead
      else:
        note_valid[cell] = 1    # Mark the note as working
  # Back to main menu
  back_to_main()

def scanMatrix():
  # global note_valid, state_scale
  for cell in range(0,num_notes):
      if scale_map[state_scale][cell]==1 and note_valid[cell]==1:
        row = cell % num_rows
        col = cell // num_rows
        lsr_enbl.value = 0
        selectMuxChannel(row_s0, row_s1, row_s2, row)
        selectMuxChannel(col_s0, col_s1, col_s2, col)
        # time.sleep(0.001) # Settle time
        current_sensor = scan_in.value
        lsr_enbl.value = 1
        if (current_sensor==note_on_logic and note_active[cell]==0):
          note_active[cell] = 1
          testScale(cell)
        elif (current_sensor!=note_on_logic and note_active[cell]==1):
          note_active[cell] = 0
          releaseNote(cell)

def slow_scan():
  # Slowly cycle round all lasers
  for _ in range(0,slow_scan_count):
    for cell in range(0,num_notes):
      row = cell % num_rows
      col = cell // num_rows
      lsr_enbl.value = 0
      selectMuxChannel(row_s0, row_s1, row_s2, row)
      selectMuxChannel(col_s0, col_s1, col_s2, col)
      lsr_enbl.value = 1
      time.sleep(slow_scan_speed)
  # Back to main menu
  back_to_main()

# +-------------------------------+
# | Async MIDI controls read cycle |
# +-------------------------------+

def test_midi_controls():
  global last_octave_up, last_octave_down, last_bend, last_mod, last_sustain
  global current_octave, state_octave
  current_octave_button_up = button_oct_up.value
  if last_octave_up == 0 and current_octave_button_up == 0:
    current_octave = current_octave + 1
    if current_octave > max_octave:
      current_octave = max_octave
    state_octave = current_octave
    last_octave_up = 1
  if last_octave_up == 1 and current_octave_button_up == 1:
    last_octave_up = 0
  
  current_octave_button_dn = button_oct_dn.value
  if last_octave_down == 0 and current_octave_button_dn == 0:
    current_octave=  current_octave - 1
    if current_octave < min_octave:
      current_octave = min_octave
    state_octave = current_octave
    last_octave_down = 1
  if last_octave_down == 1 and current_octave_button_dn == 1:
    last_octave_down = 0

  current_sustain = button_stn.value
  if last_sustain == 0 and current_sustain == 0:
    sustainOn()
    last_sustain = 1
  if last_sustain == 1 and current_sustain == 1:
    sustainOff()
    last_sustain = 0

  # Read pots and send mod / bend commands
  mod_value = 32768 - (mod_in.value/2)
  if (mod_value != last_mod) and abs(mod_value - last_mod) > ignore_jitter:
    last_mod = mod_value
    conv_mod_value = int(abs(mod_value - 16384)/128)
    modChange(conv_mod_value)
  bend_value = int(32768 - (bend_in.value/2))
  if (bend_value != last_bend) and abs(bend_value - last_bend) > ignore_jitter:
    last_bend = bend_value
    bend(bend_value/2)

################################
# This is the main entry point #
################################

# Initial setup stuff
show_splash()
output_enable = False
checkForValidNotes()
set_main_menu()

# Loop forever...
while True:
  test_menu_buttons()
 # scanMatrix()
 # test_midi_controls()
  output_enable = True  # Ignore note generation for the setup cycle
