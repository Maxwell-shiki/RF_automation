import pyvisa as visa
import numpy as np
import re
import sys, os

class VectorNetworkAnalyzer_3672E():
    def __init__(self, resource_name):
        self.rm = visa.ResourceManager()
        self.vna = self.rm.open_resource(resource_name)
        ID_msg = self.vna.query('*IDN?').replace("\n", "")
        print("\n  Connected to:", ID_msg)
    
    def write(self, command):
        self.vna.write(command)
    
    def query(self, command):
        return self.vna.query(command)
    
    def close(self):
        self.vna.close()
        self.rm.close()
        print("  Vector Network Analyzer 3672E Connection closed.\n")
    
    def listParam(self):
        return self.vna.query('CALC1:PAR:CAT?').replace("\n", "")
    
    # 默认情况为S参数二端口测试，此时S2P文件的保存与读取
    # 默认测试流程：
    # 1. 窗口只开了 WIND1
    # 2. 测量曲线为 CH1_WIN1_LINE1_PARAM1
    # 3. S2P测试，有默认参数
    # 4. 默认S2P文件测试为两端口，格式为 # Hz  S  dB  R 50.000
    # 5. ReadSNP()文件返回一个三维矩阵
    # 返回数据格式为: [freq_unit, measurement1, measurement2, measurement3, measurement4]
    class DefaultTest:
        def __init__(self, vna):
            self.vna = vna
        def saveSNP(self, ports="1,2,3,4", param="CH1_WIN1_LINE1_PARAM1", filename="data.s4p", filedir="./data"):
            self.vna.write(':DISP:WIND1:STAT ON')                    # 打开窗口
            self.vna.write(':CALC1:PAR:SEL "%s"' % param)            # 注意要先选择测量再后续操作
            self.vna.write(':MMEM:CDIR "E:\AutoTEST"')
            self.vna.write(':CALC:DATA:SNP:PORTs:SAVE "%s","tmp.s4p"' % ports)
            with open(filedir + "/" + filename, "w") as f:
                f.write(self.vna.query(":MMEM:TRAN? 'tmp.s4p'"))
            self.vna.write(":MMEM:DEL 'tmp.s4p'")
        def readSNP(self, filename, filedir="./data"):
            measurement_pattern = re.compile(r'!S[1-9]+P File: Measurements: (S\d{2}, S\d{2}, S\d{2}, S\d{2}):')
            dataformat_pattern = re.compile(r'# (Hz|GHz|MHz|kHz)  (S)  (RI|dB|MA)  R (\b\d+\.\d{3}\b)')
            with open(os.path.join(filedir, filename), "r") as f:
                lines = f.readlines()
                snpfile = lines[::2]        # 只有奇数行有数据
                for line in snpfile:
                    if measurement_pattern.match(line):
                        measurement = measurement_pattern.match(line).group(1)
                        measurement = measurement.split(", ")
                    if dataformat_pattern.match(line):
                        freq_unit = dataformat_pattern.match(line).group(1)
                        item = dataformat_pattern.match(line).group(2)
                        item_format = dataformat_pattern.match(line).group(3)
                        R_value = dataformat_pattern.match(line).group(4)
                        data_index_start = snpfile.index(line) + 1
            data = []
            for line in snpfile[data_index_start:]:
                data.append(line.split())

            freq = [freq_unit]
            measurement1 = [measurement[0]]
            measurement2 = [measurement[1]]
            measurement3 = [measurement[2]]
            measurement4 = [measurement[3]]
            for line in data:
                freq.append(float(line[0]))
                measurement1.append(complex(float(line[1]), float(line[2])))
                measurement2.append(complex(float(line[3]), float(line[4])))
                measurement3.append(complex(float(line[5]), float(line[6])))
                measurement4.append(complex(float(line[7]), float(line[8])))
            return [freq, measurement1, measurement2, measurement3, measurement4]

    # 自定义测试参数，包括选择测量、扫描类型、频率范围、显示格式、标题、轨迹处理等
    # class SelfdefinedTest:
    #     def __init__(self, vna):
    #         self.vna = vna
