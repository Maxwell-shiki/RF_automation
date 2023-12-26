import pyvisa as visa
import numpy as np
import re

# 这是没有模块化的版本
def main():
    rm = visa.ResourceManager()
    resource_name = 'GPIB0::13::INSTR'

    mpm = rm.open_resource(resource_name)

    ID_msg = mpm.query('*IDN?').replace("\n", "")
    print("Connected to:", ID_msg)

    freq = mpm.query('SENS1:FREQ?').replace("\n", "")
    freq =  np.format_float_scientific(float(freq), precision=3, unique=False, exp_digits=2)
    print("Frequency = ", freq, "Hz now.")
    print()

    print("Setting frequency to 32 Hz...")
    freq = 32
    mpm.write('SENS1:FREQ ' + str(freq) + 'GHz')
    freq = mpm.query('SENS1:FREQ?').replace("\n", "")
    freq =  np.format_float_scientific(float(freq), precision=3, unique=False, exp_digits=2)
    print("Frequency = ", freq, "Hz now.")
    print()

    print("Power meter start measurement...")
    mpm.write('INIT1:CONT ON') # 这句想写就写，可以不写，好像用起来只有通道A
    power = mpm.query('MEAS1?').replace("\n", "")
    power =  float(power)
    print("Power = ", power, "dBm now.")
    print()

if __name__ == "__main__":
    main()
