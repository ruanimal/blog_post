title: Windows Subsystem for Linux(WSL) 简单指引
date: 2017-01-08 20:00
categories: 编程
tags: [linux, WSL]

----

## 简介

　　`Windows Subsystem for Linux`（简称WSL）是一个为在Windows 10上能够原生运行Linux二进制可执行文件（ELF格式）的兼容层。它是由微软与Canonical公司合作开发，目标是使纯正的Ubuntu 14.04 "Trusty Tahr"映像能下载和解压到用户的本地计算机，并且映像内的工具和实用工具能在此子系统上原生运行。
　　WSL提供了一个微软开发的Linux兼容内核接口（不包含Linux代码），来自Ubuntu的用户模式二进制文件在其上运行。

　　此功能组件从Win10 Insider Preview build 14316开始可用，正式版是Win10 RedStone1才可用，并且只有64位系统才有此功能。我目前的系统是预览版Insider Preview build 14986，相比正式版Win10 RedStone1版本WSL功能会完善些，但系统就不稳定些了。建议大家还是用Win10 RedStone1吧

　　WSL 的出现解决了很大程度上解决了Windows用户使用linux工具链的需求，同时也解决部分用户（比如我）在Linux与Windows之间切换的麻烦。


**WSL的优点**
- 提高了接近原生Linux的使用体验，Python，Shell等开发环境与linux下基本相同
- 使用Bash进行一些日常操作比CMD高校和方便多了
- 资源利用效率，以及启动速度比虚拟机快多了，而且不用担心文件共享的问题

<!--more-->

**WSL的不足**
- WSL目前属于测试阶段（beta），一些与内核关系紧密的软件包就不能用了，比如`systemd`，`iptables`等
- 关闭WSL窗口后，后台进程全部会退出，实现后台服务有难度。
- WSL内部和外部的二进制程序并不能通用，也就是WSL里不能调用Win程序，Win也不能调用WSL里的程序。
- 文件权限管理，在WSL中可访问win中的文件，不过文件的权限均为777

## 安装
1. 开启开发者模式： 设置 > 更新及安全 > 针对开发人员 > 开发人员模式
![](http://image.runjf.com/17-1-8/91407501-file_1483888101129_101b0.gif)

2. 启用WSL功能：资源管理器地址栏输入 “控制面板\程序\程序和功能”，选择启用或关闭Windows功能，勾选适用于Linux的Windwos子系统(beta)，重启系统
![](http://image.runjf.com/17-1-8/87068378-file_1483888094877_143b7.png)

3. 下载Linux镜像：按`Win + X`选择“命令提示符”或者“Windows PowerShell”，在命令行中输入`bash`，按提示操作。安装完成后使用也是在命令行中输入`bash`
![](http://image.runjf.com/17-1-8/71864116-file_1483888221167_146b1.png)
![](http://image.runjf.com/17-1-8/275971-file_1483888221026_4896.png)

**也可以看MS的官方教程**[WSL install guide](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide)

## 替换WSL终端

可以用`mintty`作为WSL的终端，替换命令提示符，获得更类似linux的体验。github中已经有人做好了，下载使用即可[goreliu/wsl-terminal](https://github.com/goreliu/wsl-terminal/releases)
解压运行open-wsl.exe，你就得到了一个漂亮的linux终端。
![](http://image.runjf.com/17-1-8/57114153-file_1483889057173_a2dd.png)

## 在右键菜单中添加在此处打开WSL
新建文本文件，用记事本打开，输入一下内容，替换里面的两处路径，保存重命名为`wsl.reg`，运行。
```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\wsl]
@="WSL Here"
"Icon"="\"D:\\PortableApps\\wsl-terminal\\open-wsl.ico\""

[HKEY_CLASSES_ROOT\Directory\Background\shell\wsl\command]
@="D:\\PortableApps\\wsl-terminal\\open-wsl.exe"
```
![](http://image.runjf.com/17-1-8/4400425-file_1483888101002_ba17.png)

## 运行linux桌面
1. 在WSL里安装好桌面，`apt-get -y install xorg xfce4`
2. 在win上安装`x server`，可选`xming`和`VcXsrv`，这里选用[VcXsrv](https://sourceforge.net/projects/vcxsrv/)
3. 启动`x server`
![](http://image.runjf.com/17-1-8/7879750-file_1483888094999_453c.png)
![](http://image.runjf.com/17-1-8/86091829-file_1483889277522_60b1.png)
![](http://image.runjf.com/17-1-8/74401307-file_1483888095234_162aa.png)
![](http://image.runjf.com/17-1-8/59701947-file_1483888095343_17660.png)
![](http://image.runjf.com/17-1-8/85096906-file_1483888095449_1787e.png)

4. WSL的配置，在wsl的bash中运行
```
echo "export DISPLAY=:0.0" >> ~/.bashrc  # 设置屏幕为x server
source ~/.bashrc
sudo sed -i 's$<listen>.*</listen>$<listen>tcp:host=localhost,port=0</listen>$' /etc/dbus-1/session.conf  # 解决D-bus的问题
```
5. 在WSL里运行`startxfce4`，就此大功告成
![](http://image.runjf.com/17-1-8/26700478-file_1483888100890_f880.png)
![](http://image.runjf.com/17-1-8/4581644-file_1483888100682_e456.png)
