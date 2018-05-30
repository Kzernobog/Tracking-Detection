import serial
import time
from serial import tools
from serial.tools import list_ports
from enum_comm import *
from SerialCommunication import *

media = LaserModule()
right = 1
top = 1 
time_to_sleep = 1.000
try:
    while True:
        time.sleep(time_to_sleep)
        media.move_XY(right, top)
        time.sleep(time_to_sleep)

except KeyboardInterrupt:
    pass
finally:
    media.release()
