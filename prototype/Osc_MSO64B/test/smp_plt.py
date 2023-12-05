# ref to https://www.bilibili.com/video/BV1UB4y1D7qF/?vd_source=2441a44fb55231b18c83d14d540b7735

import time
import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np

visa_addr = 'USB0::0x0699::0x0530::C051431::0::INSTR' # USB port
rm = visa.ResourceManager()
scope = rm.open_resource(visa_addr)

scope.timeout = 10000   # ms
scope.write('*CLS')     # clear ESR

# print(scope.query('*IDN?'))

scope.write('*IDN?')
print(scope.read())

# scope.write('*RST')         # reset scope
# r = scope.query('*OPC?')    # query sync

# scope.write('autoset EXECUTE')  # autoset scope
# r = scope.query('*OPC?')        # query sync

# io config
scope.write('header 0')
scope.write('data:encdg SRIBINARY')
scope.write('data:source CH1')                          # channel 1
scope.write('data:start 1')                             # first sample
record = int(scope.query('horizontal:recordlength?'))
scope.write('data:stop {}'.format(record))              # wave data length
scope.write('wfmoutpre:byt_n 2')                        # 2 byte per data point
                                                        # > 8bit, so 2 bytes
# # acq config
# scope.write('acquire:state 0')                          # stop acq
# # scope.write('acquire:stopafter sequence')               # single (单个波形)
# scope.write('acquire:stopafter runstop')                # runstop (连续运行)
# scope.write('acquire:state 1')                          # start acq
# r = scope.query('*OPC?')                                # sync

# data query
bin_wave = scope.query_binary_values('curve?', datatype='h', container=np.array)

# retrieve scaling factors
tscale = float(scope.query('wfmoutpre:xincr?'))
tstart = float(scope.query('wfmoutpre:xzero?'))
vscale = float(scope.query('wfmoutpre:ymult?'))         # V/div
voff = float(scope.query('wfmoutpre:yzero?'))           # reference voltage
vpos = float(scope.query('wfmoutpre:yoff?'))            # reference position

# error checking
r = int(scope.query('*ESR?'))

scope.close()
rm.close()

# create scaled vectors
# horizontal (time)
total_time  = tscale * record
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)

# vertical (voltage)
unscaled_wave = np.array(bin_wave, dtype='double')   # data type conversion
scaled_wave = (unscaled_wave - vpos) * vscale + voff
print('Done!')

# plot
plt.plot(scaled_time, scaled_wave)
plt.title('Oscilloscope Waveform Channel 1')        # plot label
plt.xlabel('time (seconds)')                        # x-axis label
plt.ylabel('voltage (volts)')                       # y-axis label
plt.grid(which='major', color='gray', linestyle='--', alpha=0.7)
plt.grid(which='minor', color='gray', linestyle=':', alpha=0.4)
plt.minorticks_on()
plt.show()
