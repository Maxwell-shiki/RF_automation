import sys, os
import subprocess
import re
import pyvisa as visa
import openpyxl
import serial
import serial.tools.list_ports
import time

# ========= import modules ================================
path_devices = '..\\..\\modules'
for root, dirs, files in os.walk(path_devices):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)

path_scripts = '..\\..\\scripts'
for root, dirs, files in os.walk(path_scripts):
    for directory in dirs:
        path_script = os.path.join(root, directory)
        sys.path.append(path_script)

from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from SignalGenerator_1465L import SignalGenerator_1465L
# from DCElectronicLoad_ET5300A import DCElectronicLoad_ET5300A
from Oscilloscope_MSO64B import Oscilloscope_MSO64B


def main():

    # PS_resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    # DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    # # DCPS.set_voltage(3.1, channel = 1)


    # comload = DCElectronicLoad_ET5300A('COM8')
    # # comload.constCurrent(0.2)
    # # comload.constVoltage(9.2)
    # # comload.constCur2Vol(0.82, 7.2)
    # comload.applyload('ON')

    # # SG_resource_name = "GPIB0::19::INSTR"

    # # MSO_resource_name = "USB0::0x0699::0x0401::C011422::0::INSTR"

    # **********************************************************************

    










if __name__ == '__main__':
    main()