"""Simple program to control a Keysight 3458A multimeter over GPIB."""

import pyvisa as visa
import re
import time

DEFAULT_TIMEOUT = 1

class Multimeter_3458A:
    """Simple program to control a Keysight 3458A multimeter over GPIB."""

    def __init__(self, resource_name, set_mode=None, set_range=None, timeout=DEFAULT_TIMEOUT):
        """Create a new instance of the Keysight 3458A multimeter."""
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(resource_name)
        self.scope.write('END ON')

        ID_msg = self.scope.query_ascii_values('ID?', converter='s', separator='\r\n')
        print("Connected to:", ID_msg[0])
    
    def set_function(self, set_mode):
        """set function mode."""
        self.scope.write("FUNC " + set_mode)

    def set_range(self, set_mode, set_range):
        """set range."""
        self.scope.write(set_mode + " " + set_range)

    def get_data(self):
        """read data from front panel."""
        time.sleep(DEFAULT_TIMEOUT)
        list = self.scope.query_ascii_values('READ?', converter='f', separator='\r\n')
        data = list[0]
        return data
    
    def test(self):
        """Test the multimeter."""
        # test time can be less than 1 minute, and here we read data continuously until the test is done,
        # set the timeout time by changing the DEFAULT_TIMEOUT above
        time_start = time.time()
        while True:
            time_now = time.time()
            if time_now - time_start > DEFAULT_TIMEOUT:
                print("Test time out!")
                break
            else:
                list = self.scope.query_ascii_values('ERR?', converter='s', separator='\r\n')
                if list[0] == '0':
                    print("Test done! No error.")
                    break
                elif list[0] == '1':
                    print("Err code: 1")
                    continue


    def close(self):
        """Close the connection to the multimeter."""
        self.scope.close()
        self.rm.close()
        print("Connection closed.")
