import pyvisa as visa
import numpy as np
import re
from datetime import datetime

def main():
    rm = visa.ResourceManager()
    resource_name = 'GPIB1::16::INSTR'

    vna = rm.open_resource(resource_name)

    ID_msg = vna.query('*IDN?').replace("\n", "")
    print("Connected to:", ID_msg)

    # 查询测量信息
    # print(vna.query('CALC1:PAR:CAT?').replace("\n", ""))
    vna.write(':DISP:WIND1:STAT ON')                    # 打开窗口

    # 注意要先选择测量再后续操作
    vna.write(':CALC1:PAR:SEL "CH1_WIN1_LINE1_PARAM1"')

    # 设置保存到网络仪的文件路径
    # print(vna.query('MMEM:CDIR?').replace("\n", ""))      # 显示当前默认存储目录
    vna.write(':MMEM:CDIR "E:\AutoTEST"')                  # 设置默认存储目录到E盘的自动化测试AutoTEST文件夹下

    # 保存snp文件
    # print(vna.query(':MMEM:STOR:TRAC:FORM:SNP?').replace("\n", ""))         # 显示当前存储格式
    # vna.write(':MMEM:STOR:TRAC:FORM:SNP DB')                                # 设置存储格式，支持 线性幅度MA, 对数幅度DB, 实部虚部RI, AUTO, p200
    vna.write(":CALC:DATA:SNP:PORTs:SAVE '1,2','tmp.s2p'")             # 读取指定端口SNP数据到文件中, p64

    # 传输snp文件数据到本机, p201
    snpfiledata = vna.query(":MMEM:TRAN? 'tmp.s2p'")
    file_path = "./data/data1.s2p"
    with open(file_path, "w") as f:
        f.write(snpfiledata)
    
    # 删除网络仪中的文件
    vna.write(":MMEM:DEL 'tmp.s2p'")

    # **************************************************************************************
    # print(vna.query('SYST:ERR?'))

if __name__ == "__main__":
    main()