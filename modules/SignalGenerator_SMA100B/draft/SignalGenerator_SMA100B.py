import pyvisa as visa
import numpy as np
import re

# 这是没有模块化的的版本,仅用于学习了解仪器的SCPI指令功能

def main():
    rm = visa.ResourceManager()
    resource_name = 'TCPIP0::SMA100B-106560::hislip0::INSTR'
    # 在仪器面板，SCPI -> Remote Access -> Remote Connections界面里
    # SCPI Connections下面的Resource String显示的就是这个resource_name
    # 格式为: 'TCPIP::hostaddress[::LAN device name][::INSTR]'

    sg = rm.open_resource(resource_name)

    ID_msg = sg.query('*IDN?').replace("\n", "")    
    print("Connected to:", ID_msg)

    # sg.write('*RST')

    # show path of <filename>
    # default path is "/var/user"
    # print(sg.query('SYST:MMEM:PATH:USER?')).replace("\n", "")
    # avoid using the following filenames: CLOCK$, CON, COM1 to COM4, LPT1 to LPT3, NUL, PRN

    # <directory_name>/<path>: "/var/volatile"

    sg.write('SOUR:FREQ 1.14514E9')        # unit: Hz
    sg.write('SOUR:POW -12')               # unit: dBm
    
    # saving and loading current settings(p472)
    # save
    # sg.write('*SAV 4')
    # sg.write('MMEMory:STORe:STATe 4,"/var/user/savrcl/setting4.savrcltxt"')
    # # load
    # sg.write('MMEMory:LOAD:STATe 4,"/var/user/savrcl/setting4.savrcltxt"')
    # sg.write('*RCL 4')

    # MMEMory:CDIRectory
    # MMEMory:CDIRectory?
    # MMEMory:CATalog?
    # MMEMory:MDIRectory "/var/user/newdir"
    # MMEMory:COPY "/var/user/setting.savrcltxt", "/var/user/newdir/setting.savrcltxt"
    # MMEMory:RDIRectory "/var/user/newdir" # remove directory
    # MMEM:DATA? "/var/user/setting.savrcltxt"

    # CSYN clock synthesis p484

    # DISP
    sg.write('DISP:BRIG 14')        # set brightness of display, 1.0-20.0, default 14.0

    # FORM
    # sg.write('FORM:DATA?')          # query data format, default ASCii

    # HCOPy

    # OUTP
    # sg.write('OUTP1 ON')        # turn on RF output

    # CALCulate p.515

    # Sense Sweep

    # Trace

    error_msg = sg.query('SYST:ERR?').replace("\n", "")
    error_code = int(error_msg.split(',')[0])
    if error_code != 0:
        print(error_msg)

if __name__ == "__main__":
    main()
