import pyvisa as visa
import re
import time

DEFAULT_TIMEOUT = 1

class Multimeter_3458A:
    def __init__(self, resource_name, set_mode=None, set_range=None, timeout=DEFAULT_TIMEOUT):
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(resource_name)
        self.scope.write('END ON')

        ID_msg = self.scope.query_ascii_values('ID?', converter='s', separator='\r\n')
        print("\n  Connected to Multimeter: ", ID_msg[0])
    
    def set_measure(self, set_mode, set_range):
        self.scope.write("FUNC " + set_mode + "; " + set_mode + " " + str(set_range))
        print('    Start measure "', set_mode, '" in "', set_range, '" range...')

    def get_data(self):
        time.sleep(DEFAULT_TIMEOUT)
        list = self.scope.query_ascii_values('READ?', converter='s', separator='\r\n')
        data = list[0]
        data = float(data.replace(" ", ""))
        return data
    
    def write(self, command):
        self.scope.write(command)

    def query(self, command):
        return self.scope.query(command)
    
    def test(self):
        # test time can be less than 1 minute, and here we read data continuously until the test is done,
        # set the timeout time by changing the DEFAULT_TIMEOUT above
        time_start = time.time()
        while True:
            time_now = time.time()
            if time_now - time_start > DEFAULT_TIMEOUT:
                print("    Test time out!")
                break
            else:
                list = self.scope.query_ascii_values('ERR?', converter='s', separator='\r\n')
                if list[0] == '0':
                    print("    Test done! No error.")
                    break
                elif list[0] == '1':
                    print("    Err code: 1")
                    continue

    def close(self):
        self.scope.close()
        self.rm.close()
        print("  Multimeter 3458A Connection closed.\n")
