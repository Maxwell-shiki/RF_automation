import pyvisa as visa
import numpy as np
import re

# 这是没有模块化的版本

# 响应->测量->s11,s12, etc.
# 文件->另存数据为->.snp

def main():
    rm = visa.ResourceManager()
    resource_name = 'GPIB0::16::INSTR'

    vna = rm.open_resource(resource_name)

    ID_msg = vna.query('*IDN?').replace("\n", "")
    print("Connected to:", ID_msg)

    # -> CALC1:PAR:CAT:EXT?
    # <- "CH1_WIN1_LINE1_PARAM1,S11"
    print('Channel 1:')
    list = vna.query('CALC1:PAR:CAT:EXT?').replace("\n", "").replace("\"", "").split(',')
    num = int(len(list)/2)
    if num == 0:
        print('  ', list[0])
    else:
        for i in range(num):
            print('  Name:', list[2*i])
            print('  Type:', list[2*i+1])

    # -> CALC1:PAR:DEL "CH1_WIN1_LINE1_PARAM1"
    

    # vna.write('')


if __name__ == "__main__":
    main()