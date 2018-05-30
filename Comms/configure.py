import serial
import time
from serial import tools
from serial.tools import list_ports
from enum_comm import *
from SerialCommunication import *


#ports = serial.tools.list_ports.comports()
#for port in ports:
#    #print("port "+port)
#    print("device path "+port.device)
#    print("device name "+port.name)
#    print("hardware information "+str(port.hwid))
#    print("product id "+str(port.pid))
#    print("serial number "+str(port.serial_number))
#    print("product "+str(port.product))
#    print("Interface type "+str(port.interface))
serial_path = '/dev/ttyUSB0'
#with serial.Serial(serial_path, 9600) as ser:
#    ser.write(config_commands['SEQUENCE_MODE'])
#    ser.write(config_commands['ON'])
#    ser.write(config_commands['HOME'])

def main():
    time_to_sleep = 0.0000
    media = LaserModule()
    #media.seek_home()
    try:
        while True:
            for i in range(9):
                media.move_Y(1)
                a = media.read()
                print(a)
                time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep) 
            for i in range(9):
                media.move_Y(1, 'REVERSE')
                a = media.read()
                print(a)
                time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep) 
            for i in range(9):
                media.move_Y(1, 'REVERSE')
                a = media.read()
                print(a)
                time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                    
            for i in range(9):
                media.move_Y(1)
                a = media.read()
                print(a)
                time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1, 'REVERSE')
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
                for i in range(9):
                    media.move_X(1)
                    a = media.read()
                    print(a)
                    time.sleep(time_to_sleep)
    except KeyboardInterrupt:
        pass
    finally:
        media.release()

main()
#with serial.Serial(serial_path, 9600) as ser:
##    ser.write(config_commands['SEQUENCE_MODE'])
#    ser.write(config_commands['OFF'])
##    ser.write(config_commands['HOME'])

