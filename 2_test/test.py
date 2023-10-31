import pyvisa as visa
import re
import numpy as np
import matplotlib.pyplot as plt

def main():
    rm = visa.ResourceManager()
    # print(rm.list_resources())

    # configure power supply
    ps = rm.open_resource('USB0::0x2A8D::0x1002::MY61003060::0::INSTR')
    print(ps.query('*IDN?'))
    ps.write('*RST')
    ps.write('APPL CH1, 5.0')
    ps.write('OUTP ON, (@1)')
    output = ps.query('MEAS:VOLT? P25V')
    print('output: ', output)



    

if __name__ == "__main__":
    main()

