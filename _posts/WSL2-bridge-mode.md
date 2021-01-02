title: WSL2开启桥接网络
date: 2021-01-02 15:00
categories: 工作生活
tags: [linux, WSL]

----


## 安装WSL2
参考[官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10#manual-installation-steps)安装WSL2

在PowerShell中执行以下命令
1. 启用WSL2 `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
2. 启用虚拟机平台 `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
3. 启用Hyper-V `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
4. 设置WSL2为默认 `wsl --set-default-version 2`

然后重启系统, 安装[适用于 x64 计算机的 WSL2 Linux 内核更新包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

## 安装Linux发行版
这里选择Debian作为示例

1. 在`Microsoft Store`中搜索Debian并安装
2. 启动Debian应用，并根据提示初始化系统
3. 在PowerShell执行`wsl -l --all -v`确认WSL版本为2
    ```
    PS C:\Users\ruan> wsl -l --all -v
    NAME      STATE           VERSION
    * Debian    Running         2
    ```
4. 如果VERSION不为为2，在PowerShell执行`wsl --set-version Debian 2`进行升级

## 修改WSL2默认网络为桥接
由于WSL2底层使用的是Hyper-V虚拟机，所以我们可以修改虚拟交换机的类型，来启用桥接网络
打开`Hyper-V管理器 -> 操作 -> 虚拟交换机管理器`， 修改WSL的连接类型为“外部网络”

## 修复Debian网络
由于WSL2默认网络模式是NAT，我们把虚拟交换机改为桥接后，默认的ip和路由以及DNS解析将会失效

以下操作在Debian系统内执行

### 修复ip和路由
1. 清除原网卡ip `ip addr flush dev eth0`
2. 添加新ip `ip addr add 192.168.123.31/24 dev eth0`
3. 清除原默认路由 `ip route delete default`
4. 添加默认路由 `ip route add default via 192.168.123.1 dev eth0`

这些操作在重启WSL2虚拟机后会失效，如果永久修改，请配置静态ip

### 修复DNS解析
1. 新建`/etc/wsl.conf`，防止WSL2覆盖DNS配置文件
    ```
    [network]
    generateResolvConf = false
    ```
2. 编辑`/etc/resolv.conf`， 清除原配置，添加以下内容
    ```
    nameserver 192.168.123.1
    ```

## 参考
   1. https://docs.microsoft.com/zh-cn/windows/wsl/install-win10#manual-installation-steps
   2. https://github.com/microsoft/WSL/issues/4928#issuecomment-646703350
   3. https://github.com/microsoft/WSL/issues/4150#issuecomment-747152240
