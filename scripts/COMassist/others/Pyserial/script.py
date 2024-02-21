import sys, os
import re
import time
import serial
import serial.tools.list_ports

def SPI_write(portname, baudrate, parity, stopbits, command):
    ser = serial.Serial(port=portname, baudrate=baudrate, parity=parity, stopbits=stopbits)
    ser.write(command.encode("utf-8"))
    data = ser.readline()
    return data

if __name__ == "__main__":

    portname = "COM4"
    baudrate = 9600
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE

    command = "reg08=0x1111FFFF#"

    data = SPI_write(portname, baudrate, parity, stopbits, command)
    print(data)
