import pyvisa as visa
import re
import time
import numpy as np

def main():
    rm = visa.ResourceManager()
    resource_name = 'USB0::0x0699::0x0503::B030477::0::INSTR'

    scope = rm.open_resource(resource_name)
    ID_msg = scope.query_ascii_values('*IDN?', converter='s', separator='\r\n')
    print("Connected to:", ID_msg[0], "now")

    scope.close()