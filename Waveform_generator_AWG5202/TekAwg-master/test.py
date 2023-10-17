import TekAwg
import time
import socket

def main():

    AWG_IP = "127.0.0.1"
    AWG_PORT = "4001"
    awg = tekawg5000.tekawg5000(AWG_IP,AWG_PORT)
    awg.print_waveform_list()
    awg.close()
