import serial
import time
from serial import tools
from serial.tools import list_ports
from enum_comm import *
from SerialCommunication import *
import ipdb

def main():
    time_to_sleep = 0.1000
    media = LaserModule()
    left = 6 
    right = -6
    top = 5
    bottom = -5

    # media.seek_home()
    res = [0, 0]
    try:
        while True:
           #time.sleep(time_to_sleep)
           res = media.move_XY(res, 0, top)
           #time.sleep(time_to_sleep) 
           res = media.move_XY(res, 0, bottom)
           #time.sleep(time_to_sleep)
           res = media.move_XY(res, left, 0)
           #time.sleep(time_to_sleep) 
           res = media.move_XY(res, right, 0)
    except KeyboardInterrupt:
        pass
    finally:
        media.release()

def some_shit():
    media = LaserMoudle()
    media.
main()
# with serial.Serial(serial_path, 9600) as ser:
##    ser.write(config_commands['SEQUENCE_MODE'])
#    ser.write(config_commands['OFF'])
##    ser.write(config_commands['HOME'])
