import pyvisa as visa
import numpy as np

def main():
    rm = visa.ResourceManager()

    print(rm.list_resources())

    scope = rm.open_resource('GPIB0::19::INSTR')
    print(scope.query('*IDN?'))

if __name__ == "__main__":
    main()