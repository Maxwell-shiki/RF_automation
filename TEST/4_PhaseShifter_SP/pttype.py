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

def genCode(I, Q):
    I_bin = dec2bin(I, 6)       # I6 I5 I4 I3 I2 I1
    Q_bin = dec2bin(Q, 6)       # Q6 Q5 Q4 Q3 Q2 Q1
    I_not = bin_not(I_bin)      # I6' I5' I4' I3' I2' I1'
    Q_not = bin_not(Q_bin)      # Q6' Q5' Q4' Q3' Q2' Q1'
    
    code = ''
    # reg_bank0<0> ~ reg_bank0<23> 依次为
    # Q1 Q1' Q2 Q2' Q3 Q3' 
    # I1 I1' I2 I2' I3 I3'
    # I4 I4' I5 I5' I6 I6'
    # Q4 Q4' Q5 Q5' Q6 Q6'
    code =  Q_bin[5]+Q_not[5]+Q_bin[4]+Q_not[4]+Q_bin[3]+Q_not[3]+\
            I_bin[5]+I_not[5]+I_bin[4]+I_not[4]+I_bin[3]+I_not[3]+\
            I_bin[2]+I_not[2]+I_bin[1]+I_not[1]+I_bin[0]+I_not[0]+\
            Q_bin[2]+Q_not[2]+Q_bin[1]+Q_not[1]+Q_bin[0]+Q_not[0]
    print(code)
    code = code[::-1]
    code = hex(int(code, 2))
    return '0x' + ''.join(code.split('0x')).zfill(8)

def main():
    I = 11
    Q = 56
    
    I_bin = dec2bin(I, 6)
    I_not = bin_not(I_bin)
    
    Q_bin = dec2bin(Q, 6)
    Q_not = bin_not(Q_bin)
    
    # print(I_bin)
    # print(I_not)
    # print(Q_bin)
    # print(Q_not)
    
    code = genCode(I, Q)
    print(code)
    

if __name__ == '__main__':
    main()