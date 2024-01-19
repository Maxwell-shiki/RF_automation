import csv
import sys, os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import re

def get_filename_list(file_dir):
    file_pattern = re.compile(r'(.*)\.csv')
    filename_list = []
    for filename in os.listdir(file_dir):
        if file_pattern.match(filename):
            filename_list.append(filename)
    return filename_list

def parse_filename_components(filename):
    pattern = re.compile(
        r'(?P<Type>[^-]+)-'
        r'(?P<X_name>[^-]+)-'
        r'(?P<Y_name>[^-]+)-'
        r'(?P<Curv_name>[^@]+)@'
        r'(?P<Const_name>[^=]+)=(?P<Const_value>[-+]?\d*\.\d+|[-+]?\d+).* \['
        r'(?P<Type_abbr>[NP]+)-'
        r'(?P<Len>\d*\.\d+|\d+)-'
        r'(?P<Width>\d*\.\d+|\d+)-'
        r'(?P<Temp>\d+)K.* ; '
        r'(?P<month>\d+)_(?P<date>\d+)_(?P<year>\d+) '
        r'(?P<hour>\d+)_(?P<min>\d+)_(?P<sec>\d+) '
        r'(?P<AM_PM>[AP]M+)\].csv'
    )

    match = pattern.match(filename)
    if match:
        components = {
            'Type': match.group('Type'),                            # 管子类型
            'X_name': match.group('X_name'),                        # X轴名称
            'Y_name': match.group('Y_name'),                        # Y轴名称
            'Curv_name': match.group('Curv_name'),                  # 曲线名称
            'Const_name': match.group('Const_name'),                # 常量名称
            'Const_value': float(match.group('Const_value')),       # 常量值
            'Type_abbr': match.group('Type_abbr'),                  # 管子类型缩写
            'Len': float(match.group('Len')),                         # 管子长度
            'Width': float(match.group('Width')),                   # 管子宽度
            'Temp': int(match.group('Temp')),                       # 温度
            'month': int(match.group('month')),                     # 月
            'date': int(match.group('date')),                       # 日
            'year': int(match.group('year')),                       # 年
            'hour': int(match.group('hour')),                       # 时
            'min': int(match.group('min')),                         # 分
            'sec': int(match.group('sec')),                         # 秒
            'AM_PM': match.group('AM_PM'),                          # 上午/下午
        }
        return components
    else:
        raise ValueError(f"Invalid filename format: {filename}")

def main():
    filename_list = get_filename_list('./data')
    for filename in filename_list:
        parsed_components = parse_filename_components(filename)
        # print(parsed_components)
    
    # 将所有下面的操作做成循环，遍历所有文件
    for filename in filename_list:
        parsed_components = parse_filename_components(filename)
        # print(parsed_components)
        print("开始处理文件：", filename)
        # 读取csv文件
        file_path = './data/' + filename
        matrix = []
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csvfile.read().split('\n')
            for row in reader:
                # row_data = row.split(', ')
                row_data = row.split(',')
                matrix.append([element.strip() for element in row_data])
        # for row in matrix:
        #     print(row)

        # 分配数据
        Primary_start = float(matrix[18][2])
        Primary_stop = float(matrix[19][2])
        Primary_step = float(matrix[20][2])
        
        Secondary_start = float(matrix[26][2])
        Secondary_cnt = float(matrix[27][2])
        Secondary_step = float(matrix[28][2])
        
        X_axis_name = matrix[256][1]
        Y_axis_name = matrix[256][2]
        
        curv_len = int((Primary_stop - Primary_start) / Primary_step + 1)       # 单条曲线的区间长度
        curv_num = int(Secondary_cnt)                                           # 曲线数量
        
        # print(curv_len)     # 331
        # print(curv_num)     # 6
        
        # 初始化一个包含多条曲线数据的三维矩阵
        curv_data = np.zeros((curv_num, curv_len, 2))
        # for i in range (0, curv_num):
        #     for j in range (0, curv_len):
        #         print(curv_data[i][j][0], curv_data[i][j][1])
        
        for i in range (0, curv_num):
            for j in range (0, curv_len):
                x = 257 + i * curv_len + j
                curv_data[i][j][0] = float(matrix[x][1])
                curv_data[i][j][1] = float(matrix[x][2])
                # print(curv_data[i][j][0], curv_data[i][j][1])
                
        for i in range (0, curv_num):
            plt.plot(curv_data[i][:,0], curv_data[i][:,1], label=f"curv{i+1}")
        
        plt.xlabel(X_axis_name,fontdict={'family': 'times new roman', 'size': 12})
        plt.ylabel(Y_axis_name,fontdict={'family': 'times new roman', 'size': 12})
        
        plot_title = f"{parsed_components['Type']}: {parsed_components['X_name']}-{parsed_components['Y_name']}, {parsed_components['Const_name']}={parsed_components['Const_value']}, curve of {parsed_components['Curv_name']}.\n W/L = {parsed_components['Len']}:{parsed_components['Width']}, temp = {parsed_components['Temp']}K"

        plt.title(plot_title, fontsize=14, fontfamily='times new roman')
        # plt.title(plot_title, x=0.5, fontsize=14, ha='center', va='center', fontfamily='times new roman')
        
        # 存储图像
        plt.legend(fontsize=10)
        plt.tight_layout()
        # figname = filename.split('.csv')[0].split(' [')[0]
        figname = filename.split('.csv')[0]
        plt.savefig('./img/' + figname + '.png')
        plt.clf()
        print("文件处理完成：", filename)


if __name__ == '__main__':
    main()

# 6-1 文件格式有问题

