import sys, os
import re
import time
import serial
import serial.tools.list_ports

class COMassist:
    def __init__(self, portname, baudrate, parity, stopbits):
        self.portname = portname
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.ser = serial.Serial(port=self.portname, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopbits)

    def SPI_write(self, command):
        self.command = command
        self.ser.write(command.encode("utf-8"))
        data = self.ser.readline()
        return data

    def check(self, data):
        # 判断返回输出有无出错
        # 正常情况下返回 b'OK!reg00=0xffa55aaa\r\n'
        # 出错情况下返回 b'ERROR!reg00=0xffa55aaa\r\n'
        # 如果出错，停止后续操作
        self.data = data
        if b'ERROR' in self.data:
            print('ERROR: illegal return value!')
            sys.exit(1)


