import time
from datetime import datetime
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyvisa.errors import VisaIOError
from PIL import Image

DEFAULT_TIMEOUT = 10000

class Oscilloscope_MSO64B:
    def __init__(self, resource_name,timeout = DEFAULT_TIMEOUT):
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(resource_name)
        # self.inst.timeout = DEFAULT_TIMEOUT
        self.inst.write('*CLS')
        print(self.inst.query('*IDN?'))
    
    def close(self):
        self.inst.close()
        self.rm.close()

