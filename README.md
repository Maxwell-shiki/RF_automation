2023.09.19
---

- 配置环境：anaconda3(conda 4.12.0), python 3.9.12
- tools: Everything, Qttabbar
- VScode Extension: GlassIt, Bookmarks, indent-rainbow, Markdown all in one, Material Icon Theme, One Monkai Theme, Python, Pylance, Github Copilot, Tabout  
<br>  
- 根据《用户指南》学习操作
- 接口连接P33  
  - 安装 [Key IO Libraries Suite](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html?jmpid=zzfindiolib)
  - 运行 Keysight Connection Expert 2023
  - USB: 
    - `USB0::<供应商ID>::<Prod ID>::<Serial Number>::0::INSTR`
    - 本机的VISA Adress: `USB0::0x2A8D::0x1002::MY61002637::0::INSTR`
    - 扫描后点开 Interactive IO就能控制了  

- 下载 [Command Expert](https://www.keysight.com/us/en/lib/software-detail/computer-software/command-expert-downloads-2151326.html)  
- 下载 [Benchvue](https://www.keysight.com/us/en/lib/software-detail/computer-software/benchvue-complete-control-collection-download-2814115.html) （要钱的，但好像也没啥用）  

- 安装 `keysight_kte36000`, 即 KtE36000 Driver Python API，注意版本对齐  


2023.10.08
----

- ES3631的测试程序 `ES3631A.py` 调好了，放在 ../DC_power_supply_ES3631A 目录下    


2023.10.10
----

- 写了ES3631A测试程序的帮助文档，和程序放在一个目录下  

- 开始调试Mulitmeter 3458A.  

  - [3458A 中文简明操作指南](https://edadocs.software.keysight.com/kkbopen/3458a-577943035.html)，youtube上也有个视频

  - 发现只有GPIB的接口，需要买一根GPIB/USB的转换线: [LINK](https://www.keysight.com.cn/cn/zh/product/82357B/usb-gpib-interface-high-speed-usb-2-0.html)

- 开始看AWG5202任意波发生器  

  - 要了编程手册    
  - 下载了TekVISA, 和之前那个交互界面差不多，由OpenChoice Manager启动  
  - 下了[IVI Driver](https://www.tek.com/en/support/software/driver/ivi-driver-awg70000a-awg5200-series-arbitrary-waveform)    
  - 好像Driver只有C#, LabView, VB和C++的，没找到Python的  
  - 非官方找到个这个[Python Driver](https://github.com/dahlend/TekAwg/), 但没示例程序，自己先试试   



2023.10.13
------
- GPIB转USB的线到了，开始搞Multimeter 3458A  
- [Python automation](https://www.keysight.com/us/en/assets/7018-06894/white-papers/5992-4268.pdf) Keysight的文章，蛮清楚的，说明了Keysight I/O Libraries是调Keysight的仪器都需要的，SCPI在要远程调控也是必须的  
- 但[link](https://support.keysight.com/KeysightdCX/s/knowledge-article-detail?language=en_US&keyid=Draftedarticleforcasenumber01226604)有提到3458A这个仪器生产于SCPI提出之前，所以在Keysight Connection Expert里连接时，直接`IDN?`是不会响应的，最好需要`END ON`或`END ALWAYS`, 然后`ID?`才会回复`HP3458A`，才可以进行后续的测试  
- 学习使用PyVisa，[这个](https://pyvisa.readthedocs.io/en/latest/api/visalibrarybase.html)是API  


2023.10.17
------
- 部署项目到了github, 这里有一些使用的[注意事项](https://blog.csdn.net/qq_44441669/article/details/103539420)  
- 