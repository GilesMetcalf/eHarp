

import storage

# Allows CircuitPython code to write to CIRCUITPY.
# The USB drive may become read-only to the host computer.
storage.remount("/", readonly=False)