import pyvisa as visa
import re
import time
import numpy as np
import sys, os

def main():
    rm = visa.ResourceManager()
    resource_name = 'USB0::0x0699::0x0503::B030477::0::INSTR'

    scope = rm.open_resource(resource_name)
    ID_msg = scope.query_ascii_values('*IDN?', converter='s', separator='\r\n')
    print("Connected to:", ID_msg[0], "now")

    # filename = "D:\RF_automation\modules\ArbitraryWaveformGenerator_AWG5204\draft\Equation_files\sin.equ"

    scope.write('FILESystem:READFile \"C:/Program Files/Tektronix/AWG5200/Documentation/AWG5200/AWG5200.chw\"')
    data = scope.read_raw()
    file = open("./Equation_files/help", "wb")
    file.write(data)
    file.close()

    scope.close()


if __name__ == "__main__":
    main()