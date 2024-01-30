import sys, os
import subprocess
import pyvisa as visa

# ========= import modules ================================
path_modules = '..\\modules'

for root, dirs, files in os.walk(path_modules):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)

# Ex: sys.path.append("..\\modules\\DCPowerSupply_ES3631A")

# 第一批调试的设备
from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from Multimeter_3458A import Multimeter_3458A
# from SignalGenerator_1465L import SignalGenerator_1465L, Freq, LFO
from SignalGenerator_1465L import SignalGenerator_1465L
from Oscilloscope_MSO64B import Oscilloscope_MSO64B

# 第二批调试的设备
from MicrowavePowerMeter_2438PA import MicrowavePowerMeter_2438PA
from SignalGenerator_SMA100B import SignalGenerator_SMA100B

# =========================================================

def main():
    # **********************  电源  ********************************************************
    # PS_resource_name = "USB0::0x2A8D::0x1002::MY61002637::0::INSTR"
    # DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    # # 默认启动时*RST

    # DCPS.set_voltage(3.3, channel = 1)
    # DCPS.set_current(0.5, channel = 1)
    # print("    Voltage output = ", DCPS.get_voltage(channel = 1), "V")
    # print("    Current output = ", DCPS.get_current(channel = 1), "A")

    # DCPS.close()
    # **************************************************************************************

    # **********************  万用表  *******************************************************
    # MM_resource_name = "GPIB0::22::INSTR"
    # MM = Multimeter_3458A(MM_resource_name)

    # MM.set_measure(set_mode='DCV', set_range=10)
    # voltage = MM.get_data()
    # print("    Voltage output = ", voltage, "V")

    # MM.close()
    # **************************************************************************************

    # **********************  信号源 1465L  ************************************************
    # SG_resource_name = "GPIB0::19::INSTR"
    # SG = SignalGenerator_1465L(SG_resource_name)

    # SG.write('*RST')

    # 连续波输出，<67GHz
    # SG.Freq(SG).set(6e5)          # Hz
    # SG.write('OUTP ON')

    # # LDO低频输出，<10MHz
    # SG.LFO(SG).shape('RAMP')      # 'SINE, SQU, TRI, RAMP, NOIS, SWEP'
    # SG.LFO(SG).freq(2e4)
    # SG.LFO(SG).stat('ON')

    # # 输出功率电平
    # SG.Pow(SG).set(-10)             # [-135dBm, +30dBm]
    # # SG.Pow(SG).offset(2)            # [-100dB, +100dB]
    # SG.Pow(SG).ref('ON', -60)         # [-135dBm, +30dBm]

    # SG.close()
    # *************************************************************************************

    # **********************  示波器  *****************************************************
    # MSO_resource_name = "USB0::0x0699::0x0530::C051431::0::INSTR"
    # MSO = Oscilloscope_MSO64B(MSO_resource_name)
    # MSO.save_img()
    # MSO.save_img('test', './fig/')
    # MSO.save_waveform('tmp', './data/')

    # transfer .wfm to .csv
    # os.chdir('./data/')
    # os.system(".\ConvertTekWfm.exe .\\tmp.wfm /CSV tek000.csv > nul 2>&1")

    # MSO.sample_and_plot()

    # SG.close()
    # MSO.close()
    # *************************************************************************************

    # **********************  功率计  *****************************************************
    # MPM_resource_name = 'GPIB1::13::INSTR'
    # MPM = MicrowavePowerMeter_2438PA(MPM_resource_name)
    # # freq = MPM.get_freq()
    # MPM.set_freq(32)
    # power = MPM.get_power()
    # print("    Power = ", power, "dBm now.")

    # MPM.close()
    # *************************************************************************************

    # **********************  信号源SMA100B  **********************************************
    # SG_resource_name = 'TCPIP0::SMA100B-106560::hislip0::INSTR'
    # SG = SignalGenerator_SMA100B(SG_resource_name)

    # # MAIN system
    # SG.write('*RST')

    # DISPlay subsystem
    # SG.Disp(SG).bright(14)
    # SG.Disp(SG).ann('FREQ', 'ON')     # 'FREQ, AMPL, ALL'

# 问下 AM FM PM使用时需要设置哪些参数

    # AM subsystem
    # SG.AM(SG).state(ch=1, state='OFF')

    # FM subsystem
    # SG.FM(SG).state(ch=1, state='OFF')

    # PM subsystem
    # SG.PM(SG).state(ch=1, state='OFF')

    # LFO subsystem
    # SG.LFO(SG).shape('SINE')     # 'SIN, SQUare, PULSe, TRIangle, TRAPeze'
    # SG.LFO(SG).freq(2e4)         # Hz
    # SG.LFO(SG).voltage(1.5)      # V
    # # SG.LFO(SG).offset(1.65)      # V

    # FREQuency subsystem
    # 默认设置模式为CW/FIXED，函数内没写修改模式的指令
    # SG.Freq(SG).set(6e9)
    # SG.Freq(SG).offset(2e9)
    # SG.Freq(SG).multi(1.5)
    # print('    Frequency =', SG.query('SOUR:FREQ:CW?').replace('\n',''), 'Hz')

    # POWer subsystem
    # SG.write('POW:EMF:STAT 1')     
        # activeates display of the signal level as voltage of the EMF (no-load voltage)
        # If disabled, the level is displayed as a voltage over a 50 Ohm load
    # SG.Pow(SG).set(-10)     # dBm
    # SG.Pow(SG).offset(2)    # dB
    # print('    Level =', SG.query('SOUR:POW?').replace('\n',''), 'dBm')

    # 输出信号
    # SG.write('OUTP1 ON')

    # print(SG.query('SYST:ERR?'))

    # END
    # SG.write('OUTP1 OFF')
    # SG.write('*RST')
    # SG.close()
    # *************************************************************************************

    print('  Test done.\n')


    # 测试代码例子也重新写一遍另外放在一个文件夹里，这个文件夹只用来引用


if __name__ == "__main__":
    main()
