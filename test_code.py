# Cycle through laser array for test

import busio
import digitalio
import time
import board

# Constants
num_rows = 6
num_cols = 6
temp_loop_count = 5
scan_speed = 0.20

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
lsr_enbl = digitalio.DigitalInOut(board.GP9)
lsr_enbl.direction = digitalio.Direction.OUTPUT

def selectMuxChannel(s0, s1, s2, mux):
  s0.value = (mux & 0x01) > 0  # Set LSB
  s1.value = (mux & 0x02) > 0  # Set second bit
  s2.value = (mux & 0x04) > 0  # Set third bit

def scanMatrix():
  for col in range(0,num_cols):
    for row in range(0,num_rows):
    	lsr_enbl.value = 0
      selectMuxChannel(row_s0, row_s1, row_s2, row)
      selectMuxChannel(col_s0, col_s1, col_s2, col)
      lsr_enbl.value = 1
      time.sleep(scan_speed)


# Loop forever!
while True:
     
    scanMatrix()

