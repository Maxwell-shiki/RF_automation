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

# 十进制转二进制
def dec2bin(num, bits): 
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num), bits)
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
            return ''.join(l[::-1]).zfill(bits)

# 二进制每位取非
def bin_not(num):
    l = list(str(num))
    for i in range(len(l)):
        l[i] = '1' if l[i] == '0' else '0'
    return ''.join(l)

# 生成code: reg_bank0<24>
def genCode(I, Q):
    I_bin = dec2bin(I, 6)       # I6 I5 I4 I3 I2 I1
    Q_bin = dec2bin(Q, 6)       # Q6 Q5 Q4 Q3 Q2 Q1
    I_not = bin_not(I_bin)      # I6' I5' I4' I3' I2' I1'
    Q_not = bin_not(Q_bin)      # Q6' Q5' Q4' Q3' Q2' Q1'
    
    code = ''
    # reg_bank0<0> ~ reg_bank0<23> 依次为
    # Q1 Q1' Q2 Q2' Q3 Q3' 
    # I1 I1' I2 I2' I3 I3'
    # I4 I4' I5 I5' I6 I6'
    # Q4 Q4' Q5 Q5' Q6 Q6'
    code =  Q_bin[5]+Q_not[5]+Q_bin[4]+Q_not[4]+Q_bin[3]+Q_not[3]+\
            I_bin[5]+I_not[5]+I_bin[4]+I_not[4]+I_bin[3]+I_not[3]+\
            I_bin[2]+I_not[2]+I_bin[1]+I_not[1]+I_bin[0]+I_not[0]+\
            Q_bin[2]+Q_not[2]+Q_bin[1]+Q_not[1]+Q_bin[0]+Q_not[0]
    code = code[::-1]
    code = hex(int(code, 2))
    return '0x' + ''.join(code.split('0x')).zfill(8)

def main():

    # 打开串口, portname记得每次连接的时候看设备管理器修改
    com1 = COMassist(portname="COM6", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    
    # 打开VNA, 记得打开Keysight Connection Expert, 看是GPIB几
    VNA_resource_name = 'GPIB0::16::INSTR'
    VNA = VectorNetworkAnalyzer_3672E(VNA_resource_name)
    VNA.timeout = 3000      # 设置VNA pyvisa的超时时间为3s
    
    # 关闭网分连续模式
    VNA.write("INIT:CONT OFF")

    for code_I in range(0, 64, 8):
        for code_Q in range(0, 64, 8):
            code_out = genCode(code_I, code_Q)
            command = 'reg00=' + code_out + '#'         # 对齐格式

            SPI_returndata = com1.SPI_write(command)
            print(SPI_returndata)                       
            com1.check(SPI_returndata)                  # 检查SPI返回值是否正确

            VNA.write("ABOR;INIT:IMM")                  # 给网分单次激励
            
            startTime = time.time()                     # 计时
            timeout = 30                                # 设置设置一次IQ时激励的总超时时间为30s
            
            while True:
                try: 
                    rsp = VNA.query("*OPC?")            # *OPC?返回1时表示网分扫完一次
                    if rsp == "+1\n":
                        break
                except visa.errors.VisaIOError as ex:
                    if time.time() - startTime > timeout:
                        print("超时: '*OPC?'未及时返回1")
                        break
                    else:
                        continue

            # 保存S参数
            print(VNA.listParam())
            snpfilename = 'I'+ str(code_I) + '_Q' + str(code_Q) + '.s4p'
            VNA.DefaultTest(VNA).saveSNP(ports="1,2,3,4", param="CH1_WIN1_LINE1_PARAM2128", filename=snpfilename, filedir="./data")
            # 注意此处的param参数可能需要根据"CALC1:PAR:CAT?"返回的参数进行修改

            time.sleep(1)

if __name__ == "__main__":
    main()
