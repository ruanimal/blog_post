---
title: Windows 网络共享
date: 2021-10-10 15:00:00
updated: 2024-07-09 22:02:56
categories: 工作生活
tags: [Windows,]

---
要在不暴露 client 的情况下共享网络，一般就只能使用 nat(Network Address Translation), linux 下可以使用 iptables 很轻松地搞定。
nat 包含 DNAT 和 SNAT, 要想双向互通，必须两者都实现。

windows下的网络共享只有SNAT那一部分，比如各自免费wifi软件。少了DNAT，外部网络就无法访问内部。

还好windows下可以配置端口转发，实现等效的DNAT
<!--more-->
## 先配置网络共享
前置要求，需要两张网卡，无线或者有线均可。
- A: 用于访问外网
- B: 共享网络接入点

打开：控制面板 》网络和Internet 》网络和共享中心 》更改适配器设置

![](https://image.ponder.work/mweb/2021-10-10-16338760513347.jpg)

![](https://image.ponder.work/mweb/2021-10-10-16338761455929.jpg)

右键A网卡 > 属性 > 共享 > 勾选允许 （win10可能有下拉选择，下拉选中B网卡）
![](https://image.ponder.work/mweb/2021-10-10-16338761903207.jpg)

## 端口映射配置
netsh是Windows自带的端口转发/端口映射工具。

支持IPv4和IPv6,命令即时生效,重启系统后配置仍然存在。

### 常用命令

* add - 在一个表格中添加一个配置项。
* delete - 从一个表格中删除一个配置项。
* dump - 显示一个配置脚本。
* help - 显示命令列表。
* reset - 重置端口代理配置状态。
* set - 设置配置信息。
* show - 显示信息。

### 用法(以v4tov4为例)
```
add v4tov4 [listenport=]integer>|servicename> \
           [connectaddress=]IPv4 address>|hostname>  \
           [[connectport=]integer>|servicename>]  \
           [[listenaddress=]IPv4 address>|hostname>]  \
           [[protocol=]tcp]
```

### 参数说明

* listenport      - IPv4 侦听端口。
* connectaddress  - IPv4 连接地址。
* connectport     - IPv4 连接端口。
* listenaddress   - IPv4 侦听地址。
* protocol     - 使用的协议。现在只支持 TCP

### 案例(ssh端口转发)
将192.168.8.108的22端口映射到本地的2222端口

这样外部就可以通过本地的对外ip来ssh访问192.168.8.108了
```
netsh interface portproxy add v4tov4 listenport=2222 connectaddress=192.168.8.108 connectport=22
```

### 显示端口转发
一般情况下使用下列命令进行查看

```
netsh interface portproxy show all
```
