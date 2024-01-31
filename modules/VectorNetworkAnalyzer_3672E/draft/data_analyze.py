import re, sys, os
import numpy as np 

def main():
    file_dir = './data'
    filename_pattern = re.compile(r'(.*)\.s([1-9]+)p')
    filename_list = []
    for filename in os.listdir(file_dir):
        if filename_pattern.match(filename):
            filename_list.append(filename)

    # # 显示数据存储文件夹中的snp文件
    # if not filename_list:
    #     print("No snp file found in", file_dir)
    #     sys.exit(1)
    # else:
    #     print("Found snp files:", filename_list)

    measurement_pattern = re.compile(r'!S[1-9]+P File: Measurements: (S\d{2}, S\d{2}, S\d{2}, S\d{2}):')
    dataformat_pattern = re.compile(r'# (Hz|GHz|MHz|kHz)  (S)  (RI|dB|MA)  R (\b\d+\.\d{3}\b)')
    
    with open(os.path.join(file_dir, filename_list[0]), "r") as f:
        lines = f.readlines()
        snpfile = lines[::2]
        for line in snpfile:
            # 如果以"!SNP File: Measurement: "开头，则匹配该行Measurement:后面到:之间的字符串
            if measurement_pattern.match(line):
                measurement = measurement_pattern.match(line).group(1)
                measurement = measurement.split(", ")
            if dataformat_pattern.match(line):
                freq_unit = dataformat_pattern.match(line).group(1)
                item = dataformat_pattern.match(line).group(2)
                item_format = dataformat_pattern.match(line).group(3)
                R_value = dataformat_pattern.match(line).group(4)
                data_index_start = snpfile.index(line) + 1
        
    # 从data_index_start开始逐行读取数据
    data = []
    for line in snpfile[data_index_start:]:
        data.append(line.split())
    # data每行的数据格式为: 
    # [freq, S11(Re), S11(Im), S12(Re), S12(Im), S21(Re), S21(Im), S22(Re), S22(Im)]
    freq = [freq_unit]
    measurement1 = [measurement[0]]
    measurement2 = [measurement[1]]
    measurement3 = [measurement[2]]
    measurement4 = [measurement[3]]
    print("Measurement:", measurement1, measurement2, measurement3, measurement4)

    # 从data中提取数据
    for line in data:
        freq.append(float(line[0]))
        measurement1.append(complex(float(line[1]), float(line[2])))
        measurement2.append(complex(float(line[3]), float(line[4])))
        measurement3.append(complex(float(line[5]), float(line[6])))
        measurement4.append(complex(float(line[7]), float(line[8])))

    index = 5
    print("when freq =", freq[index], freq_unit)
    print(measurement1[0], ":")
    print("  real part: ", measurement1[index].real, item_format)
    print("  imag part: ", measurement1[index].imag, item_format)
    print(measurement2[0], ":")
    print("  real part: ", measurement2[index].real, item_format)
    print("  imag part: ", measurement2[index].imag, item_format)
    print(measurement3[0], ":")
    print("  real part: ", measurement3[index].real, item_format)
    print("  imag part: ", measurement3[index].imag, item_format)
    print(measurement4[0], ":")
    print("  real part: ", measurement4[index].real, item_format)
    print("  imag part: ", measurement4[index].imag, item_format)


if __name__ == "__main__":
    main()