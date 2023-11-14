import pyvisa as visa
import numpy as np
import time

class SignalGenerator_1465L():
    # def __init__(self, resource_name, *args):
    def connect(self, resource_name):
        self.resource_name = resource_name
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(self.resource_name)
        self.inst.read_termination = '\n'
        self.inst.write('*CLS\n')
        print('\n  Connected to Signal Generator: ', self.inst.query('*IDN?'))

        # self.inst.write('*RST\n')
        # 好像每次写复位*RST后面就写不进去了
    def freq(self):
        pass

    def close(self):
        if self.inst is not None:
            self.inst.close()
            self.inst = None
            print('  Signal Generator connection closed\n')

class Freq(SignalGenerator_1465L):
    def set_freq(self, value):
        self.inst.write(':FREQ %s\n' % value)
        print('    Setting frequency:\t\t', value)
    
    def set_step(self, value):
        self.inst.write(':FREQ:STEP %s\n' % value)
        print('    Setting frequency step:\t', value)

    # feat: offset, ref, mult 待写

class LFO(SignalGenerator_1465L):
    def stat(self, value):
        self.inst.write(':LFOutput:STATe %s\n' % value)
        print('    Setting LFO state:\t\t', value)

    def set_freq(self, value):
        self.inst.write(':LFO:FREQ %s\n' % value)
        print('    Setting LFO frequency:\t', value)

    def set_ampl(self, value):
        self.inst.write(':LFO:AMPL %s\n' % value)
        print('    Setting LFO amplitude:\t', value)

    def set_shape(self, value):
        self.inst.write(':LFO:SHAPe %s\n' % value)
        print('    Setting LFO shape:\t\t', value)

    # def get_freq(self):
    #     freq = self.inst.query('FREQ?')
    #     step = self.inst.query('FREQ:STEP?')
    #     # offset = self.inst.query('FREQ:OFFS?')
    #     print('频率为:     \t', freq, ' Hz')
    #     print('频率步进为: \t', step, ' Hz')
    #     # print('频率偏移为: \t', offset, ' Hz')
    #     print()
    
    # def get_power(self):
    #     power = self.inst.query('POW?')
    #     # offset = self.inst.query('POW:OFFS?')
    #     # ref = self.inst.query('POW:REF?')
    #     print('功率为:     \t', power, ' dBm')
    #     # print('功率偏置为: \t', offset, ' dB')
    #     # print('功率参考为: \t', ref, ' dBm')
    #     print()

