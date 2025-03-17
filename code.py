# eHarp in CircuitPython

import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1107
import busio
import digitalio
from analogio import AnalogIn

# Constants and menu constants
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

# # IO ports (MIDI controls)
# button_oct_up = digitalio.DigitalInOut(board.GP16)
# button_oct_up.direction = digitalio.Direction.INPUT
# button_oct_up.pull = digitalio.Pull.UP
# button_oct_dn = digitalio.DigitalInOut(board.GP17)
# button_oct_dn.direction = digitalio.Direction.INPUT
# button_oct_dn.pull = digitalio.Pull.UP
# button_oct_stn = digitalio.DigitalInOut(board.GP18)
# button_oct_stn.direction = digitalio.Direction.INPUT
# button_oct_stn.pull = digitalio.Pull.UP
# mod_in = AnalogIn(board.A1)
# bend_in = AnalogIn(board.A2)

# # IO ports (note scanning)
# row_s0 = digitalio.DigitalInOut(board.GP10)
# row_s0.direction = digitalio.Direction.OUTPUT
# row_s1 = digitalio.DigitalInOut(board.GP11)
# row_s1.direction = digitalio.Direction.OUTPUT
# row_s2 = digitalio.DigitalInOut(board.GP12)
# row_s2.direction = digitalio.Direction.OUTPUT
# col_s0 = digitalio.DigitalInOut(board.GP6)
# col_s0.direction = digitalio.Direction.OUTPUT
# col_s1 = digitalio.DigitalInOut(board.GP7)
# col_s1.direction = digitalio.Direction.OUTPUT
# col_s2 = digitalio.DigitalInOut(board.GP8)
# col_s2.direction = digitalio.Direction.OUTPUT
# scan_in = digitalio.DigitalInOut(board.GP17)
# scan_in.direction = digitalio.Direction.INPUT

# Menu constants
len_main = 3
len_scale = 23
len_tuning = 13
len_channel = 11
display_window = 10
current_top = 0
# max_top = 0
current_menu = 0
current_pointer = 0
# num_buttons = 4
button_pressed = [0,0,0,0]
last_button_state = [0,0,0,0]
# menu_buttons = [button_up, button_dn, button_sel, button_bck]

# State values
state_menu = 0
state_scale = 0
state_tune = 6
state_channel = 1
state_octave = 0
state_velocity = 64

# Menus
main_menu = [
  "Scale / mode",
  "Tuning",
  "MIDI channel",
  "Velocity"
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

tuning = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

channel = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

velocity = [8, 16, 24, 32, 48, 64, 80, 96, 112, 127]

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

# MIDI constants
current_octave = 0
max_octave = 3
min_octave = -3
last_octave_up = 0
last_octave_down = 0
last_sustain = 0
last_mod = 0;
last_bend = 0;

# Set up the display
WIDTH = 128
HEIGHT = 128
BORDER = 2
displayio.release_displays()
# Use for I2C
i2c = busio.I2C(board.GP5, board.GP4)  # Update pins if needed
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)
display.rotation = 180


# Menu functions
def get_window(this_menu, this_pointer):
  window = []
  item_count = len(this_menu)
  this_pointer = max(0, min(this_pointer, item_count - 1))
  start = (this_pointer // display_window) * display_window
  end = min(start + display_window, item_count)
  print(f"Pointer: {this_pointer}")
  print(f"Start: {start}, End: {end}")
  return start, end, this_menu[start:end]

def show_menu(menu, pointer):
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
  start, end, window = get_window(working_menu, pointer)

  for i in range(0, len(window)):
    y_pos = 20 + (i * 12)
    if (i+start) == pointer:
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
  # current_pointer = 14
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

# Menu control handling
def select_item():
  # Menu logic
  if current_menu==0:
    if current_pointer==0:  # Main menu -> Scales
      set_scale_menu()
      # menu_scales(current_pointer)
    if current_pointer==1:  # Main menu -> Tuning
      set_tune_menu()
      # menu_tune(current_pointer)
    if current_pointer==2: # Main menu -> MIDI channel
      set_midi_menu()
      # menu_midi(current_pointer)
    if current_pointer==3: # Main menu -> Velocity
      set_velocity_menu()
      # menu_midi(current_pointer)
   
  if current_menu==1:
    state_scale = current_pointer
    print(f"Currently selected item: {scales[state_scale]}")
  if current_menu==2:
    state_tune = current_pointer
    print(f"Currently selected item: {tuning[state_tune]}")
  if current_menu==3:
    state_channel = current_pointer
    print(f"Currently selected item: {channel[state_channel]}")
  if current_menu==4:
    state_velocity = current_pointer
    print(f"Currently selected item: {velocity[state_velocity]}")
  
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
  print(f"Pointer is now {current_pointer}")
  show_menu(current_menu, current_pointer)

def step_down():
  global current_pointer
  current_pointer = current_pointer - 1
  if current_pointer<0:
    current_pointer = 0
  print(f"Pointer is now {current_pointer}")
  show_menu(current_menu, current_pointer)

def test_menu_buttons():
  if button_up.value==0 and last_button_state[0]==0:
    print("Up")
    last_button_state[0] = 1
    step_up()
  if button_dn.value==0 and last_button_state[1]==0:
    print("Down")
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

set_main_menu()
while True:
  test_menu_buttons()
