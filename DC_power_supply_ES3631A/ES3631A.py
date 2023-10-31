"""
keysight_kte36000 Python API Example Program

Creates a driver object, reads a few DriverIdentity interface properties, and checks
the instrument error queue.  May include additional instrument specific functionality.

Runs in simulation mode without an instrument.

Requires Python 3.6 or newer and keysight_kte36000 Python module installed.
"""

from datetime import timedelta
import keysight_kte36000
import numpy as np # For keysight_kte36000 arrays
import time


def main():
    """
    Edit resource_name and options as needed.  resource_name is ignored if option Simulate=true
    For this example, resource_name may be a VISA address(e.g. "TCPIP0::<IP_Address>::INSTR")
    or a VISA alias. See below for some typical address examples.
    For more information on using VISA aliases, refer to the Keysight IO
    Libraries Connection Expert documentation.
    """
    #resource_name = "MyVisaAlias"
    #resource_name = "TCPIP0::<IP_Address>::INSTR"
    #resource_name = "GPIB0::09::INSTR"
    #resource_name = "USB0::0x2A8D::0x1401::MY53200158::0::INSTR"
    resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    # resource_name = "TCPIP0::10.80.6.42::inst0::INSTR"

    #  Edit the initialization options as needed
    idQuery = True
    reset   = True
    #options = "QueryInstrStatus=False, Simulate=True, Trace=False"
    options = "QueryInstrStatus=False, Simulate=False, Trace=False"

    try:
        print("\n  keysight_kte36000 Python Instrument Driver Example\n")

        # Call driver constructor with options
        global driver # May be used in other functions
        driver = None
        driver = keysight_kte36000.KtE36000(resource_name, idQuery, reset, options)
        print("  Driver Initialized")

        #  Print a few identity properties
        print('  identifier: ', driver.identity.identifier)
        print('  revision:   ', driver.identity.revision)
        print('  vendor:     ', driver.identity.vendor)
        print('  description:', driver.identity.description)
        print('  model:      ', driver.identity.instrument_model)
        print('  resource:   ', driver.driver_operation.io_resource_descriptor)
        print('  options:    ', driver.driver_operation.driver_setup)


        # TODO: Implement some common instrument specific tasks
        print()
        print('  Setting output parameters...')
        driver.output.set_voltage_level(5.0, "(@1)")
        driver.output.set_enabled(1, "(@1)")
        time.sleep(1.0)
        print('  Measuring Voltage & Current...')
        print('     CH1 Voltage = ', driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE, "(@1)"))
        print('     CH1 Current = ', driver.measurement.measure(keysight_kte36000.FetchType.CURRENT, "(@1)"))
        print('     CH2 Voltage = ', driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE, "(@2)"))
        # driver.output.set_voltage_level(5.0,"(@1)")
        # # driver.output.set_current_limit(5.0,"(@1)")
        # # driver.output.set_voltage_level(10.0,"(@2)")
        # # driver.output.set_current_limit(0.8,"(@2,3)")
        # driver.output.set_enabled(1,"(@1:3)")
        # time.sleep(1.0)
        # print('  Measuring Voltage & Current...')
        # print('     CH1 Voltage = ', driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE,"(@1)"))
        # print('     CH1 Current = ', driver.measurement.measure(keysight_kte36000.FetchType.CURRENT,"(@1)"))
        # print('     CH2 Voltage = ', driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE,"(@2)"))
        # print('     CH2 Current = ', driver.measurement.measure(keysight_kte36000.FetchType.CURRENT,"(@2)"))
        # print('     CH3 Voltage = ', driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE,"(@3)"))
        # print('     CH3 Current = ', driver.measurement.measure(keysight_kte36000.FetchType.CURRENT,"(@3)"))
        

        # Check instrument for errors
        print("\n  Checking for errors...")
        while True:
            outVal = ()
            outVal = driver.utility.error_query()
            print("  error_query: code:", outVal[0], " message:", outVal[1])
            if(outVal[0] == 0): # 0 = No error, error queue empty
                break

    except Exception as e:
        print("\n  Exception:", e.__class__.__name__, e.args)

    finally:
        if driver is not None: # Skip close() if constructor failed
            driver.close()
        print('\n  Program complete.\n')
        #input("\nDone - Press Enter to Exit")


if __name__ == "__main__":
    main()
    