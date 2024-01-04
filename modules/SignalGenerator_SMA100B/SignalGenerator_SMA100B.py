import pyvisa as visa
import numpy as np
import re

class SignalGenerator_SMA100B():
    def connect(self, resource_name):
        self.rm = visa.ResourceManager()
        self.sg = self.rm.open_resource(resource_name)
        self.sg.write('*CLS')
        ID_msg = self.sg.query('*IDN?').replace("\n", "")
        print("\n  Connected to:", ID_msg)

    # 自定义输入指令
    def write(self, command):
        self.sg.write(command)
    
    def set_brightness(self, value):
        self.sg.write('DISP:BRIG ' + str(value))
        print("    Setting brightness to", value, "...")

    def close(self):
        self.sg.close()
        self.rm.close()
        print("  Signal Generator SMA100B Connection closed.\n")

class FREQ(SignalGenerator_SMA100B):
    def set_freq(self, value):
        self.sg.write('SOUR:FREQ %s' % value)
        print("    Setting frequency to", value, "Hz ...")

class POW(SignalGenerator_SMA100B):
    def set_pow(self, value):
        self.sg.write('SOUR:POW %s' % value)
        print("    Setting power to", value, "dBm ...")


