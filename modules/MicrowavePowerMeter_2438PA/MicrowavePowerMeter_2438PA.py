import pyvisa as visa
import numpy as np
import re

# 默认测试通道为通道A，注意使用前校准，然后接线务必注意接口型号对齐
class MicrowavePowerMeter_2438PA:
    def __init__(self, resource_name):
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(resource_name)
        ID_msg = self.scope.query('*IDN?').replace("\n", "")
        print("\n  Connected to:", ID_msg)
    
    def get_freq(self):
        current_freq = self.scope.query('SENS1:FREQ?').replace("\n", "")
        current_freq =  np.format_float_scientific(float(current_freq), precision=3, unique=False, exp_digits=2)
        print("    Frequency = ", current_freq, "Hz now.")
        return current_freq

    def set_freq(self, target_freq):
        print("    Setting frequency to", target_freq, "Hz...")
        self.scope.write('SENS1:FREQ ' + str(target_freq) + 'GHz')
        self.get_freq()
    
    def get_power(self):
        power = self.scope.query('MEAS1?').replace("\n", "")
        power =  float(power)
        # print("    Power = ", power, "dBm now.")
        return power
    
    def close(self):
        self.scope.close()
        self.rm.close()
        # print("  Microwave Power Meter 2438A Connection closed.\n")
