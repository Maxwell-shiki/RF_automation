import sys, os
import pyvisa as visa

# ========= import modules =========
path_modules = '..\\modules'

for root, dirs, files in os.walk(path_modules):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)

# Ex: sys.path.append("..\\modules\\DCPowerSupply_ES3631A")

from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from Multimeter_3458A import Multimeter_3458A
from SignalGenerator_1465L import SignalGenerator_1465L
from Oscilloscope_MSO64B import Oscilloscope_MSO64B
# 第一个是.py文件名，第二个是class名

# ==================================

def main():
    # PS_resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    # DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    # DCPS.set_voltage(5.0, 1)
    # DCPS.close()
    # error handling is needed

    MM_resource_name = "GPIB0::22::INSTR"
    MM = Multimeter_3458A(MM_resource_name)
    # MM.test()
    MM.set_mode('DCV')
    MM.set_range('DCV', '10')
    Volt_output = MM.get_data()
    print("    Voltage output = ", Volt_output, "V")
    MM.close()

    # type of resource name should have consistency
    # more functions are needed 
    # gpib = 19
    # de = SignalGenerator_1465L(gpib)
    # de.open()

    # de.set_freq('128MHz')
    # # de.set_freq('300MHz', '5MHz')
    # # de.set_freq('500MHz', '10MHz', '0GHz', None, '5')

    # de.set_power('-10dBm')

    # de.get_freq()
    # de.get_power()

    # de.close()

    OSC_resource_name = "USB0::0x0699::0x0530::C051431::0::INSTR"
    OSC = Oscilloscope_MSO64B(OSC_resource_name)
    # OSC.save_img()
    # OSC.save_img('./fig/', 'test')
    # OSC.save_csv()
    OSC.close()


if __name__ == "__main__":
    main()