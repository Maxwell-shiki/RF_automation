import time
from datetime import datetime
import pyvisa as visa
import numpy as np
import sys, os
import matplotlib.pyplot as plt
import pandas as pd
from pyvisa.errors import VisaIOError
from PIL import Image

DEFAULT_TIMEOUT = 10000

class Oscilloscope_MSO64B:
    def __init__(self, resource_name,timeout=DEFAULT_TIMEOUT):
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(resource_name)
        # self.inst.timeout = DEFAULT_TIMEOUT
        self.inst.write('*CLS')
        print('\n  Connected to Oscilloscope: ', self.inst.query('*IDN?').strip('\n'))
        # print("\n  Connected to Oscilloscope: ", self.inst.query('*IDN?'))

    def reset(self):
        self.inst.write('*RST')
        print("    Oscilloscope MSO64B reseted.")

    def save_img(self, filename=None, path=None):
        # set filename
        if filename == None:
            dt = datetime.now()
            filename = dt.strftime("OSC_image_%Y%m%d_%H%M%S.png")
        else:
            filename = filename + '.png'

        # set path
        if path == None:
            path = './img/'
            os.makedirs(path, exist_ok=True)
        else:
            # Ex: path = './fig/2023-01-01/'
            os.makedirs(path, exist_ok=True)

        self.inst.write('SAVE:IMAGe \"C:/Temp/Temp.png\"')
        self.inst.query('*OPC?')
        self.inst.write('FILESystem:READFile \"C:/Temp/Temp.png\"')
        imgData = self.inst.read_raw(1024*1024)
        file = open("{}{}".format(path, filename), "wb")
        file.write(imgData)
        file.close()
        self.inst.write('FILESystem:DELEte \"C:/Temp/Temp.png\"')
        print("    Image saved as: ", path+filename)

    def save_waveform(self, filename=None, path=None):
        # set filename
        if filename == None:
            dt = datetime.now()
            filename = dt.strftime("OSC_waveform_%Y%m%d_%H%M%S.wfm")
        else:
            filename = filename + '.wfm'
        # set path
        if path == None:
            path = './data/'
            os.makedirs(path, exist_ok=True)
        else:
            os.makedirs(path, exist_ok=True)
        # save, read, to local PC, and delete
        self.inst.write('SAVE:WAVEFORM CH1, "C:/Temp/Temp.wfm"')
        self.inst.query('*OPC?')
        self.inst.write('FILESystem:READFile \"C:/Temp/Temp.wfm\"')
        data = self.inst.read_raw()
        file = open("{}{}".format(path, filename), "wb")
        file.write(data)
        file.close()
        self.inst.write('FILESystem:DELEte \"C:/Temp/Temp.wfm\"')
        print("    Waveform saved as: ", path+filename)

    # def save_csv(self, filename=None, path=None):
    #     # set filename
    #     if filename == None:
    #         dt = datetime.now()
    #         filename = dt.strftime("OSC_data_%Y%m%d_%H%M%S.csv")
    #     else:
    #         filename = filename + '.wfm'
    #     # set path
    #     if path == None:
    #         path = './data/'
    #         os.makedirs(path, exist_ok=True)
    #     else:
    #         os.makedirs(path, exist_ok=True)
    #     # save, read, to local PC, and delete
    #     # self.inst.write('SAVEONEVENT:WAVEform:SOURCE CH1')
    #     # self.inst.write('SAVEONEVENT:WAVEform:FILEFormat SPREADSheet')  # CSV
    #     # # self.inst.write('SAVEONEVENT:FILEName "temp_a"')
    #     # self.inst.write('SAVEONEVENT:FILEDest "C:/Temp"')
    #     # self.inst.write('MEASUrement:ADDMEAS TIE')
    #     # self.inst.write('SAVE:PLOTDATA "C:/Temp/plot1.csv"')

    # file is too large, timeout expire
    # def copyfile(self, srcfile, dstfile, path=None):
    #     # set path
    #     if path == None:
    #         path = './local_copy/'
    #         os.makedirs(path, exist_ok=True)
    #     else:
    #         os.makedirs(path, exist_ok=True)
    #     self.inst.write('FILESystem:READFile %s' % srcfile)
    #     data = self.inst.read_raw()
    #     file = open("{}{}".format(path, dstfile), "wb")
    #     file.write(data)
    #     file.close()
    #     print("    File copied as: ", path+dstfile)

    def sample_and_plot(self):
        # io config
        self.inst.write('header 0')
        self.inst.write('data:encdg SRIBINARY')
        self.inst.write('data:source CH1')                          # channel 1
        self.inst.write('data:start 1')                             # first sample
        record = int(self.inst.query('horizontal:recordlength?'))
        self.inst.write('data:stop {}'.format(record))              # wave data length
        self.inst.write('wfmoutpre:byt_n 2')                        # 2 byte per data point
                                                                # > 8bit, so 2 bytes
        # # acq config
        # self.inst.write('acquire:state 0')                          # stop acq
        # # self.inst.write('acquire:stopafter sequence')             # single (单个波形)
        # self.inst.write('acquire:stopafter runstop')                # runstop (连续运行)
        # self.inst.write('acquire:state 1')                          # start acq
        # r = self.inst.query('*OPC?')                                # sync

        # data query
        bin_wave = self.inst.query_binary_values('curve?', datatype='h', container=np.array)

        # retrieve scaling factors
        tscale = float(self.inst.query('wfmoutpre:xincr?'))
        tstart = float(self.inst.query('wfmoutpre:xzero?'))
        vscale = float(self.inst.query('wfmoutpre:ymult?'))         # V/div
        voff = float(self.inst.query('wfmoutpre:yzero?'))           # reference voltage
        vpos = float(self.inst.query('wfmoutpre:yoff?'))            # reference position

        # error checking
        r = int(self.inst.query('*ESR?'))

        self.inst.close()
        # rm.close()

        # create scaled vectors
        # horizontal (time)
        total_time  = tscale * record
        tstop = tstart + total_time
        scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)

        # vertical (voltage)
        unscaled_wave = np.array(bin_wave, dtype='double')   # data type conversion
        scaled_wave = (unscaled_wave - vpos) * vscale + voff
        print('    Sample and plot completed.')

        # plot
        plt.plot(scaled_time, scaled_wave)
        plt.title('Oscilloscope Waveform Channel 1')        # plot label
        plt.xlabel('time (seconds)')                        # x-axis label
        plt.ylabel('voltage (volts)')                       # y-axis label
        plt.grid(which='major', color='gray', linestyle='--', alpha=0.7)
        plt.grid(which='minor', color='gray', linestyle=':', alpha=0.4)
        plt.minorticks_on()
        plt.show()

    def close(self):
        self.inst.close()
        self.rm.close()
        # print("  Oscilloscope MSO64B closed.\n")

