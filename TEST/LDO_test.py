import sys, os

# 相对路径导入
sys.path.append("..\\modules\\DCPowerSupply_ES3631A")
from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
# 第一个是.py文件名，第二个是class名

sys.path.append("..\\modules\\Multimeter_3458A")
from Multimeter_3458A import Multimeter_3458A

sys.path.append("..\\modules\\SignalGenerator_1465L")
from SignalGenerator_1465L import SignalGenerator_1465L

import pyvisa as visa


def main():
    # 要不下次把resource_name都缩短点
    PS_resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    DCPS.set_voltage(5.0, 1)
    DCPS.close()

    # MM_resource_name = "GPIB0::22::INSTR"
    # MM = Multimeter_3458A(MM_resource_name)
    # # MM.test()
    # MM.set_mode('DCV')
    # MM.set_range('DCV', '10')
    # Volt_output = MM.get_data()
    # print("    Voltage output = ", Volt_output, "V")
    # MM.close()

    SG_gpib = 19
    SG = 

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



if __name__ == "__main__":
    main()