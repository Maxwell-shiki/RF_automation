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
from Multimeter_3458A import Multimeter_3458A
from SignalGenerator_1465L import SignalGenerator_1465L
from MicrowavePowerMeter_2438PA import MicrowavePowerMeter_2438PA
from VectorNetworkAnalyzer_3672E import VectorNetworkAnalyzer_3672E
from DCElectronicLoad_ET5300A import DCElectronicLoad_ET5300A


def main():
    comload = DCElectronicLoad_ET5300A('COM3')

    # comload.constCurrent(1.25)
    # comload.constVoltage(9.2)
    # comload.constCur2Vol(0.82, 7.2)
    # comload.applyload('ON')

    Imax = comload.query('CURR:IMAX?')
    print(Imax)
    comload.write('CURR:IMAX 1.81')
    Imax = comload.query('CURR:IMAX?')
    print(Imax)






if __name__ == '__main__':
    main()