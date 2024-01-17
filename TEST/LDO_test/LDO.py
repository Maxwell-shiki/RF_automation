import sys, os
import subprocess
import pyvisa as visa

# ========= import modules ================================
path_modules = '..\\..\\modules'

for root, dirs, files in os.walk(path_modules):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)

# Ex: sys.path.append("..\\modules\\DCPowerSupply_ES3631A")

from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from Multimeter_3458A import Multimeter_3458A
# from SignalGenerator_1465L import *
from SignalGenerator_1465L import SignalGenerator_1465L, Freq, LFO
from Oscilloscope_MSO64B import Oscilloscope_MSO64B

# =========================================================

def main():
    # connect
    SG_resource_name = "GPIB1::19::INSTR"
    SG = LFO()
    SG.connect(SG_resource_name)
    SG.stat('ON');
    MSO_resource_name = "USB0::0x0699::0x0530::C051431::0::INSTR"
    MSO = Oscilloscope_MSO64B(MSO_resource_name)

    # set parameter and test
    
    SG.set_freq('100Hz'); SG.set_ampl('2VPP'); SG.set_shape('SINE')


    print('\n  Test done.\n')


if __name__ == "__main__":
    main()