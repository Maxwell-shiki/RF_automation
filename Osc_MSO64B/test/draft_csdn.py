# ref to https://blog.csdn.net/qq_27655845/article/details/129602483

import time
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pyvisa.errors import VisaIOError
from PIL import Image

# rm = visa.ResourceManager('@py')
# rm.list_resources()
# Tek = rm.open_resource('TCPIPO::10.163.xxx.xxx::INSTR')
# Tek.timeout=10000
# print(Tek.query('*IDN?'))
# self.inst.write('*RST')
# self.inst.write('AUTOSET EXECUTE')


class Tektronix_DPO:
        def __init__(self):
            self.rm = visa.ResourceManager('@py')
            self.rm.list_resources()
            # self.inst = self.rm.open_resource('TCPIPO::10.163.xxx.xxx::INSTR')
            self.inst = self.rm.open_resource('USB0::0x0699::0x0530::C051431::0::INSTR')           
            self.inst.timeout=10000
            print(self.inst.query('*IDN?'))
            self.inst.write('CLEAR')
            self.inst.write('ACQuire:MODe?')
            self.inst.write('ACQUIRE:STOPAFTER RUNSTOP')
            self.inst.write('ACQuire:STATE RUN')
            self.inst.write('autoset EXECUTE') # autoset
              
        def set_HORIZONTAL(self, POSITION, SCALE):         #horizontal settings
            self.inst.write('HORIZONTAL:POSITION %s'%POSITION)  #position means trigger point on the screen /%
            self.inst.write('HORIZONTAL:SCALE %se-6'%SCALE)     #scale means step /us
  
        def open_ch(self,ch):   # open channal
            self.inst.write('DISplay:GLObal:CH%s:STATE ON'%ch)
  
        def close_ch(self,ch):  # close channal
            self.inst.write('DISplay:GLObal:CH%s:STATE OFF'%ch)
  
        def vertical_ch(self,ch,scale,position):     #channal settings，
            self.inst.write('CH%s:BANDWIDTH FULl'%ch) # at its maximum bandwidth
            self.inst.write('CH%s:SCAle %sE-3'%(ch,scale))     #channal scale/mv
            self.inst.write('CH%s:POSition %s'%(ch,position))  #channal divisions above the center graticule
            self.inst.write('CH%s:COUPLING DC'%ch)     # DC coupling
            self.inst.write('CH%s:TERMINATION 10.0E+5'%ch) #channal input resistence is 1MΩ
  
        def trigger_set(self,ch,level):        #trigger settings
            self.inst.write('TRIGGER:A:EDGE:COUPLING DC')  # DC trigger coupling with input signal to the trigger circuitry
            self.inst.write('TRIGGER:A:EDGE:SOURCE CH%s'%ch)
            self.inst.write('TRIGGER:A:EDGE:SLOPE RISE')   #triggers on the rising edge of the signal
            self.inst.write('TRIGGER:A:LEVEL:CH%s %s'%(ch,level))  # level specifies channal trigger level for seach 1, /V
    
        def begin_trigger(self): #start once trigger action
            self.inst.write('acquire:state 0') # stop
            self.inst.write('acquire:stopafter SEQUENCE') # single
            self.inst.write('acquire:state 1') # run
            self.inst.query('*opc?') # sync
        
        def data_caul(self,ch): #calculate the channal value
            self.inst.write("HEADER 0")
            self.inst.write('DATA:SOURCE CH%s'%ch)
            self.inst.write("DAT:ENC SRI")   # Signed Binary Format, LSB order
            self.inst.write("DAT:WIDTH 1")
            self.inst.write("DAT:START 1")
            recordLength = int(self.inst.query('horizontal:recordlength?'))
            self.inst.write("DAT:STOP {0}".format(recordLength)) # Set data stop to match points available

            # Fetch horizontal scaling factors
            xinc = float(self.inst.query("WFMO:XINCR?"))
            xzero = float(self.inst.query("WFMO:XZERO?"))
            pt_off = int(self.inst.query("WFMO:PT_OFF?"))

            # Fetch vertical scaling factors
            ymult = float(self.inst.query("WFMO:YMULT?"))
            yzero = float(self.inst.query("WFMO:YZERO?"))
            yoff = float(self.inst.query("WFMO:YOFF?"))

            # Fetch waveform data and save as csv file
            rawData = self.inst.query_binary_values('curve?', datatype='b', container=np.array)       
            dataLen = len(rawData)
            t0 = (-pt_off * xinc) + xzero                
            with open('horizonal_vector.csv',mode='w') as file:
                for i in range(0,dataLen):
                    xvalues = t0 + xinc * i # Create timestamp for the data point
                    file.write(str(xvalues))
                    file.write(",") 
                    yvalues= float(rawData[i] - yoff) * ymult + yzero # Convert raw ADC value into a floating point value
                    file.write(str(yvalues))
                    file.write("\n")        
            # plotting the measurement figure
            data = pd.read_csv("horizonal_vector.csv")
            data_x = data.iloc[:,0]
            data_y = data.iloc[:,1]
            plt.plot(data_x, data_y)
            plt.title('channel 1') # plot label
            plt.xlabel('time (seconds)') # x label
            plt.ylabel('voltage (volts)') # y label
            print("look for plot window...")
            plt.savefig('test.png')     #save test picture
            plt.show()
               
        def close(self):
            self.inst.close()
            self.rm.close()
    
        def get_screen(self):
            self.inst.write("HARDCopy:PORT FILE;")
            self.inst.write("EXPort:FORMat PNG")
            self.inst.write("HARDCopy:FILEName \"C:\\est_Temp\\Temp.png\"")
            self.inst.write("HARDCopy STARt")
            self.inst.write("FILESystem:READFile \"C:\\Low_Speed_Test_Temp\\Temp.png\"")
            imgData = self.inst.read_raw()
            dt = datetime.now()
            fileName = dt.strftime("DPO70000_%Y%m%d_%H%M%S.png") # Generate a filename with date and time
            file = open(fileName, "wb")
            file.write(imgData)
            file.close()
            self.inst.write('FILESystem:DELEte \"C:\\Test_Temp\\Temp.png\"') # Delete image file from instrument's hard disk.
            

if __name__ == "__main__":
    
    my=Tektronix_DPO()
    my.set_HORIZONTAL(0,40E-3)
    my.open_ch(1)
    my.vertical_ch(1,200,0)
    my.trigger_set(1,0)
    my.begin_trigger()
    my.data_caul(1)
    my.get_screen()
    my.close()
