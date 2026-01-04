---
title: ubuntu静态ip配置
date: 2016-04-16 20:52:00
updated: 2016-08-25 18:05:00
categories: 编程
tags: [Ubuntu, Linux]
---

以vmware虚拟机为例

## 设置IP
运行 `sudo nano /etc/network/interfaces`
将文件修改成如下：
```
auto eth0  # eth0是网卡名称，你的不一定是这个，可通过ifconfig查看
iface eth0 inet static
address 192.168.157.129   # 地址
gateway 192.168.157.2    # 网关
netmask 255.255.255.0   # 掩码
```

## 修改DNS
运行 `sudo nano /etc/resolvconf/resolv.conf.d/base`
把文件改成 `nameserver 192.168.157.2`
把`192.168.157.2`改成你需要的dns，这里因为是vmware的NAT模式，所以dns和网关是一样的。

