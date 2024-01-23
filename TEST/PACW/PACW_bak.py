import sys, os
import subprocess
import pyvisa as visa
import openpyxl

# ========= import modules ================================
path_modules = '..\\modules'

for root, dirs, files in os.walk(path_modules):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)
        
from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from Multimeter_3458A import Multimeter_3458A
from SignalGenerator_1465L import SignalGenerator_1465L
from MicrowavePowerMeter_2438PA import MicrowavePowerMeter_2438PA

# =========================================================

def main():
    # Start Connection
    # 连接好仪器后先开 Keysight connection expert，看看连接情况和IDN
    PS_resource_name = "USB0::0x2A8D::0x1002::MY61002637::0::INSTR"     # ES3631A 直流电源
    DCPS = DCPowerSupply_ES3631A(PS_resource_name)
    MM_resource_name = "GPIB0::22::INSTR"                               # 3458A 万用表
    MM = Multimeter_3458A(MM_resource_name)
    SG_resource_name = "GPIB0::19::INSTR"                               # 1465L 信号源
    SG = SignalGenerator_1465L(SG_resource_name)
    MPM_resource_name = 'GPIB2::13::INSTR'                              # 2438PA 功率计
    MPM = MicrowavePowerMeter_2438PA(MPM_resource_name)
    
    # 设置直流电源
    DCPS.set_voltage(5, channel = 1)
    DCPS.set_current(0.3, channel = 1)
    # 设置万用表量程 mA
    MM.set_measure(set_mode='DCI', set_range=1e-3)
    
    # 初始化列表
    col1 = ["Freq(GHz)"]
    col2 = ["Pin_source(dBm)"]
    col3 = ["Pout_meter(dBm)"]
    col4 = ["I_source(mA)"]

    # 存储进不同的栏
    for freq in range(6, 19, 2):
        # 设置信号源频率
        SG.Freq(SG).set(freq*1e9)                   # GHz
        SG.write('OUTP1 ON')
        # 设置功率计频率
        MPM.set_freq(freq*1e9)                      # GHz
        for Pin_source in range(-30, 6, 1):
            # 设置信号源输出功率
            SG.Pow(SG).set(Pin_source)              # dBm
            # 读取功率计示数 Pout_meter dBm（取10次平均）
            Pout_meter_sum = 0
            for i in range(10):
                Pout_meter_sum += MPM.get_power()
                # MPM.write(*OPC), &judge null?
            Pout_meter = Pout_meter_sum / 10        # dBm
            # 读取万用表的电流示数 I_source mA（取10次平均）
            I_source_sum = 0
            for i in range(10):
                I_source_sum += MM.get_data()
            I_source = I_source_sum / 10            # mA
            # 写入列表
            col1.append(freq)
            col2.append(Pin_source)
            col3.append(Pout_meter)
            col4.append(I_source)
    
    # Close connection
    DCPS.close()
    MM.close()
    SG.close()
    MPM.close()
    
    # 写到excel里
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row in zip(col1, col2, col3, col4):
        sheet.append(row)
    workbook.save("./data/sheet.xlsx")      # add year.month.day.hour.min.sec
    
    print('  Test done.\n')

if __name__ == "__main__":
    main()
