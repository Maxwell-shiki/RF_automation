import pyvisa as visa
import numpy as np
import time
from datetime import datetime
# from visadore import get


def main():
    rm = visa.ResourceManager()
    # print(rm.list_resources())
    osc = rm.open_resource('USB0::0x0699::0x0530::C051431::0::INSTR')
    print(osc.query('*IDN?'))

    # osc = get("USB0::0x0699::0x0530::C051431::0::INSTR")
    # # print(osc.idn)
    # osc.write("*RST")
    # print(osc.query("*IDN?"))
    # osc.write('SAVE:IMAGe \"C:/Temp/Temp.png\"')
    osc.write('SAV:PLOTData \"C:/Temp/Temp.csv\"')


    dt = datetime.now()

    fileName = dt.strftime("MSO5_%Y%m%d_%H%M%S.csv")

    osc.query('*OPC?')

    # Read image file from instrument
    # osc.write('FILESystem:READFile \"C:/Temp/Temp.csv\"')
    # curveData = osc.read()
    # curveData = osc.query('FILESystem:READFile \"C:/Temp/Temp.csv\"')
    curveData = osc.query_binary_values

    # Save image data to local disk

    file = open(fileName, "wb")
    file.write(curveData)
    file.close()


    # Image data has been transferred to PC and saved. Delete image file from instrument's hard disk.

    osc.write('FILESystem:DELEte \"C:/Temp/Temp.csv\"')

    osc.close()
    rm.close()



if __name__ == "__main__":
    main()