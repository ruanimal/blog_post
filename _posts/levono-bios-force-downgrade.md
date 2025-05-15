title: 联想笔记本 BIOS 跳过检测强制降级
date: 2025-05-15 18:00
categories: 工作生活
tags: [硬件]

----

联想某些版本的 bios 似乎会禁止降级，即使打开 bios 设置里的允许降级选项，依然会提示 "this platform does not support IHISI interface" 的错误，导致降级失败。
<!--more-->

## 降级方法
经过一些尝试，找到了方法绕过，以 `ThinkBook 14 G3 ACL` 机型为例
1. 打开驱动[下载页面](https://newthink.lenovo.com.cn/driveList.html?selname=21A2004H0D) 
2. 打开 [BIOS](https://think.lenovo.com.cn/support/driver/driverdetail.aspx?DEditid=134398) 页面， 下载以下安装文件
    - 当前版本 BIOS 的安装包（`NEW`），版本 GQCN41WW_HFCN36WW
    - 以及想要降级的 BIOS (`OLD`)，版本 GQCN36WW_HFCN31WW
3. 运行 `NEW`，选择仅解压。找到解压目录，应该只有一个 exe 程序，使用 7-zip 或者 bandizip 打开并提取内部文件。
4. 对 `OLD` 也执行如上操作，如果没有解压选项，可以尝试直接提取。
5. 将 `OLD` 提取目录中的 .bin 格式固件（GLV3A036.bin、GLV4D031.bin）复制到 `NEW` 提取目录中。
6. 修改 `NEW` 提取目录中的 `platform.ini` 文件，找到如下内容
    ```
    [MULTI_FD]
    Flag=1
    FD#01=ID,GLV4D,GLV4D036.bin
    FD#02=PCI,0,1,1,0,FFFFFFFF,FFFFFFFF,GLV3A041.bin
    ```
    
    将其中的 .bin 文件名，修改为 `OLD` 中的 .bin 文件名，保存。
    有两个 .bin 文件，文件名是和版本中的数字对应的，不要修改错误。
    ```
    [MULTI_FD]
    Flag=1
    FD#01=ID,GLV4D,GLV4D031.bin
    FD#02=PCI,0,1,1,0,FFFFFFFF,FFFFFFFF,GLV3A036.bin
    ```
7. 运行 `NEW` 提取目录中的 H2OFFT-Wx64.exe，等待降级完成。

**注意：有风险，请谨慎操作。不要跨太多版本，可能有不可预料的问题**

![](https://image.ponder.work/mweb/2025-05-15---17473119676089.jpg)


## 参考
- https://www.geektech.co.nz/lenovo-y700-how-to-enable-bios-downgrade