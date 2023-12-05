import pyvisa as visa
import numpy as np
import time 


def main():
    rm = visa.ResourceManager()

    # print(rm.list_resources())
    # scope = rm.open_resource('GPIB0::19::INSTR')
    # print(scope.query('*IDN?'))

    resource_name = 'GPIB0::19::INSTR'
    sg = rm.open_resource(resource_name)

    # 确认连接
    print(sg.query('*IDN?'))
    sg.write('*RST')

    # 设置频率
    sg.write(':FREQuency 10')

    status = sg.query('FREQ?')
    time.sleep(1)
    print(status)
    
    


if __name__ == "__main__":
    main()