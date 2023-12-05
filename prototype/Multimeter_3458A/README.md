Keysight Multimeter 3458A 数字万用表 测试程序使用说明
---

### 1. 示例程序

- 测试程序示例`test_example.py`放在 [tests目录](./tests)下  


### 2. 基本支持功能

- `set_function`: 设置测量功能，参数支持 `DCV`, `DCI`, `OHM`等  
- `set_range`: 设置量程，param1 为模式，和功能设置参数一致；param2 为量程值，注意和功能对应，具体对应值见[用户指南](./manual/操作和维修指南.pdf)
- `get_data`: 获取仪器显示数据，返回类型为float
- `test`: 仪器自检

