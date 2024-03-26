import sys, os
import subprocess
import numpy as np
import re
import csv
import pandas as pd

# 获取脚本所在文件夹下的所有csv文件
def getFilelist_csv(file_dir):
    file_pattern = re.compile(r'(.*)\.csv')
    filename_list = []
    for filename in os.listdir(file_dir):
        if file_pattern.match(filename):
            filename_list.append(filename)
    return filename_list

# 获取csv文件的曲线数据
def getCurves_csv(filename):
    skiprows = 254
    
    # 读取曲线参数：每条曲线的数据点数 和 曲线数
    df_dim = pd.read_csv(filename, skiprows=skiprows, header=None, names=['Type', 'x', 'y'])
    points_per_curve = int(df_dim.loc[df_dim['Type'] == 'Dimension1', 'x'].iloc[0])
    num_curves = int(df_dim.loc[df_dim['Type'] == 'Dimension2', 'x'].iloc[0])
    
    # 读取横纵坐标名称
    df_param = pd.read_csv(filename, skiprows=skiprows+2, header=None, names=['Type', 'x', 'y'])
    XAxisName = df_param.loc[df_param['Type'] == 'DataName', 'x'].iloc[0]
    YAxisName = df_param.loc[df_param['Type'] == 'DataName', 'y'].iloc[0]

    # 读取数据
    df_data = pd.read_csv(filename, skiprows=skiprows+3, header=None, names=['Type', XAxisName, YAxisName])
    df_data = df_data[df_data['Type'] == 'DataValue']
    df_data = df_data.drop(columns=['Type'])
    
    # 按曲线参数分割数据
    # 创建一个DataFrame列表集和，每个DataFrame代表一条曲线
    # 每个DataFrame有两列：XAxisName 和 YAxisName
    curves = []
    for i in range(num_curves):
        curve = df_data.iloc[i*points_per_curve:(i+1)*points_per_curve]
        curves.append(curve)
    
    return curves

def getZAxisVal_csv(filename):
    skiprows = 26
    num_lines = sum(1 for l in open(filename, encoding='utf-8'))
    df = pd.read_csv(filename, skiprows=list(range(1, 26))+list(range(29, num_lines)), header=None, names=['Name', 'Param', 'Value'])
    val = df.loc[df['Name'] == 'TestParameter', 'Value']
    z_start = val.iloc[0]
    z_cnt = val.iloc[1]
    z_step = val.iloc[2]
    return z_start, z_cnt, z_step

def getParam_csv(filename):
    pattern = (
        r"(?P<type>\w+)-"
        r"(?P<y_name>\w+)-"
        r"(?P<x_name>\w+)-"
        r"(?P<z_name>\w+)@"
        r"(?P<const_name>\w+)="
        r"(?P<const_value>[+-]?\d*\.\d+|\d+)"
        r" \[(?P<type2>\w+)_"
        r"(?P<Width>\d*\.\d+|\d+)_"
        r"(?P<Len>\d*\.\d+|\d+)_"
        r"(?P<Temp>\d+)K.*.csv"
    )
    match = re.match(pattern, filename)
    if match:
        return match.groupdict()
    else:
        print(f"Invalid filename format: {filename}")

def main():
    #***************************** 单个csv文件 *****************************************************
    # 待处理的csv文件, 后续需要写个遍历
    filename = "NMOS-id-vg-vbs@vds=0.05 [NMOS_0.22_0.35_77K(36) ; 3_8_2024 3_39_12 PM].csv"
    
    # 获取csv文件曲线数据, DataFrame 格式, 包括x, y两列数据及其名称
    curves = getCurves_csv(filename)
    num_curves = len(curves)
    # for i in range(num_curves):
    #     curve = curves[i]
    #     print(f"Curve {i+1}:")
    #     print(curve)
    #     print()
    
    # 获取csv文件参数
    # 从文件名中得到的大多数参数, 字典 格式, 通过param['index']查询
    params = getParam_csv(filename)
    # # 获取Z轴参数
    z_start, z_cnt, z_step = getZAxisVal_csv(filename)
    
    newmeafile = f"data_W_{params['Width']}_L_{params['Len']}_T_{params['Temp']}.mea"
    
    # 新建.mea文件
    f = open(newmeafile , "w")
    
    # 第一行, 可能后面需要改
    msg = ["condition{date=3/24/24,instrument=pseudo.meter,mode=forward,type=nmos}\n","\n"]
    f.writelines(msg)
    
    curve_msg = f'''Page (name=\
{params['y_name'].capitalize()}_{params['x_name'].capitalize()}_{params['z_name'].capitalize()},\
x={params['x_name'].capitalize()},\
p={params['z_name'].capitalize()},\
y={params['y_name'].capitalize()})\
{{{params['const_name'].capitalize()}={params['const_value']},\
W={params['Width']},\
L={params['Len']},\
T={params['Temp']}}}'''

    f.write(curve_msg)
    f.write("\n")
    
    # 遍历num_curves条曲线
    for i in range(num_curves):
        z_now = round((z_start + z_step * i), 1)
        msg = f"curve {{ {z_now} }}\n"
        f.write(msg)
        for j in range(len(curves[i])):
            x_val = curves[i].iloc[j, 0]
            format_x = "{:.2f}".format(x_val)
            y_val = curves[i].iloc[j, 1]
            format_y = "{:.3e}".format(y_val)
            msg = f"{format_x}			{format_y}\n"
            f.write(msg)


    f.close()


if __name__ == '__main__':
    main()