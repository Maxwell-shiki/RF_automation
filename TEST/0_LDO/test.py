import sys, os
import subprocess
import re
import pyvisa as visa
import openpyxl
import serial
import serial.tools.list_ports
import time
import csv
import math

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
# from DCElectronicLoad_ET5300A import DCElectronicLoad_ET5300A   # 好像电子负载没啥用？先放着
from Oscilloscope_MSO64B import Oscilloscope_MSO64B

def wfm2csv(wfm_file, csv_file):
    os.system('.\\ConvertTekWfm.exe {} /CSV {}'.format(wfm_file, csv_file))

def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def main():

    # 仪器链接与对象创建
    PS_resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    DCPS = DCPowerSupply_ES3631A(PS_resource_name)

    SG_resource_name = "GPIB0::19::INSTR"
    SG = SignalGenerator_1465L(SG_resource_name)

    MSO_resource_name = "USB0::0x0699::0x0530::C051431::0::INSTR"
    MSO = Oscilloscope_MSO64B(MSO_resource_name)

    # 需要补充一些示波器的自动化功能
    # 一个是获取某个通道的Measurement中的某个参数
    # 一个是示波器某个通道的函数波形提取

    

if __name__ == '__main__':
    main()