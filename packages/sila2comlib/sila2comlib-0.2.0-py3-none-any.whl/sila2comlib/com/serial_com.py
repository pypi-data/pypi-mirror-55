"""
________________________________________________________________________

:PROJECT: labPy

*serial_communication: serial communication interface simulation*

:details: serial interface simulation.

:file:    serial_sim.py

:author:  mark doerr <mark.doerr@uni.greifswald.de> :

:date: (creation)          20181228
:date: (last modification) 20190110
.. note::
.. todo::

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
  For further Information see COPYING file that comes with this distribution.
________________________________________________________________________

"""

__version__ = "0.0.1"

import logging

import os
import sys
import glob
import threading
import time

import serial

import csv
from datetime import datetime

import sys
import os
import re

# chose an implementation, depending on os
#~ if sys.platform == 'cli':
#~ else:
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
#~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

def listOpenPorts(check_open=True, include_links=False, verbose=True):
    """Lists all open serial ports.

    ports are tested if they can be opened
    hits = 0
    """
    detected_ports = []

    iterator = sorted(comports(include_links=include_links))
    # list the ports
    for n, (port, description, hwid) in enumerate(iterator, 1):
        detected_ports.append(port)

        # portinfo.append( [port, description, hwid] ) # for more information
        if verbose:
            sys.stdout.write(f"\tport        : {port}\n")
            sys.stdout.write(f"\tdescription : {description}\n")
            sys.stdout.write(f"\thardw.-ID   : {hwid}\n")

    if len(detected_ports) > 0:
        if verbose:
            sys.stdout.write("\tlistOpenPorts: {} serial port(s) found.\n".format(len(detected_ports)))
    else:
        sys.stderr.write(f"ERROR(sila2comlib.listOpenPorts): no serial ports found!\n")
        return detected_ports

    #
    # for port in serial.tools.list_ports.comports():
    #     if port[2] != 'n/a':
    #         info = [port.device, port.name, port.description, port.hwid]
    #         portinfo.append(info)
    # return portinfo

    # check, if they are open
    if check_open:
        open_ports = []
        for port in detected_ports:
            try:
                s = serial.Serial(port)
                s.close()
                open_ports.append(port)
                if verbose:
                    sys.stdout.write("open serial port: {}\n".format(port))
            except (OSError, serial.SerialException) as err:
                sys.stderr.write(f"SerialPortException- {err}")

        logging.debug(open_ports)
        return open_ports
    else :
        return detected_ports

class Connection:
    """High level SerialConnection handling serial port connections.
    """
    def __init__(self, port="",
                 baudrate=0,
                 timeout=1,
                 reset_buffers=True, verbose=False):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.reset_buffers = reset_buffers
        self.verbose = verbose

    def open(self):
        logging.debug("opening port ...")
        try:
            self.ser = serial.Serial()
            self.ser.baudrate = self.baudrate
            self.ser.port = self.port
            self.ser.timeout = self.timeout
            self.ser.open()
            if self.ser.isOpen():
                if self.verbose:
                    print(f"Serial port [{self.port}] opened.")
                # flushing the I/O-buffers
                if self.reset_buffers:
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
        except Exception as err:
            if self.verbose:
                print(f'Failed to connect to port [{self.port}].')
                print(err)
            pass

    def close(self):
        self.ser.close()
        if self.verbose:
            print(f"Connection to serial port [{self.port}] closed.")

    def sendCommand(self, command, terminator='\r', resp_delay=0.5):
        try:
            arg = bytes(str(command + terminator), 'utf8')
            self.ser.write(arg)
            time.sleep(resp_delay)
            response = self.getResponse()
            return response

        except TypeError as err:
            if self.verbose:
                print(err)
            self.ser.close()

    def getResponseList(self):
        try:
            response_list = []
            while True:
                response = self.ser.readlines()
                for line in response:
                    line = line.strip(b'\n').decode('utf8')
                    line = line.strip('\r')
                    if self.verbose:
                        print(line)
                    response_list.append(line)
                break
            return response_list
        except TypeError as e:
            if self.verbose:
                print(e)
            self.closeConnection()
        except Exception as f:
            if self.verbose:
                print(f)
            self.closeConnection()

    def getResponse(self):
        try:
            response_list = []
            while True:
                response = self.ser.readlines()
                for line in response:
                    line = line.strip(b'\n').decode('utf8')
                    line = line.strip('\r')
                    if self.verbose:
                        print(line)
                    response_list.append(line)
                break
            return response_list[0]
        except TypeError as e:
            if self.verbose:
                print(e)
            self.closeConnection()
        except Exception as f:
            if self.verbose:
                print(f)
            self.closeConnection()

    def readline(self):
        return self.ser.readline()

    def readlines(self):
        return self.ser.readlines()
