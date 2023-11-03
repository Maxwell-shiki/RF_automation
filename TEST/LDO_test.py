import sys, os

# 相对路径导入
sys.path.append("..\\modules\\DCPowerSupply_ES3631A")
from DCPowerSupply_ES3631A import DCPowerSupply_ES3631A  # 第一个是.py文件名，第二个是类名



def main():
    resource_name = "USB0::0x2A8D::0x1002::MY61003060::0::INSTR"
    DCPS = DCPowerSupply_ES3631A(resource_name)
    DCPS.set_voltage(5.0, 1)
    DCPS.close()

if __name__ == "__main__":
    main()