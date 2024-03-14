import sys, os
import subprocess
import re
import pyvisa as visa
import openpyxl
import serial
import time

def dec2bin(num, bits): 
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num), bits)
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
            return ''.join(l[::-1]).zfill(bits)

def bin_not(num):
    l = list(str(num))
    for i in range(len(l)):
        l[i] = '1' if l[i] == '0' else '0'
    return ''.join(l)

# base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
# def dec2hex(num):
#     l = []
#     if num < 0:
#         return '-' + dec2hex(abs(num))
#     while True:
#         num,rem = divmod(num, 16)
#         l.append(base[rem])
#         if num == 0:
#             return ''.join(l[::-1])

def genCode(I, Q):
    I_bin = dec2bin(I, 6)
    Q_bin = dec2bin(Q, 6)
    I_not = bin_not(I_bin)
    Q_not = bin_not(Q_bin)
    
    code = ''
    
    # reg_bank0<0> ~ reg_bank0<23> 依次为
    # Q1 Q1' Q2 Q2' Q3 Q3' 
    # I1 I1' I2 I2' I3 I3'
    # I4 I4' I5 I5' I6 I6'
    # Q4 Q4' Q5 Q5' Q6 Q6'
    for i in range(3):
        code += Q_bin[i] + Q_not[i]
    for i in range(6):
        code += I_bin[i] + I_not[i]
    for i in range(3, 6):
        code += Q_bin[i] + Q_not[i]
    
    # 左边是低位，右边是高位，故倒序
    code = code[::-1]
    
    # code = dec2hex(int(code, 2))        # bin序列转hex序列
    code = hex(int(code, 2))
    
    return code 

def main():
    I = 11
    Q = 56
    code = genCode(I, Q)
    
    print(code)
    print(hex(1283))


if __name__ == '__main__':
    main()