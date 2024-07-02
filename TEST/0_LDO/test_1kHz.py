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

    # *********************************************************************
    # 常量设置
    # VDC = 10V
    # VAC = 1 VP-P at 1kHz
    # Iload = 50mA，没用程控

    vdc = 10
    vac = 1
    vac_freq = 1000

    # **********************************************************************
    DCPS.set_voltage(vdc, channel = 2)

    # 改变信号发生器的输入低频频率，观察 示波器 小波峰峰值的变化
    time.sleep(3)
    # MSO.save_img('before', './fig/')
    MSO.save_waveform('0_base', './data/')

    SG.LFO(SG).shape('SINE')
    SG.LFO(SG).freq(vac_freq)
    SG.LFO(SG).ampl(vac)                  # VP-P, max 5V
    SG.LFO(SG).stat('ON')

    time.sleep(3)
    MSO.save_waveform('1_uncensored', './data/')

    wfm2csv('./data/0_base.wfm', './data/0_base.csv')
    wfm2csv('./data/1_uncensored.wfm', './data/1_uncensored.csv')

    print(" Start analyzing base waveform ...")
    csv_data = read_csv('./data/0_base.csv')
    x_list = []
    y_list = []
    for i in range(6, len(csv_data)):
        x_list.append(float(csv_data[i][3].strip()))
        y_list.append(float(csv_data[i][4].strip()))
    y0_max = max(y_list)
    y0_min = min(y_list)
    delta_y0 = y0_max - y0_min
    print('y0_max = ', y0_max)
    print('y0_min = ', y0_min)
    print('delta_y0 = ', delta_y0)

    print(" Start analyzing waveform with ripple ...")
    csv_data = read_csv('./data/1_uncensored.csv')
    x_list = []
    y_list = []
    for i in range(6, len(csv_data)):
        x_list.append(float(csv_data[i][3].strip()))
        y_list.append(float(csv_data[i][4].strip()))
    y_max = max(y_list) - y0_max
    y_min = min(y_list) - y0_min
    delta_y = y_max - y_min
    print('y_max = ', y_max)
    print('y_min = ', y_min)
    print('delta_y = ', delta_y)

    PSRR = 20 * math.log10(1 / delta_y)
    print('PSRR = ', PSRR)
    # 83.34dB






if __name__ == '__main__':
    main()