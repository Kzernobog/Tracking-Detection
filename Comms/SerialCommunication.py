import serial
import serial
from serial import tools
from serial.tools import list_ports
import serial
from Comms.enum_comm import *
import time
import ipdb


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
#
#serial_path = '/dev/ttyUSB0'
#a = ''
#with serial.Serial(serial_path, 9600) as ser:
#    ser.write(config_commands['SEQUENCE_MODE'])
#    #ser.write(config_commands['AUTO_MODE'])


# class that handles serial port communication
class LaserModule(object):

    # constructor
    def __init__(self, unix_path_to_port='/dev/ttyUSB0', baud_rate=9600):

        # serial port to access
        self.port = unix_path_to_port

        # baud rate
        self.baud_rate = baud_rate

        # sleep time
        self.time_to_sleep = 0.015

        # creating an instance of the Serial class - gives us
        # programmatic access to the serial ports
        self.media = serial.Serial(self.port, self.baud_rate)
        self.media.write(config_commands['HOME'])
        time.sleep(1)
        self.media.write(config_commands['SEQUENCE_MODE'])
        time.sleep(1)
        self.media.write(config_commands['ON'])

    # seeks the home position
    def seek_home(self, steps):
        '''
        steps - a tuple containing x and y distances to be traversed to reach
        the home position
        '''
        x = steps[0]
        y = steps[1]
        if x < 0:
            self.move_X(abs(x))
            time.sleep(self.time_to_sleep)
        elif x > 0:
            self.move_X(abs(x), 'REVERSE')
            time.sleep(self.time_to_sleep)
        if y < 0:
            self.move_Y(abs(y))
            time.sleep(self.time_to_sleep)
        elif y > 0:
            self.move_Y(abs(y), 'REVERSE')
            time.sleep(self.time_to_sleep)

    # moves the laser in the +ve X direction 
    def move_X(self, steps, direction='FORWARD'):

        # construction of command string
        command = b'$X'
        if (direction == 'FORWARD'):
            command += b'F'
        elif (direction == 'REVERSE'):
            command += b'R'
        N = str(steps)
        command += N.encode()
        command += b';'

        # send the command
        self.media.write(command)
        res = self.media.read()

        # returns the last character - signifying number of legal steps left
        # for the motor
        return res[-1]
    
    # moves the laser in the +ve Y direction
    def move_Y(self, steps,  direction='FORWARD'):

        # construction of command string
        command = b'$Y'
        if (direction == 'FORWARD'):
            command += b'F'
        elif (direction == 'REVERSE'):
            command += b'R'
        N = str(steps)
        command += N.encode()
        command += b';'

        # send the command
        self.media.write(command)
        res = self.media.read()

        # returns the last character - signifying number of legal steps left
        # for the motor
        return res[-1]

    # moves the laser to a particular co-ordinate
    def move_XY(self, steps, x=0, y=0):
        '''
        x and y are integers
        This function moves the laser dot wrt to the center homing position

        returns the offset of x and y from the home position
        '''
        # seeks the origin of the laser frame
        self.seek_home(steps)
        #time.sleep(self.time_to_sleep) 
        if x<0:
            res_x = self.move_X(abs(x))
            time.sleep(self.time_to_sleep)
        elif x>0:
            res_x = self.move_X(abs(x), 'REVERSE')
            time.sleep(self.time_to_sleep)
        if y<0:
            res_y = self.move_Y(abs(y))
            time.sleep(self.time_to_sleep)
        elif y>0:
            res_y = self.move_Y(abs(y), 'REVERSE')
            time.sleep(self.time_to_sleep)

        res = [-x, -y]
        return res

    # releases the serial object
    def release(self):
        # close the media port
        self.media.write(config_commands['OFF'])
        self.media.close()
     
    # reads the output from the remote serial port
    def read(self):
        res = self.media.read()
        return res


def main():
    media = SerialMedia()
    time.sleep(5)
    media.release()

if __name__=='__main__':
    main()
