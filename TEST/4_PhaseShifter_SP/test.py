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

def dec2bin(num, bits): 
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num), bits)
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
            return ''.join(l[::-1]).zfill(bits)

def bin_not(num):
    l = list(str(num))
    for i in range(len(l)):
        l[i] = '1' if l[i] == '0' else '0'
    return ''.join(l)

def genCode(I, Q):
    I_bin = dec2bin(I, 6)
    Q_bin = dec2bin(Q, 6)
    I_not = bin_not(I_bin)
    Q_not = bin_not(Q_bin)
    
    code = ''
    
    # reg_bank0<0> ~ reg_bank0<23> 依次为
    # Q1 Q1' Q2 Q2' Q3 Q3' 
    # I1 I1' I2 I2' I3 I3'
    # I4 I4' I5 I5' I6 I6'
    # Q4 Q4' Q5 Q5' Q6 Q6'
    for i in range(3):
        code += Q_bin[i] + Q_not[i]
    for i in range(6):
        code += I_bin[i] + I_not[i]
    for i in range(3, 6):
        code += Q_bin[i] + Q_not[i]
    
    # 左边是低位，右边是高位，故倒序
    code = code[::-1]
    
    code = hex(int(code, 2))        # bin序列转hex序列
    
    return code 

def main():

    com1 = COMassist(portname="COM6", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    
    # VNA_resource_name = 'GPIB2::16::INSTR'
    # VNA = VectorNetworkAnalyzer_3672E(VNA_resource_name)

    for code_I in range(63, 64):
        for code_Q in range(63, 64):
            code_out = genCode(code_I, code_Q)
            # print("code_out =", code_out)
            command = 'reg00=' + code_out + '#'

            SPI_returndata = com1.SPI_write(command)
            print(SPI_returndata)
            com1.check(SPI_returndata)

            # time.sleep(1)

            # 保存S参数
            # print(VNA.listParam())
            # snpfilename = 'I'+code_I + '/Q'+code_Q + ': ' + command + '.s4p'
            # # snpfilename = command + '.s4p'
            # VNA.DefaultTest(VNA).saveSNP(ports="1,2,3,4", param="CH1_WIN1_LINE1_PARAM1", filename=snpfilename, filedir="./data")

if __name__ == "__main__":
    main()
