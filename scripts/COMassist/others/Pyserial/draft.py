# 串口的基本操作
# 1. 确定串口号
# 2. 配置波特率、数据位、奇偶校验位、停止位、DTR/DSR、RTS/CTS、XON/XOFF
# 3. 打开串口
# 4. 收发数据
# 5. 关闭串口

import sys, os
import re
import time
import serial
import serial.tools.list_ports

def print_portslist():
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) == 0:
        print("没有发现串口设备")
    else:
        print("发现以下串口设备：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])

def write(filename, ser):
    with open(filename, 'r') as f:
        for line in f.readlines():
            ser.write(line.encode("utf-8"))
            time.sleep(0.1)

# 将读取到的数据写入文件
def read(filename, ser):
    with open(filename, 'w') as f:
        data = ser.read_all()
        f.write(data)

if __name__ == "__main__":
    # print_portslist()
    # print(serial.tools.list_ports.comports())
    
    # 打开并配置串口
    # ser = serial.Serial(port="COM4",                       # 串口号
    #                     baudrate=9600,                      # 波特率
    #                     # bytesize=5,                       # 数据位
    #                     parity=PARITY_NONE,                 # 校验位
    #                     stopbits=STOPBITS_ONE               # 停止位
    #                     # timeout=None,                     # 读超时
    #                     # write_timeout=0                   # 写超时
    # )
    ser = serial.Serial(port="COM4", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    
    # if ser.isOpen():
    #     print("打开串口成功")
    # else:
    #     print("打开串口失败")
    
    # 发送数据
    command = ser.write('reg08=0x1111FFFF#'.encode("utf-8"))
    # command = ser.write(b'hello')
    
    # filedir = "./data/"
    # srcfile = "send.txt"
    # write(filedir + filename, ser)
    # destfile = "received.txt"
    # read(destfile, ser)
    
    time.sleep(10)
    
    # 接收数据
    # ser.readline()      # 读取一行
    # ser.read_all()      # 读取所有数据
    # ser.read(10)        # 读取10个字节
    data = ser.read_all()
    print("接收到的数据：", data)

    # 关闭串口
    # ser.close()
    # if ser.isOpen():
    #     print("关闭串口失败")
    # else:
    #     print("串口已关闭")
