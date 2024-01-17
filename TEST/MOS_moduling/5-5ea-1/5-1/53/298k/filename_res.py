import os
import re
import csv

def get_filename_list():
    # 获取当前脚本所在目录
    current_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_path)

    file_pattern = re.compile(r'(.*)\.csv')

    # 遍历当前目录下的所有csv文件名, 并将其路径存入列表
    filename_list = []
    for filename in os.listdir(current_path):
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
        r'(?P<Len>\d+)-'
        r'(?P<Width>\d*\.\d+)-'
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
            'Len': int(match.group('Len')),                         # 管子长度
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

    # 示例
    # parsed_components = parse_filename_components(filename)
    # print(parsed_components)
    # print(parsed_components['Type'])

def main():
    filename_list = get_filename_list()
    # print(filename_list)

    for filename in filename_list:
        parsed_components = parse_filename_components(filename)
        print(parsed_components)

if __name__ == '__main__':
    main()
