import pyvisa as visa
import numpy as np
import re

class SignalGenerator_SMA100B():
    def __init__(self, resource_name):
        self.rm = visa.ResourceManager()
        self.sg = self.rm.open_resource(resource_name)
        self.sg.write('*CLS')
        ID_msg = self.sg.query('*IDN?').replace("\n", "")
        print("\n  Connected to:", ID_msg)

    def write(self, command):
        self.sg.write(command)

    def query(self, command):
        return self.sg.query(command)
    
    def close(self):
        self.sg.close()
        self.rm.close()
        print("  Signal Generator SMA100B Connection closed.\n")

    class Disp:
        def __init__(self, sg):
            self.sg = sg
        def bright(self, value):                    # 调节亮度
            self.sg.write('DISP:BRIG ' + str(value))
        def ann(self, name, state):                 # 打开/关闭显示标注
            self.sg.write('DISP:ANN:%s %s' % (name, state))

    class AM:       # manual p.584
        def __init__(self, sg):
            self.sg = sg
        def state(self, ch, state):
            self.sg.write('SOUR:AM%d:STAT %s' % (ch, state))

    class FM:
        def __init__(self, sg):
            self.sg = sg
        def state(self, ch, state):
            self.sg.write('SOUR:FM%d:STAT %s' % (ch, state))
    
    class PM:
        def __init__(self, sg):
            self.sg = sg
        def state(self, ch, state):
            self.sg.write('SOUR:PM%d:STAT %s' % (ch, state))

    class Freq:     # manual p.664
        def __init__(self, sg):
            self.sg = sg
        def set(self, value):
            self.sg.write('SOUR:FREQ %s' % value)
        def offset(self, value):
            self.sg.write('SOUR:FREQ:OFFS %s' % value)
        def multi(self, value):
            self.sg.write('SOUR:FREQ:MULT %s' % value)

    class Pow:
        def __init__(self, sg):
            self.sg = sg
        def set(self, value):
            self.sg.write('SOUR:POW %s' % value)
        def offset(self, value):
            self.sg.write('SOUR:POW:OFFSET %s' % value)

    class LFO:      # manual p.674
        def __init__(self, sg):
            self.sg = sg
            self.sg.write('SOUR:LFO:STAT ON')
        def shape(self, shape):
            self.sg.write('SOUR:LFO:SHAP %s' % shape)
        def freq(self, value):
            self.sg.write('SOUR:LFO:FREQ %s' % value)
        def voltage(self, value):
            self.sg.write('SOUR:LFO:VOLT %s' % value)
        def offset(self, value):
            self.sg.write('SOUR:LFO:OFFS %s' % value)
    
    # class System:
    #     def __init__(self, sg):
    #         self.sg = sg
    # 准备写些和保存和保护有关的函数，先放着

    # SENSe 相关配件未选，暂时不写
    # HCopy 同
