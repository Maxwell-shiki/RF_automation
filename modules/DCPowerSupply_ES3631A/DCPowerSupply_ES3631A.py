from datetime import timedelta
import keysight_kte36000
import numpy as np # For keysight_kte36000 arrays
import time

class DCPowerSupply_ES3631A:
    def __init__(self, resource_name, timeout=1):
        self.resource_name = resource_name
        self.timeout = timeout

        self.idQuery = True
        self.reset = True
        self.options = "QueryInstrStatus=False, Simulate=False, Trace=False"

        self.driver = None
        self.driver = keysight_kte36000.KtE36000(self.resource_name, self.idQuery, self.reset, self.options)

        print("\n  Connected to DC Power Supply: ES3631A.")


    def set_voltage(self, set_voltage, set_channel):
        set_channel_str = "(@" + str(set_channel) + ")"
        # print('    Setting output parameters...')
        print('    Setting Output: Channel', set_channel, 'voltage =', set_voltage, 'V')

        self.driver.output.set_voltage_level(set_voltage, set_channel_str)
        self.driver.output.set_enabled(1, set_channel_str)

    def set_current(self, set_current, set_channel):
        set_channel_str = "(@" + str(set_channel) + ")"
        # print('    Setting output parameters...')
        print('    Setting Output: Channel', set_channel, 'current =', set_current, 'A')

        self.driver.output.set_current_limit(set_current, set_channel_str)
        self.driver.output.set_enabled(1, set_channel_str)
    
    def close(self):
        if self.driver is not None:
            self.driver.close()
        print('  DC Power Supply ES3631A Connection closed.\n')


# ==========================================================================

# if __name__ == "__main__":
#     resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
#     DCPS = DCPowerSupply_ES3631A(resource_name)
#     DCPS.set_voltage(5.0, 1)
#     DCPS.close()

# ==========================================================================