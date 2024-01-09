import pyvisa as visa
import numpy as np
import time

class SignalGenerator_1465L():
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.rm = visa.ResourceManager()
        self.sg = self.rm.open_resource(self.resource_name)
        self.sg.read_termination = '\n'
        self.sg.write('*CLS\n')
        print('\n  Connected to Signal Generator: ', self.sg.query('*IDN?'))
    
    def write(self, command):
        self.sg.write(command)
    
    def query(self, command):
        return self.sg.query(command)

    def close(self):
        if self.sg is not None:
            self.sg.close()
            self.sg = None
            print('  Signal Generator connection closed\n')
    
    class Freq:
        # 打开射频输出直接写`OUTP ON`
        def __init__(self, sg):
            self.sg = sg
        def set(self, value):
            self.sg.write(':FREQ %s\n' % value)
        def step(self, value):
            self.sg.write(':FREQ:STEP %s\n' % value)
        def offset(self, value):
            self.sg.write(':FREQ:OFFS %s\n' % value)

    class LFO:
        # 编程文档显示 不支持直流偏置设置
        def __init__(self, sg):
            self.sg = sg
        def freq(self, value):
            self.sg.write(':LFO:FREQ %s\n' % value)
        def ampl(self, value):
            self.sg.write(':LFO:AMPL %s\n' % value)
        def shape(self, value):
            self.sg.write(':LFO:SHAPe %s\n' % value)
        def stat(self, boolean):
            self.sg.write(':LFOutput:STATe %s\n' % boolean)
    
    class Pow:
        def __init__(self, sg):
            self.sg = sg
        def set(self, value):
            self.sg.write(':POW %sdBm\n' % value)
        def offset(self, value):
            self.sg.write(':POW:OFFS %sdB\n' % value)
        def ref(self, stat, value):
            self.sg.write(':POW:REF:STAT %s\n' % stat)
            self.sg.write(':POW:REF %sdBm\n' % value)
        # 衰减设置，环路控制，ALC等还没写，不知道咋用
