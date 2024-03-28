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
        r" \[(?P<type2>\w+)_"                       # 注意根据.csv文件命名格式 修改分隔符 "-" or "_"
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
    csvfilelist = getFilelist_csv('.')
    csvfile_tmp = csvfilelist[0]
    params = getParam_csv(csvfile_tmp)
    newmeafile = f"data_W_{params['Width']}_L_{params['Len']}_T_{params['Temp']}.mea"
    
    f = open(newmeafile , "w")

    # 第一行, 可能后面需要改
    msg = ["condition{date=3/24/24,instrument=pseudo.meter,mode=forward,type=nmos}\n","\n"]
    f.writelines(msg)
    
    for csvfile in csvfilelist:
        print(f"Processing: {csvfile} ...")
        curves = getCurves_csv(csvfile)
        num_curves = len(curves)
        params = getParam_csv(csvfile)
        z_start, z_cnt, z_step = getZAxisVal_csv(csvfile)
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
        
        print()
    

    
    f.close()


if __name__ == '__main__':
    main()