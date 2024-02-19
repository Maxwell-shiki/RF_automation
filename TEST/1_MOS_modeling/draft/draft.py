import csv
import sys, os
import subprocess
import matplotlib.pyplot as plt
import numpy as np

# 读取csv文件
file_path = './data.csv'
matrix = []
with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csvfile.read().split('\n')
    for row in reader:
        row_data = row.split(', ')
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
    plt.plot(curv_data[i][:,0], curv_data[i][:,1], label=f"curv{i+1}@vgs")

plt.xlabel(X_axis_name)
plt.ylabel(Y_axis_name)
plt.title('NMOS-id-vd-vgs@vbs=-3.3')

# 存储图像
plt.legend(fontsize=8)
plt.savefig('./img/pic1.png')

plt.show()
