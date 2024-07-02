import csv
import sys, os

# 进行对csv文件 波形文件的数据处理
def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def main():
    csv_data = read_csv('1.csv')
    # 从第7行开始读取，分开横纵轴数据
    # 第7行开始的数据格式为
    # ,,, [x_data],    [y_data]
    x_list = []
    y_list = []
    for i in range(6, len(csv_data)):
        # 去除数据两端空格，转换为float
        x_list.append(float(csv_data[i][3].strip()))
        y_list.append(float(csv_data[i][4].strip()))
    
    # 获取y_list中的最大值和最小值
    y_max = max(y_list)
    y_min = min(y_list)
    delta_y = y_max - y_min

    print('y_max = ', y_max)
    print('y_min = ', y_min)
    print('delta_y = ', delta_y)
    



if __name__ == '__main__':
    main()