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


    def set_voltage(self, set_voltage, channel):
        channel_str = "(@" + str(channel) + ")"
        # print('    Setting output parameters...')
        print('    Setting Output: Channel', channel, 'voltage =', set_voltage, 'V')

        self.driver.output.set_voltage_level(set_voltage, channel_str)
        self.driver.output.set_enabled(1, channel_str)

    def set_current(self, set_current, channel):
        channel_str = "(@" + str(channel) + ")"
        # print('    Setting output parameters...')
        print('    Setting Output: Channel', channel, 'current =', set_current, 'A')

        self.driver.output.set_current_limit(set_current, channel_str)
        self.driver.output.set_enabled(1, channel_str)
    
    def get_voltage(self, channel):
        channel_str = "(@" + str(channel) + ")"
        voltage =  self.driver.measurement.measure(keysight_kte36000.FetchType.VOLTAGE, channel_str)
        return voltage

    def get_current(self, channel):
        channel_str = "(@" + str(channel) + ")"
        current =  self.driver.measurement.measure(keysight_kte36000.FetchType.CURRENT, channel_str)
        return current

    def close(self):
        if self.driver is not None:
            self.driver.close()
        print('  DC Power Supply ES3631A Connection closed.\n')

# add test demo 


# ==========================================================================

# if __name__ == "__main__":
#     resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
#     DCPS = DCPowerSupply_ES3631A(resource_name)
#     DCPS.set_voltage(5.0, 1)
#     DCPS.close()

# ==========================================================================