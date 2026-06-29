# eHarp in CircuitPython

# +-------------------------------+
# |   *** eHarp v2.0 Project ***  |
# |                               |
# | Author:         Gil Metcalf   |
# | Code version:   2.10.8        |
# | Date:           28-Jun-2026   |
# | Licence :       GPL v3.0      |
# +-------------------------------+

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
import config

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
scan_in.pull = digitalio.Pull.UP
lsr_enbl = digitalio.DigitalInOut(board.GP9)
lsr_enbl.direction = digitalio.Direction.OUTPUT

# IO ports (analogue input control)
baseline_in = analogio.AnalogIn(board.A0)
baseline_out = pwmio.PWMOut(board.GP18, frequency=500)

# Scanning constants
num_notes = config.NUM_NOTES
output_enable = False # Disable MIDI note generation for setup and calibration

# Menu handling constants
button_pressed = [0,0,0,0]
last_button_state = [0,0,0,0]

# State values
state_menu = 0
state_scale = 0
state_tune = 6
state_channel = 1
state_octave = 0
state_velocity = 6

# Menus
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

system_menu = ["Calibration", "Slow Scan", "Single Step", "Mute lasers"]

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
current_octave = 0
last_octave_up = 0
last_octave_down = 0
last_sustain = 0
last_mod = 0
last_bend = 0
note_active = [0 for i in range(num_notes)]
note_valid = [1 for i in range(num_notes)]

# Display constants
displayio.release_displays()
i2c = busio.I2C(board.GP5, board.GP4)  # Update pins if needed
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=config.DISPLAY_WIDTH, height=config.DISPLAY_HEIGHT, display_offset=config.DISPLAY_OFFSET)
display.rotation = config.DISPLAY_ROTATION
display_window = config.DISPLAY_WINDOW


# +----------------------+
# | Laser scan functions |
# +----------------------+

def selectMuxChannel(s0, s1, s2, mux):
  s0.value = (mux & 0x01) > 0  # Set LSB
  s1.value = (mux & 0x02) > 0  # Set second bit
  s2.value = (mux & 0x04) > 0  # Set third bit

def selectLaser(cell):
  # Select and turn on the selected laser
  row = cell % config.NUM_ROWS
  col = cell // config.NUM_ROWS
  lsr_enbl.value = 0
  selectMuxChannel(row_s0, row_s1, row_s2, row)
  selectMuxChannel(col_s0, col_s1, col_s2, col)
  lsr_enbl.value = 1

def set_baseline():
  lsr_enbl.value = 0
  for _ in range(config.CALIBRATION_SCANS):
    base_mv = baseline_in.value / config.DCMV_RATIO
    time.sleep(config.BASE_SETTLE)
    if base_mv > config.BASE_OFFSET:
      offset = base_mv - config.BASE_OFFSET
      baseline_out.duty_cycle = int(offset * config.DCMV_RATIO)

def checkForValidNotes():
  global note_valid, note_active, output_enable
    # Reset everything
  note_active = [0 for i in range(num_notes)]
  note_valid = [1 for i in range(num_notes)]
    # Loop around the array and look for blocked/non-working lasers
    # Non-working notes will be ignored in scans so that they don't play continuously.
  output_enable = False
  for _ in range(config.CALIBRATION_SCANS):
    for cell in range(0,num_notes):
      selectLaser(cell)
      time.sleep(config.LASER_SETTLE) # Settle time
      current_sensor = scan_in.value
      if current_sensor == config.NOTE_ON_LOGIC:   # Laser is not reaching the sensor
        note_valid[cell] = 0    # Mark the note as dead
      else:
        note_valid[cell] = 1    # Mark the note as working
  # Back to main menu
  output_enable = True
  go_back()

def calibrate():
  set_baseline()
  checkForValidNotes()

def scanMatrix():
  # global note_valid, state_scale
  for cell in range(0,num_notes):
      if scale_map[state_scale][cell] == 1 and note_valid[cell] == 1:
        selectLaser(cell)
        time.sleep(config.LASER_SETTLE) # Settle time
        current_sensor = scan_in.value
        if (current_sensor == config.NOTE_ON_LOGIC and note_active[cell] == 0):
          note_active[cell] = 1
          testScale(cell)
        elif (current_sensor != config.NOTE_ON_LOGIC and note_active[cell] == 1):
          note_active[cell] = 0
          releaseNote(cell)

def slow_scan():
  # Slowly cycle round all lasers
  global output_enable
  output_enable = False
  for _ in range(0,config.SLOW_SCAN_COUNT):
    for cell in range(0,num_notes):
      selectLaser(cell)
      time.sleep(config.SLOW_SCAN_SPEED)
  # Back to main menu
  output_enable = True
  go_back()

def single_step():
  # Manually step through lasers
  global last_button_state
  this_step = 0
  while True:
    if button_up.value == 0 and last_button_state[0] == 0:
      last_button_state[0] = 1
      this_step += 1
      if this_step > num_notes - 1:
        this_step = num_notes - 1
    if button_dn.value == 0 and last_button_state[1] == 0:
      last_button_state[1] = 1
      this_step -= 1
      if this_step < 0:
        this_step = 0
    if button_bck.value == 0 and last_button_state[3] == 0:
      last_button_state[3] = 1
      break
    selectLaser(this_step)
    time.sleep(0.5) # Allow time to release the button!
    last_button_state[0] = 0
    last_button_state[1] = 0
    last_button_state[3] = 0
    lsr_enbl.value = 0  # Turn off any lasers
  go_back()

def mute_lasers():
  # Turn lasers off for up to 1 minute
  global output_enable
  output_enable = False
  lsr_enbl.value = 0
  start_time = time.monotonic()
  while time.monotonic() - start_time < config.MAX_MUTE_TIME:  # Press any button to continue...
    if not button_up.value:
      break
    if not button_dn.value:
      break
    if not button_sel.value:
      break
    if not button_bck.value:
      break
    time.sleep(0.05)
  output_enable = True
  lsr_enbl.value = 1


# +--------------------------+
# | Scale and MIDI functions |
# +--------------------------+
def set_scale(index):
  global state_scale
  state_scale = index
  scale_menu.pointer = index
  go_back()

def set_tune(index):
  global state_tune
  state_tune = index
  tuning_menu.pointer = index
  go_back()

def set_velocity(index):
  global state_velocity
  state_velocity = index
  velocity_menu.pointer = index
  go_back()

def set_channel(index):
  global state_channel
  state_channel = index
  channel_menu.pointer = index
  go_back()


# +----------------------------+
# | Menu and display functions |
# +----------------------------+

# Classes for menu handling
class Menu:
  def __init__(self, title, items, pointer = 0):
    self.title = title
    self.items = items
    self.pointer = max(0, min(pointer, len(items) - 1))
class MenuItem:
  def __init__(self, text, action=None, submenu=None):
    self.text = text
    self.action = action
    self.submenu = submenu


# Menu configuration
scale_menu = Menu(
  "Scales",
  [MenuItem(
    scale_name, action=lambda idx=i: set_scale(idx))
    for i, scale_name in enumerate(scales)
  ], state_scale)

tuning_menu = Menu(
  "Tuning",
  [MenuItem(
    tuning_value, action=lambda idx=i: set_tune(idx))
    for i, tuning_value in enumerate(tuning)
  ], state_tune)

channel_menu = Menu(
  "Channel",
  [MenuItem(
    channel_value, action=lambda idx=i: set_channel(idx))
    for i, channel_value in enumerate(channel)
  ], state_channel)

velocity_menu = Menu(
  "Velocity",
  [MenuItem(
    velocity_value, action=lambda idx=i: set_velocity(idx))
    for i, velocity_value in enumerate(velocity)
  ], state_velocity)

system_menu = Menu("Diagnostics", [
  MenuItem("Calibration", action=calibrate),
  MenuItem("Slow Scan", action=slow_scan),
  MenuItem("Single Step", action=single_step),
  MenuItem("Mute lasers", action=mute_lasers)
])

main_menu = Menu("Main", [
  MenuItem("Scale / Mode", submenu=scale_menu),
  MenuItem("Tuning", submenu=tuning_menu),
  MenuItem("MIDI Channel", submenu=channel_menu),
  MenuItem("Velocity", submenu=velocity_menu),
  MenuItem("Diagnostics", submenu=system_menu)
])

menu_stack = [main_menu]

def show_splash():
  splash_group = displayio.Group()
  bitmap = displayio.OnDiskBitmap(config.LOGO_FILE)
  tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=0, y=-10)
  splash_group.append(tile_grid)
  display.root_group = splash_group
  start_time = time.monotonic()
  while time.monotonic() - start_time < config.SPLASH_TIME:  # Press any button to continue or timeout..
    if not button_up.value:
      break
    if not button_dn.value:
      break
    if not button_sel.value:
      break
    if not button_bck.value:
      break
    time.sleep(0.05)

def get_window(this_menu, this_pointer):
  item_count = len(this_menu)
  this_pointer = max(0, min(this_pointer, item_count - 1))
  start = (this_pointer // display_window) * display_window
  end = min(start + display_window, item_count)
  return start, end

def show_menu(menu, pointer):
  start, end = get_window(menu.items, pointer)
  menu_group = displayio.Group(x=-6, y=-16)
  for i in range(start, end):
    y_pos = 20 + ((i - start) * 12)
    item = menu.items[i]
    if i == pointer:
      bg_width = len(item.text) * 7
      bg_bitmap = displayio.Bitmap(bg_width, 10, 2)
      bg_palette = displayio.Palette(2)
      bg_palette[0] = 0xFFFFFF
      bg_palette[1] = 0x000000
      bg_tilegrid = displayio.TileGrid(
        bg_bitmap,
        pixel_shader=bg_palette,
        x=20,
        y=y_pos - 3
      )
      menu_group.append(bg_tilegrid)
      text_label = label.Label(
        terminalio.FONT,
        text=item.text,
        color=0x000000,
        x=20,
        y=y_pos + 2
      )
    else:
      text_label = label.Label(
        terminalio.FONT,
        text=item.text,
        color=0xFFFFFF,
        x=20,
        y=y_pos + 2
      )
    menu_group.append(text_label)
  display.root_group = menu_group

def step_up():
  current_menu = menu_stack[-1]
  current_menu.pointer += 1
  if current_menu.pointer > len(current_menu.items) - 1:
    current_menu.pointer = len(current_menu.items) - 1
  show_menu(current_menu, current_menu.pointer)

def step_down():
  current_menu = menu_stack[-1]
  current_menu.pointer -= 1
  if current_menu.pointer < 0:
    current_menu.pointer = 0
  show_menu(current_menu, current_menu.pointer)

def select_item():
  current_menu = menu_stack[-1]
  selected_item = current_menu.items[current_menu.pointer]
  if selected_item.submenu:
    menu_stack.append(selected_item.submenu)
    show_menu(selected_item.submenu, selected_item.submenu.pointer)
  elif selected_item.action:
     selected_item.action()

def go_back():
  if len(menu_stack) > 1:
    menu_stack.pop()
  current_menu = menu_stack[-1]
  show_menu(current_menu, current_menu.pointer)

def get_current_menu():
    return menu_stack[-1]

def test_menu_buttons():
  global last_button_state
  if button_up.value == 0 and last_button_state[0] == 0:
    last_button_state[0] = 1
    step_up()
  if button_dn.value == 0 and last_button_state[1] == 0:
    last_button_state[1] = 1
    step_down()
  if button_sel.value == 0 and last_button_state[2] == 0:
    last_button_state[2] = 1
    select_item()
  if button_bck.value == 0 and last_button_state[3] == 0:
    last_button_state[3] = 1
    go_back()
    # Button release debounce clearing
  if button_up.value == 1 and last_button_state[0] == 1:
    last_button_state[0] = 0
  if button_dn.value == 1 and last_button_state[1] == 1:
    last_button_state[1] = 0
  if button_sel.value == 1 and last_button_state[2] == 1:
    last_button_state[2] = 0
  if button_bck.value == 1 and last_button_state[3] == 1:
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
  pitch = note + config.MIDI_OFFSET
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


# +-------------------------------+
# | Async MIDI controls read cycle |
# +-------------------------------+

def test_midi_controls():
  global last_octave_up, last_octave_down, last_bend, last_mod, last_sustain
  global current_octave, state_octave
  current_octave_button_up = button_oct_up.value
  if last_octave_up == 0 and current_octave_button_up == 0:
    current_octave = current_octave + 1
    if current_octave > config.MAX_OCTAVE:
      current_octave = config.MAX_OCTAVE
    state_octave = current_octave
    last_octave_up = 1
  if last_octave_up == 1 and current_octave_button_up == 1:
    last_octave_up = 0
  
  current_octave_button_dn = button_oct_dn.value
  if last_octave_down == 0 and current_octave_button_dn == 0:
    current_octave=  current_octave - 1
    if current_octave < config.MIN_OCTAVE:
      current_octave = config.MIN_OCTAVE
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
  if (mod_value != last_mod) and abs(mod_value - last_mod) > config.IGNORE_JITTER:
    last_mod = mod_value
    conv_mod_value = int(abs(mod_value - 16384)/128)
    modChange(conv_mod_value)

  bend_value = int(32768 - (bend_in.value/2))
  if (bend_value != last_bend) and abs(bend_value - last_bend) > config.IGNORE_JITTER:
    last_bend = bend_value
    bend(bend_value/2)

################################
# This is the main entry point #
################################

# Initial setup stuff and boot sequence
baseline_out.duty_cycle = config.INITIAL_BASELINE
output_enable = False
show_splash()
calibrate()
show_menu(main_menu,main_menu.pointer)

# Loop forever...
while True:
  output_enable = True  # Ignore note generation for the setup cycle
  test_menu_buttons()
  scanMatrix()
  test_midi_controls()
