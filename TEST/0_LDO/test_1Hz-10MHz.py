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
import matplotlib.pyplot as plt
import numpy as np

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

    vdc = 12
    vac = 1

    # **********************************************************************
    DCPS.set_voltage(vdc, channel = 2)
    freq_list = []
    PSRR_list = []

    # 改变信号发生器的输入低频频率，观察 示波器 小波峰峰值的变化

    # vac_freq 从 1Hz 到 10MHz
    # 测量一次PSRR，记录下来，vac_freq *10，循环
    # 画图，vac_freq vs PSRR
    # 1Hz, 10Hz, 100Hz, 1kHz, 10kHz, 100kHz, 1MHz, 10MHz

    # 先测一组没有加纹波的
    time.sleep(3)
    MSO.save_waveform('0_base', './data/')
    wfm2csv('./data/0_base.wfm', './data/0_base.csv')
    data = read_csv('./data/0_base.csv')
    v_list = []
    for i in range(6, len(data)):
        v_list.append(float(data[i][4].strip()))
    v0_max = max(v_list)
    v0_min = min(v_list)
    print('    测量基准波形有：')
    print('    V0max = {:.4f}'.format(v0_max))
    print('    V0min = {:.4f}'.format(v0_min))

    for i in range(0, 8):
        vac_freq = 10 ** i
        freq_list.append(vac_freq)

        SG.LFO(SG).shape('SINE')
        SG.LFO(SG).freq(vac_freq)
        SG.LFO(SG).ampl(vac)                  # VP-P, max 5V
        SG.LFO(SG).stat('ON')

        time.sleep(3)
        MSO.save_waveform('1_uncensored', './data/')
        wfm2csv('./data/1_uncensored.wfm', './data/1_uncensored.csv')
        data = read_csv('./data/1_uncensored.csv')
        y_list = []
        for i in range(6, len(data)):
            y_list.append(float(data[i][4].strip()))
        v1_max = max(y_list)
        v1_min = min(y_list)
        delta_v = v1_max - v1_min
        print('    测量频率为{}Hz的波形有: '.format(vac_freq))
        print('      Vmax = {:.4f}'.format(v1_max))
        print('      Vmin = {:.4f}'.format(v1_min))
        print('      Vpp-ripple = {:.4f}'.format(delta_v))
        PSRR = 20 * math.log10(1 / delta_v)
        PSRR_list.append(PSRR)
        print('      PSRR = {:.4f}'.format(PSRR))

    # 画图, 横轴为对数坐标（vac_freq）, 纵轴为PSRR
    x = np.array(freq_list)
    y = np.array(PSRR_list)
    # 作图
    plt.figure()
    plt.plot(x, y, label='100mA')
    plt.xscale('log')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSRR (dB)')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()