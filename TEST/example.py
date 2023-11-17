import sys, os
import subprocess
import pyvisa as visa

# ========= import modules ================================
path_modules = '..\\modules'

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
    PS_resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    DCPS.set_voltage(5.0, 1)
    DCPS.set_current(0.5, 1)
    DCPS.close()
    # error handling is needed

    MM_resource_name = "GPIB0::22::INSTR"
    MM = Multimeter_3458A(MM_resource_name)
    # MM.test()
    MM.set_mode('DCV')
    MM.set_range('DCV', '10')
    Volt_output = MM.get_data()
    print("    Voltage output = ", Volt_output, "V")
    MM.close()

    # more functions are needed 

    SG_resource_name = "GPIB1::19::INSTR"
    # SG = Freq()
    # SG.connect(SG_resource_name)
    # SG.set_freq('10GHz')
    # SG.set_step('1MHz')
    SG = LFO()
    SG.connect(SG_resource_name)
    SG.stat('ON');
    SG.set_freq('20KHz'); SG.set_ampl('2VPP'); SG.set_shape('SINE')
    # SG.stat('OFF');
    # SG.close()

    MSO_resource_name = "USB0::0x0699::0x0530::C051431::0::INSTR"
    MSO = Oscilloscope_MSO64B(MSO_resource_name)
    # MSO.save_img()
    # MSO.save_img('test', './fig/')
    MSO.save_waveform('tmp', './data/')

    # transfer .wfm to .csv
    os.chdir('./data/')
    os.system(".\ConvertTekWfm.exe .\\tmp.wfm /CSV tek000.csv > nul 2>&1")

    # MSO.sample_and_plot()

    # SG.close()
    # MSO.close()

    print('\n  Test done.\n')


if __name__ == "__main__":
    main()