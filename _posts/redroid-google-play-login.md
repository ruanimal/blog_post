---
title: redroid “设备未获得play保护机制认证” 问题
date: 2025-05-07 18:00:00
updated: 2025-05-08 15:05:34
categories: 工作生活
tags: [Android]

---
使用 redroid 等安卓虚拟环境，可能会发现 google play 用不了的问题。
虽然系统集成了 gapps，但系统提示 “设备未获得play保护机制认证”，无法登录 play 商店。
可能的原因比较多，这里大概是因为虚拟机的型号没在google的数据库里。
解决方案就是，获取 GSF ID 注册到 Google。
<!--more-->
![](https://image.ponder.work/mweb/2025-05-08---17466861942743.jpg)
## 步骤
1. 安装 [device id](https://apkpure.com/device-id/vtechnotm.com.deviceid)
2. 打开应用，复制 GSF id，假设为`ffffffff`
3. 终端运行`printf "%d\n" 0xffffffff`，转换换成10进制数字。
4. 打开 https://www.google.com/android/uncertified/ 输入转换后的结果并提交

![](https://image.ponder.work/mweb/2025-05-08---17466877549957.jpg)
 