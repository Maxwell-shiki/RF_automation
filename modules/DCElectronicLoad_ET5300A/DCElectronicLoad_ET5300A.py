import pyvisa as visa
import re
import time
import serial
import serial.tools.list_ports

class DCElectronicLoad_ET5300A:
    def __init__(self, portname):
        self.comload = serial.Serial(port=portname, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        # 确认链接
        cmd = '*IDN?\n'
        self.comload.write(cmd.encode("utf-8"))
        ID_msg = self.comload.readline()
        ID_msg = str(ID_msg)[2:-5]
        print("\n  Connected to:", ID_msg)

    def write(self, command):
        command = command + '\n'
        self.comload.write(command.encode("utf-8"))
    
    def query(self, command):
        command = command + '\n'
        self.comload.write(command.encode("utf-8"))
        data = self.comload.readline()
        data = str(data)[2:-5]
        return data

    def applyload(self, stat):
        if stat == 'ON' or stat == '1':
            self.write('CH:SW ON')
        elif stat == 'OFF' or stat == '0':
            self.write('CH:SW OFF')
        else:
            print('Invalid command!')
        time.sleep(1)

    def constCurrent(self, current):
        self.write('CH:MODE CC')
        time.sleep(1)
        self.write('CURR:CC ' + str(current))
        time.sleep(1)
    
    def constVoltage(self, voltage):
        self.write('CH:MODE CV')
        time.sleep(1)
        self.write('VOLT:CV ' + str(voltage))
        time.sleep(1)


# 还需要写一个切换量程的，见手册2.3.1
