from datetime import timedelta
import keysight_kte36000
import numpy as np # For keysight_kte36000 arrays
import time


def main():
    resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"

    #  Edit the initialization options as needed
    idQuery = True
    reset   = True
    #options = "QueryInstrStatus=False, Simulate=True, Trace=False"
    options = "QueryInstrStatus=False, Simulate=False, Trace=False"

    try:

        # Call driver constructor with options
        global driver # May be used in other functions
        driver = None
        driver = keysight_kte36000.KtE36000(resource_name, idQuery, reset, options)

        # TODO: Implement some common instrument specific tasks
        driver.output.set_voltage_level(5.0, "(@1)")
        driver.output.set_enabled(1, "(@1)")
        # time.sleep(1.0)

        # Check instrument for errors
        # print("\n  Checking for errors...")
        # while True:
        #     outVal = ()
        #     outVal = driver.utility.error_query()
        #     print("  error_query: code:", outVal[0], " message:", outVal[1])
        #     if(outVal[0] == 0): # 0 = No error, error queue empty
        #         break

    except Exception as e:
        print("\n  Exception:", e.__class__.__name__, e.args)

    finally:
        if driver is not None: # Skip close() if constructor failed
            driver.close()
        # print('\n  Program complete.\n')
        #input("\nDone - Press Enter to Exit")


if __name__ == "__main__":
    main()
    