# eHarp in CircuitPython

# +-------------------------------+
# |   *** eHarp v2.0 Project ***  |
# |                               |
# | Author:         Gil Metcalf   |
# | Code version:   2.10.8        |
# | Date:           28-Jun-2026   |
# | Licence :       GPL v3.0      |
# +-------------------------------+

# Externalised config elements

# Scanning constants
NUM_NOTES = 32              # Number of notes avaiable on the eHarp
NUM_ROWS = 6                # Number of laser anodes to scan in matrix
NUM_COLS = 6                # Number of laser cathodes to scan in matrix
NOTE_ON_LOGIC = True        # input state for "on" note

# Calibration and diagnostics constants
CALIBRATION_SCANS = 10      # Number of scans for calibration cycle
SLOW_SCAN_COUNT = 5         # Number of cycles for slow scan
SLOW_SCAN_SPEED = 0.25      # Number of seconds for each step in slow scan
DCMV_RATIO = 10             # FITA duty cycle to mV ration for baseline control
BASE_OFFSET = 20            # Offset to set baseline value. Should be slightly above 0mV
BASE_SETTLE = 0.01          # Baseline ADC settle time in seconds
INITIAL_BASELINE = 150      # Initial baseline output value on boot
MAX_MUTE_TIME = 60          # Maximum seconds lasers can be muted for

# MIDI constants
MIDI_OFFSET = 48            # MIDI number for lowest note
IGNORE_JITTER = 500         # Threshold for bend/mod ADC change detection
MAX_OCTAVE = 3              # Maximum allowed octave setting
MIN_OCTAVE = -3             # Minimum allowed octave setting

# Display constants
DISPLAY_WIDTH = 128         # Display width in pixels
DISPLAY_HEIGHT = 128        # Display height in pixels
DISPLAY_OFFSET = 0          # Prevents display wrapping oddly (specific to oLED display)
DISPLAY_ROTATION = 180      # Spins display to show correctly on panel
DISPLAY_WINDOW = 10         # Maximum number of lines of text to display
SPLASH_TIME = 6             # Maximum number of seconds splashscreen will display
LOGO_FILE = "/logo.bmp"      # Logo file for splash screen
