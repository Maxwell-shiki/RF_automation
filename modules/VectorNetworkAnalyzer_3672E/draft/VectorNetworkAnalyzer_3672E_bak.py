import pyvisa as visa
import numpy as np
import re

# 这是没有模块化的版本

# 响应->测量->s11,s12, etc.
# 文件->另存数据为->.snp

def main():
    rm = visa.ResourceManager()
    resource_name = 'GPIB1::16::INSTR'

    vna = rm.open_resource(resource_name)

    ID_msg = vna.query('*IDN?').replace("\n", "")
    print("Connected to:", ID_msg)

    # p51 仪器子系统目录

    # **************************************************************************************
    # CALC 测量子系统
    # -> DISP:WIND:STATe 创建窗口
    # p56 custom 测量类定义
    # :CALC:PAR:DEF:EXT 标准测量类

    # CALC:FUNC 子系统
    # 轨迹统计功能的设置和查询 p88

    # CALCL:MARK 子系统

    # **************************************************************************************
    # 基本操作案例 p442 

    # 校准相关 可能就写个应用校准集的操作
    # SENS:CORRection 校准相关子系统，操作案例里面写了好多

    # **************************************************************************************
    # 基本设置
    # 查询测量信息
    # print(vna.query('CALC1:PAR:CAT?').replace("\n", ""))
    # print(vna.query(':DISP:CAT?').replace("\n", ""))
    
    vna.write(':DISP:WIND1:STAT ON')                    # 打开窗口

    # 远控时需要 创建测量、显示测量、选择测量   
    vna.write(':CALC1:PAR:DEF:EXT "Line1",S12')         # 创建测量 p166
    vna.write(':DISP:WIND1:TRAC1:FEED "Line1"')         # 显示测量
    # vna.write(':DISP:WIND2:STAT ON')
    # vna.write(':CALC1:PAR:DEF:EXT "Line2",S11')         # 创建测量
    # vna.write(':DISP:WIND2:TRAC2:FEED "Line2"')         # 显示测量

    # 注意要先选择测量再后续操作
    vna.write(':CALC1:PAR:SEL "Line1"')

    # # 删除测量
    # vna.write(':CALC1:PAR:DEL "Line2"')
    # # vna.write(':CALC1:PAR:DEL:ALL')

    # # 设置扫描参数
    # vna.write(':CALC1:PAR:SEL "Line1"')                 # 选择测量
    # vna.write(':SENS1:SWE:TYPE LIN')                    # 设置扫描类型为线性扫描  p369
    # # vna.write(':SENS1:BANDwidth 1000')                  # 设置中频带宽为 1KHz
    # vna.write(':SENS1:FREQ:STAR 1e8')                   # 设置起始频率为 1GHz
    # vna.write(':SENS1:FREQ:STOP 5e10')                  # 设置终止频率为 10GHz
    # vna.write(':SENS1:SWE:POIN 401')                    # 设置扫描点数为 401
    # vna.write(':SENS1:SWE:TIME:AUTO ON')                # 设置自动扫描时间
    # vna.write(':SOUR:POW -10dBm')                       # 设置输出功率为 -10dBm


    # 设置显示参数
    # vna.write(':CALC:FORM MLOG')                        # 设置显示格式为对数幅度  p69 
    # 支持格式包括：MLIN, MLOG, PHAS, IMAG, REAL, POL, SMIT, SWR, etc.
    # vna.write(':DISP:WIND1:TRAC1:STAT on')              # 显示轨迹
    # vna.write(':DISP:WIND1:TITL:STAT off')              # 显示标题
    # vna.write(':DISP:ANN:FREQ on')                      # 显示频率

    # vna.write(':DISP:WIND1:TRAC1:Y:Scale:AUTO')         # 对轨迹执行自动比例
    # 查询比例值，参考电平和参考位置
    # pdiv = float(vna.query(':DISP:WIND1:TRAC1:Y:Scale:PDIV?').replace("\n", ""))
    # print("  窗口1 轨迹1 Y轴比例 = ", pdiv)
    # rlev = float(vna.query(':DISP:WIND1:TRAC1:Y:Scale:RLEV?').replace("\n", ""))
    # print("  窗口1 轨迹1 Y轴参考值 = ", rlev)
    # rpos = float(vna.query(':DISP:WIND1:TRAC1:Y:Scale:RPOS?').replace("\n", ""))
    # print("  窗口1 轨迹1 Y轴参考位置 = ", rpos)

    # # 打开测多次取平均系统，减噪，对本通道所有测量起作用
    # vna.write(':SENS1:AVER:STAT on')               
    # vna.write(':SENS1:AVER:Count 3')

    # 打开平滑系统，设置平滑孔径为20%
    # vna.write(':CALC1:SMOothing:STAT ON')
    # vna.write(':CALC1:SMOothing:APER 20')

    # **************************************************************************************
    # 查询频标 p455

    # **************************************************************************************
    # MMEMory 子系统 p194
    # 网络仪与控制机间的数据传输 p201

    # 设置保存到网络仪的文件路径
    # print(vna.query('MMEM:CDIR?').replace("\n", ""))      # 显示当前默认存储目录
    vna.write(':MMEM:CDIR "E:\AutoTEST"')                  # 设置默认存储目录到E盘的自动化测试AutoTEST文件夹下

    # 保存snp文件
    # print(vna.query(':MMEM:STOR:TRAC:FORM:SNP?').replace("\n", ""))         # 显示当前存储格式
    # vna.write(':MMEM:STOR:TRAC:FORM:SNP DB')                                # 设置存储格式，支持 线性幅度MA, 对数幅度DB, 实部虚部RI, AUTO, p200
    vna.write(":CALC:DATA:SNP:PORTs:SAVE '1,2','MyData.s2p'")             # 读取指定端口SNP数据到文件中, p64

    # 直接查询轨迹数据见 p60 CALC:DATA 系统
    # 传输snp文件数据到本机, p201
    snpfiledata = vna.query(":MMEM:TRAN? 'MyData.s2p'")
    file_path = "./data/MyData.s2p"
    with open(file_path, "w") as f:
        f.write(snpfiledata)
    
    # 删除网络仪中的文件
    vna.write(":MMEM:DEL 'MyData.s2p'")

    # **************************************************************************************
    # print(vna.query('SYST:ERR?'))


if __name__ == "__main__":
    main()