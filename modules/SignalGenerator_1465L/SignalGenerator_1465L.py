import pyvisa as visa
import numpy as np
import time

class SignalGenerator_1465L():
    def __init__(self, gpib, *args):
        self.gpib = gpib
        self.addr = 'GPIB0::%s::INSTR' % self.gpib
        self.rm = visa.ResourceManager()
    
    def open(self):
        self.inst = self.rm.open_resource(self.addr)
        self.inst.read_termination = '\n'
        self.inst.write('*CLS\n')

        # self.inst.write('*RST\n')
        # 好像每次写复位*RST后面就写不进去了
    
    def close(self):
        if self.inst is not None:
            self.inst.close()
            self.inst = None
    
    def set_freq(self, freq, step=None, offset=None, ref=None, mult=None):
        self.inst.write(':FREQ %s\n' % freq)
        if step is not None:
            self.inst.write(':FREQ:STEP %s\n' % step)
        if offset is not None:
            self.inst.write(':FREQ:OFFS %s\n' % offset)
        if ref is not None:
            self.inst.write(':FREQ:REF %s\n' % ref)
        if mult is not None:
            self.inst.write(':FREQ:MULT %s\n' % mult)
    
    def set_power(self, power, offset=None, ref=None):
        self.inst.write(':POW %s\n' % power)
        if offset is not None:
            self.inst.write(':POW:OFFS %s\n' % offset)
        if ref is not None:
            self.inst.write(':POW:REF:STAT 1\n')
            self.inst.write(':POW:REF %s\n' % ref)

    def get_freq(self):
        freq = self.inst.query('FREQ?')
        step = self.inst.query('FREQ:STEP?')
        # offset = self.inst.query('FREQ:OFFS?')
        print('频率为:     \t', freq, ' Hz')
        print('频率步进为: \t', step, ' Hz')
        # print('频率偏移为: \t', offset, ' Hz')
        print()
    
    def get_power(self):
        power = self.inst.query('POW?')
        # offset = self.inst.query('POW:OFFS?')
        # ref = self.inst.query('POW:REF?')
        print('功率为:     \t', power, ' dBm')
        # print('功率偏置为: \t', offset, ' dB')
        # print('功率参考为: \t', ref, ' dBm')
        print()

