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
        print("\n  Connected to Oscilloscope: ", self.inst.query('*IDN?'))

    def reset(self):
        self.inst.write('*RST')
        print("    Oscilloscope MSO64B reseted.")

    def save_img(self, path=None, filename=None):
        if path == None:
            path = './img/'
            os.makedirs(path, exist_ok=True)
        else:
            # Ex: path = './fig/2023-01-01/'
            os.makedirs(path, exist_ok=True)
        self.inst.write('SAVE:IMAGe \"C:/Temp/Temp.png\"')
        if filename == None:
            dt = datetime.now()
            filename = dt.strftime("Osc_%Y%m%d_%H%M%S.png")
        else:
            filename = filename + '.png'
        self.inst.query('*OPC?')
        self.inst.write('FILESystem:READFile \"C:/Temp/Temp.png\"')
        imgData = self.inst.read_raw(1024*1024)
        file = open("{}{}".format(path, filename), "wb")
        file.write(imgData)
        file.close()
        self.inst.write('FILESystem:DELEte \"C:/Temp/Temp.png\"')

    def 

    
    def close(self):
        self.inst.close()
        self.rm.close()

