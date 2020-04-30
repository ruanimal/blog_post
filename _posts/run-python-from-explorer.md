title: 从windows资源管理器启动Python脚本
date: 2018-02-04 10:40 AM
categories: 编程
tags:  [Python, ]

----

有时想给windows的资源管理器增加一些自定义的功能，比如创建目录联接到某个目录。

## 思路
给windows的资源管理器添加一个右键菜单，调用你想要运行的程序或脚本，理论上可以实现任意功能。

## 实现
**那么我们就开始py一个脚本吧, 创建目录联接到指定目录**

```python
import os, sys, subprocess

if len(sys.argv) < 2:
    exit()

p = sys.argv[1]  # 目标路径通过命令行参数传入
base_dir, name = os.path.split(p)

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW   # 隐藏subprocess运行的命令窗口
cmd = 'mklink /J {} {}'.format(os.path.join('E:\\share', name), p)
subprocess.call(cmd, startupinfo=si, shell=True)
```
<!--more-->
**修改注册表,添加右键菜单**

复制这段保存为 add_to_share.reg 双击执行导入

```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\shell\share]
@="添加到共享文件夹"

[HKEY_CLASSES_ROOT\Directory\shell\share\command]
@="\"D:\\lib\\python3\\pythonw.exe\" \"D:\\Scripts\\link_to_share.py\" \"%1\""
; D:\\lib\\python3\\pythonw.exe 这是python解释器路径, pythonw.exe 执行时不会有解释器窗口
; D:\\Scripts\\link_to_share.py 脚本路径
; %1 选中的文件夹全路径
```

### 效果
![](http://image.runjf.com/18-2-4/77007025.jpg)
![](http://image.runjf.com/18-2-4/54072201.jpg)
