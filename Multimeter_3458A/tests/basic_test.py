import pyvisa as visa
import re
import time
import numpy as np

def main():
    rm = visa.ResourceManager()

    print("%d devices are now connected to the computer: " % len(rm.list_resources()))
    # show all the devices connected to the computer
    # count the list of devices
    print("  ", rm.list_resources())

    # since the Multimeter 3458A is connected to the computer via GPIB, 
    # you can see the resource name in the list of devices listed above
    resource_name = 'GPIB0::22::INSTR'

    scope = rm.open_resource(resource_name)
    scope.write('END ON');

    ID_msg = scope.query_ascii_values('ID?', converter='s', separator='\r\n')
    print("Connected to:", ID_msg[0], "now")

    scope.write('FUNC DCV')
    scope.write('OHM 1')

    # # print("Start to ")
    # scope.write("FUNC OHM")   
    # # scope.write('OHM 1')
    # data = scope.query('READ?')
    # print(data)

    # print("\nTest and check for errors...")
    # scope.write("TEST")
    # err = scope.query_ascii_values('ERR?', converter='s', separator='\r\n')
    # if err[0] != '0':
    #     print("  Error: ", err)
    # else:
    #     print("  No error.")

    print('\nProgram complete.\n')

if __name__ == "__main__":
    main()