import pyvisa as visa
from datetime import timedelta
import time
import numpy as np 
import re
import sys, os
sys.path.append('../')
from Multimeter_3458A import multimeter_3458A


import keysight_kte36000
# import multimeter_3458A


def DC_power_supply():
    resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"

    idQuery = True
    reset   = True
    options = "QueryInstrStatus=False, Simulate=False, Trace=False"

    try:
        # Call driver constructor with options
        global driver 
        driver = None
        driver = keysight_kte36000.KtE36000(resource_name, idQuery, reset, options)

        # Implement specific tasks
        driver.output.set_voltage_level(5.0, "(@1)")
        driver.output.set_enabled(1, "(@1)")

    except Exception as e:
        print("\n  Exception:", e.__class__.__name__, e.args)

    finally:
        if driver is not None: # Skip close() if constructor failed
            driver.close()
            print('\n1. DC power supply E3631A has been configured.\n')

def Multimeter():
    resource_name = "GPIB0::22::INSTR"
    print("\n2. Multimeter 3458A start testing.\n")
    mm = multimeter_3458A.Multimeter_3458A(resource_name)
    # mm.test()
    # mm.close()

        # list = self.scope.query_ascii_values('READ?', converter='f', separator='\r\n')
        # data = list[0]
    
    mm.set_function('DCV')
    mm.set_range('DCV', '10')
    print(mm.scope.query_ascii_values('READ?'))

    mm.close()


def main():
    print("TEST BEGIN.")
    DC_power_supply()
    Multimeter()
    print("\nTEST END.\n")



if __name__ == "__main__":
    main()
    