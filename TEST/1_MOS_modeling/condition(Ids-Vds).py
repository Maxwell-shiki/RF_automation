import sys, os
import subprocess
import re
import pyvisa as visa
import openpyxl
import serial
import serial.tools.list_ports
import time

import numpy as np
import matplotlib.pyplot as plt

# ========= import modules ================================
path_devices = '..\\..\\modules'
for root, dirs, files in os.walk(path_devices):
    for directory in dirs:
        path_module = os.path.join(root, directory)
        sys.path.append(path_module)

path_scripts = '..\\..\\scripts'
for root, dirs, files in os.walk(path_scripts):
    for directory in dirs:
        path_script = os.path.join(root, directory)
        sys.path.append(path_script)

from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  
from Multimeter_3458A import Multimeter_3458A


def main():

    PS_resource_name = "USB0::0x2A8D::0x1002::MY61002637::0::INSTR"
    MM_resource_name = "GPIB2::22::INSTR"
    PS = DCPowerSupply_ES3631A(PS_resource_name)
    MM = Multimeter_3458A(MM_resource_name)

    MM.set_measure(set_mode='DCI', set_range=10e-3)

    ch1_Vgs = 0
    ch2_Vds = 0
    ch3_Vbs = -3.3
    Ids = 0

    PS.set_voltage(ch3_Vbs, channel = 3)

    for i in range(3, 34, 6):
        Vds_list = []
        Ids_list = []

        ch1_Vgs = i/10
        PS.set_voltage(ch1_Vgs, channel = 1)
        print("    Vgs = ", ch1_Vgs)

        for j in range(0,34):
            ch2_Vds = j/10
            PS.set_voltage(ch2_Vds, channel = 2)
            print("    Vds = ", ch2_Vds) 
            Vds_list.append(ch2_Vds)
            
            # time.sleep(0.5)
            Ids = MM.get_data()
            print("        Current output = ", Ids, "A")
            Ids_list.append(Ids)
        curve_label = 'Vgs = ' + str(ch1_Vgs) + 'V'

        plt.plot(Vds_list, Ids_list,'-o', label=curve_label)

        print("Vds_list = ", Vds_list)
        print("Ids_list = ", Ids_list)


    plt.xlabel('Vds')
    plt.ylabel('Ids')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()