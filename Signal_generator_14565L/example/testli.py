import pyvisa as visa
#import time
import string
visa_dll = 'c:/windows/system32/visa32.dll'

#################################################################
#函数功能：建立与仪器的通信连接
#函数输入：输入仪器的IP地址 字符串类型
#函数返回:返回建立的通信句柄，用于后面的发送和读取使用
#################################################################
def connect(IpAddress):
        tcp_addr = 'TCPIP::' + IpAddress + '::5025::SOCKET'     #5025表示端口号
        rm = visa.ResourceManager(visa_dll)
        tcp_inst = rm.open_resource(tcp_addr)
        tcp_inst.write_termination = '\n'
        tcp_inst.read_termination = '\n'
        return tcp_inst

###########################################################################################################
#函数功能：设置仪器的频率和功率值
#函数输入：对应仪器的通信句柄，频率值和功率值，频率值为数值类型，范围为Hz，功率值为数值类型，单位为dBm
#函数返回：无
###########################################################################################################

def SetFreqPow(HandleConn, FreqVal, PowVal):
        HandleConn.write('freq ' + str(FreqVal) + 'Hz')
        HandleConn.write('pow ' + str(PowVal))
        return

###########################################################################################################
#函数功能：读取仪器的频率和功率值
#函数输入：对应仪器的通信句柄。
#函数返回：两个，依次为频率值和功率值，频率值的单位为Hz，功率值的单位为dBm
###########################################################################################################
def GetFreqPow(HandConn):
        freqval = HandConn.query('freq?')
        powval = HandConn.query('pow?')
        return freqval, powval
############################################################################
#函数功能：关闭与仪器的连接
#函数输入：与仪器建立的通信句柄
#函数返回：无
##########################################################################
def CloseHandle(HandConn):
        HandConn.close()
        return
#函数调用示例
handle = connect('127.0.0.1')
SetFreqPow(handle, 2000000000, -10)
freq, power = GetFreqPow(handle)
print(freq)
print(power)
CloseHandle(handle)


