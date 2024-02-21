import sys, os
import subprocess
import re
import pyvisa as visa
import openpyxl
import serial
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

from COMassist import COMassist

def main():

    com1 = COMassist(portname="COM4", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    
    # VNA_resource_name = 'GPIB0::16::INSTR'
    # VNA = VectorNetworkAnalyzer_3672E(VNA_resource_name)

    for code_I in range(0, 64):
        for code_Q in range(0, 64):
            # 生成command
            code_I1 = code_I % 2 * 1 + (code_I % 2 == 0) * 2 + code_I // 2 % 2 * 4 + (code_I // 2 % 2 == 0) * 8 + code_I // 4 % 2 * 16 + \
                (code_I // 4 % 2 == 0) * 32 + code_I // 8 % 2 * 64 + (code_I // 8 % 2 == 0) * 128 + code_I // 16 % 2 * 256 + \
                (code_I // 16 % 2 == 0) * 512 + code_I // 32 % 2 * 1024 + (code_I // 32 % 2 == 0) * 2048
            code_Q1 = code_Q % 2 * 1 + (code_Q % 2 == 0) * 2 + code_Q // 2 % 2 * 4 + (code_Q // 2 % 2 == 0) * 8 + code_Q // 4 % 2 * 16 + \
                (code_Q // 4 % 2 == 0) * 32 + code_Q // 8 % 2 * 64 + (code_Q // 8 % 2 == 0) * 128 + code_Q // 16 % 2 * 256 + \
                (code_Q // 16 % 2 == 0) * 512 + code_Q // 32 % 2 * 1024 + (code_Q // 32 % 2 == 0) * 2048
            code_out = (code_Q1 << 12) + code_I1 + 0xff000000
            code_out = hex(code_out)
            # print("code_out =", code_out)
            command = 'reg00=' + code_out + '#'

            SPI_returndata = com1.SPI_write(command)
            print(SPI_returndata)

            com1.check(SPI_returndata)

            time.sleep(1)

            # 保存S参数
            # VNA.listParam()
            # snpfilename = command + '.s4p'
            # VNA.DefaultTest(VNA).saveSNP(ports="1,2,3,4", param="CH1_WIN1_LINE1_PARAM1", filename=snpfilename, filedir="./data")

if __name__ == "__main__":
    main()
