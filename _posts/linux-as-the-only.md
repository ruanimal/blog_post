---
title: 配置 Linux 作为主力操作系统
date: 2025-12-21 21:48:00
updated: 2025-12-22 11:47:07
categories: 编程
tags: [Linux, KDE]

---
这些年日常操作系统一直是 windows 和 macOS 交替使用，Linux 一般只作为服务器的操作系统。
然而，咖喱味的 Windows 11 （LTSC）用起来实在难受（平时只玩游戏，下载）
arm 的 macbook 虽然能效惊人，但是内存金子价格，软件也封闭（点名finder）和傲慢，实在受不了。
最后，还是转向 Linux，毕竟现在 wayland 基本堪用，国产软件也随着信创逐渐丰富了。
<!--more-->

## 发行版选择
这里选用 KDE Neon user edition，基于 Ubuntu LTS, 有以下优点
1. Ubuntu 用户基数大，有问题容易解决
2. 可以安装星火应用商店，方便使用国产软件
3. 可以用到最新的 KDE 桌面环境，wayland 支持更好
4. KDE 远程桌面好用（服务端和客户端）

```
OS: KDE neon User Edition x86_64
Host: MS-7D99 (3.0)
Kernel: Linux 6.14.0-33-generic
Uptime: 1 day, 19 hours, 23 mins
Packages: 2831 (dpkg)
Shell: bash 5.2.21
Display (E2434I-T): 1920x1080 @ 60 Hz in 24" [External]
Display (KOS2718): 3840x2160 @ 60 Hz (as 1920x1080) in 27" [External] *
DE: KDE Plasma 6.4.5
WM: KWin (Wayland)
WM Theme: Breeze
Theme: Breeze (Light) [Qt], Breeze [GTK2/3]
Icons: Breeze [Qt], breeze [GTK2/3/4]
Font: 微软雅黑 (10pt) [Qt], 微软雅黑 (10pt) [GTK2/3/4]
Terminal: /dev/pts/3
CPU: 13th Gen Intel(R) Core(TM) i5-13500 (20) @ 4.80 GHz
GPU 1: NVIDIA GeForce RTX 4060 Ti [Discrete]
GPU 2: Intel AlderLake-S GT1 @ 1.55 GHz [Integrated]
Memory: 25.07 GiB / 46.67 GiB (54%)
Swap: 392.00 KiB / 8.00 GiB (0%)
```

## 硬件要求
1. NVIDIA 显卡在 Linux 下对 Wayland 支持不好，容易出现卡死或者重启的情况，建议显示器连到核显
2. 有些主板 Linux 兼容性不行，建议使用御三家主板

## 系统设置
### Nvidia 显卡驱动
显示器插到核显上，只使用 Nvidia 做计算，玩游戏也能调用到显卡。
使用开源服务器驱动，解决 Wayland 兼容性问题，防止玩游戏崩溃

1. 安装驱动
```
sudo ubuntu-drivers install 580-server-open
```

2. 启用睡眠支持[参考](https://download.nvidia.com/XFree86/Linux-x86_64/570.172.08/README/powermanagement.html)
将显存内容保存，否则唤醒后程序会报错（如CUDA程序）
```
# /etc/modprobe.d/nvidia-power-management.conf
options nvidia NVreg_PreserveVideoMemoryAllocations=1 NVreg_TemporaryFilePath=/tmp

sudo update-initramfs

```

### docker
```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done


# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update


sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker  # 立即生效（或注销重新登录）

# docker 中调用显卡
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
```

### ipv6 启用 EUI-64
可以让 ipv6 的ip后缀根据mac生成，可用于配置防火墙规则
使用形如 `::<后缀>/::ffff:ffff:ffff:ffff` 的掩码

```
nmcli con modify <WIFI NAME> ipv6.addr-gen-mode eui64
```

### 启用休眠文件
```
sudo su
cd /
truncate -s 0 swapfile
# chattr +C swapfile  # disable COW on btrfs
fallocate -l 8G swapfile
chmod 0600 swapfile
mkswap swapfile
swapon swapfile
```

### 使用英文用户文件夹
用户个人文件夹（文档、下载等），默认是跟随系统语言。
可是中文在终端下输入不太方便，建议使用英文用户文件夹名称。
方法步骤：
1. 语言修改成英文，注销重新登录
2. 打开文件管理器，确认修改为英文
3. 语言修改回中文
4. 打开文件管理器，保留原名称

### 无线网卡调优
WIFI 启用 WOL（网络唤醒）
```
# 查看 WOL 支持
iw phy0 wowlan show
# 开启 WOL 支持
sudo iw phy0 wowlan enable magic-packet
```

关闭节能模式，解决无线网口入站延迟较大
```
cat <<EOF > /etc/NetworkManager/conf.d/wifi-powersave-off.conf
[connection]
wifi.powersave = 2

EOF

# 或者启动时设置
sudo iw dev wlo1 set power_save off
```

### 睡眠调整
睡眠到内存（suspend）耗电量很低，够用了，没必要开启混合休眠

```
# 只睡眠到内存
# 修改 /etc/systemd/sleep.conf
AllowSuspend=yes
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
SuspendState=mem standby

# 禁用休眠（可选）
sudo systemctl mask hibernate.target hybrid-sleep.target

# nvida
```

### intel 核显性能优化
10代以上 intel 核显

```
# cat /etc/modprobe.d/i915.conf
options i915 enable_fbc=1 enable_guc=2 enable_dc=0

sudo update-initramfs -u
```

### RDP 远程桌面
服务端: 使用 KDE 默认的远程桌面 （可惜稳定性一般）
客户端: `apt install krdc`

其他配置
```
# 双屏只显示其中一个屏幕
# 修改 ~/.config/systemd/user/plasma-krdp_server.service
ExecStart=/usr/bin/krdpserver --monitor 0

# 重启服务
systemctl --user daemon-reload
systemctl --user restart app-org.kde.krdpserver.service
```

### 使用新内核（可选）
发行版默认内核版本可能比较老，如有必要可以更新内核
**注意**：mainline 的内核与 ubuntu-drivers 的 nvidia 显卡驱动不兼容（所以一般不推荐）

```
sudo add-apt-repository ppa:cappelikan/ppa
sudo apt update
sudo apt install mainline
```

## 软件使用
### 常见应用替代方案
- qq: 使用官方linux版本的flatpak打包
    - flatpak install com.qq.QQ
- 任务管理器
    - flatpak install io.missioncenter.MissionCenter
- 词典：使用欧陆词典
    - flatpak install net.eudic.dict
- 微信
    - 使用星火应用商店打包的官方linux版本
- 下载管理器：
    - motrix：普通http下载
    - qbittorrent： bt下载
- 虚拟机
    - KVM：性能更好
    - VMware：易用性更好
- 游戏
    - steam：大部分游戏都可以直接运行，性能损耗也不大
- 视频播放
    - haruna：使用 flatpak 版本

### KVM 虚拟机
安装

```
sudo apt install qemu-kvm libvirt-daemon-system virt-manager
sudo usermod -aG libvirt,kvm $USER
sudo systemctl enable --now libvirtd
```

硬盘直通(scsi), 相比下面的方法性能更好
```
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native'/>
      <source dev='/dev/disk/by-id/ata-TOSHIBA' index='2'/>
      <target dev='sdg' bus='scsi'/>
    </disk>
```

硬盘直通（virtio），samba分享时可能卡顿
```
<disk type="block" device="disk">
  <driver name="qemu" type="raw" cache="none"/>
  <source dev="/dev/disk/by-id/ata-ST3000DM008"/>
  <target dev="sdc" bus="virtio"/>
</disk>
```

无线网口不支持桥接，使用路由绕过
```
# 修改 /etc/sysctl.conf; sudo sysctl -p 生效
net.ipv4.ip_forward = 1
net.ipv4.conf.wlo1.proxy_arp=1
net.ipv4.conf.br-routed.proxy_arp=1


# 创建网桥和路由
#/etc/systemd/system/bridge-routed.service
[Unit]
Description=Create routed bridge br-routed
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/usr/bin/ip link add br-routed type bridge
ExecStart=/usr/bin/ip link set br-routed up
ExecStartPost=/usr/bin/ip route add 192.168.1.41/32 dev br-routed
ExecStop=/usr/bin/ip link delete br-routed

[Install]
WantedBy=multi-user.target


# 修改 kvm 配置
<interface type="bridge">
  <mac address="00:00:00:00:00:00"/>
  <source bridge="br-routed"/>
  <target dev="vnet0"/>
  <model type="virtio"/>
  <alias name="net0"/>
  <address type="pci" domain="0x0000" bus="0x0a" slot="0x00" function="0x0"/>
</interface>

# 虚拟机使用静态ip
   IPv4 地址 . . . . . . . . . . . . : 192.168.1.41(首选)
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.1.1
   DNS 服务器  . . . . . . . . . . . : 192.168.1.1
```

### dolphin 右键菜单自定义快捷方式
支持文件和文件夹

chmod +  ~/.local/share/kio/servicemenus/mklink.desktop
```
[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=inode/directory;application/octet-stream;
Actions=RunMyScript

[Desktop Action RunMyScript]
Name=制作符号链接
Icon=emblem-symbolic-link
Exec=/home/rlj/scripts/mklink.sh "%F"
```

mklink.sh
```
#!/usr/bin/env bash

NAME=$(basename "$1")
ln -s "$NAME" "$NAME.lnk"
```

### haruna 视频播放器
haruna 是 mpv 播放器的前端，功能比较齐全


存在的问题:
- 视频播放器首次最大化窗口，总是跳到另一个屏幕
    - 关闭另一个屏幕，关闭应用，再打开，再最大化，再重新打开屏幕
- 无法重命名文件
    - 设置 flatpak 目录权限

### flatpak 使用
```
# 换源
flatpak remote-modify flathub --url=https://mirrors.ustc.edu.cn/flathub

# 目录授权，解决应用无法编辑文件
flatpak override --user org.kde.haruna --filesystem=/share
```

### 挂载 SMB 共享支持 windows 符号链接
支持原生符号链接（目录连接），双向操作都能同步

步骤
- windows 允许符号链接
计算机配置 → 管理模板 → 系统 → 文件系统 → 启用 Win32 长路径
计算机配置 → windwows设置 → 安全设置 → 本地策略 → 用户权限分配 → 创建符号链接

- samba 挂载选项
symlink=native

- 链接时使用相对路径（两个系统绝对路径不一样）


## 遇到的问题
### 故障排查方法
1. 查看系统日志 journalctl -k -b0
2. 查看用户日志，比如应用崩溃 journalctl --user -b0
3. 用 AI 搜索相关问题，如果无法解决再尝试 google 搜索

### edge 无法启动
edge 异常退出后，有概率无法启动

报错
```
Microsoft Edge 进程似乎正在使用此用户配置。
Microsoft Edge 已锁定此用户配置以防止损坏。如果你确定没有其他进程正在使用此用户配置，可以将其解锁并重新启动 Microsoft Edge。
```

处理方法，其他 chromium 内核浏览器可能也类似
```
rm ~/.config/microsoft-edge/SingletonLock
```

### steam 玩游戏卡住
dmesg 信息
```
7月 27 10:48:59 neon kernel: x86/split lock detection: #AC: CPU 0/KVM/88279 took a split_lock trap at address: 0xfffff80104613be8
7月 27 10:51:00 neon kernel: x86/split lock detection: #AC: CPU 2/KVM/88281 took a split_lock trap at address: 0xfffff8010465701c
7月 27 10:52:51 neon kernel: x86/split lock detection: #AC: CHTTPClientThre/90929 took a split_lock trap at address: 0xf098fc4f
7月 27 10:53:07 neon kernel: x86/split lock detection: #AC: CPU 1/KVM/88280 took a split_lock trap at address: 0xfffff8010465701c
```

解决方法
```
# 编辑 /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT='quiet splash split_lock_detect=off'

sudo update-grub
```

### 迁移系统&修复引导
1. 进入 livecd，使用 Gparted 复制系统到新硬盘
2. 修改新硬盘分区的 /etc/fstab 的挂载点 uuid
3. 重建 grub 引导
```
mount /dev/sdaX /mnt/
mount /dev/sda0 /mnt/boot/efi
for i in {proc,dev/sys}; do
  mount --bind /${i} /mnt/${i}
done

chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi
```

### 睡眠唤醒后很卡
桌面很卡，cpu 频率上不来，只有 800mhz。
映泰主板兼容性问题，换主板解决

### 终端删除文件到回收站
```
sudo apt install trash-cli
alias rm=trash
```

### electorn 应用无法启动
报错 chrome sandbox 相关

```
# 编辑 /etc/sysctl.conf 添加
kernel.apparmor_restrict_unprivileged_userns=0

# 生效
sudo sysctl -p
```

### 登录界面隐藏无关用户
比如某些用于文件共享的用户

```
# 修改 /etc/sddm.conf
[Autologin]
Session=plasma

[Users]
HideUsers=data,data-r,data-s
HideShells=/usr/sbin/nologin,/bin/false
```

### 偶发硬件设备工作不正常
强制重启后或者系统崩溃后，如果设备不正常，可以尝试重启到 windows 再切回 linux


### 应用在启动器里找不到

```
rm -f ~/.config/menus/
kbuildsycoca6 --noincremental
```

### 修复睡眠唤醒问题
睡眠之后可能出现莫名奇妙的唤醒

```
# 查看当前唤醒触发器
cat /proc/acpi/wakeup | grep enable

# 查看触发器的设备路径
for p in /sys/class/wakeup/*/device/power/wakeup; do
    dev=$(dirname $(dirname $p));
    dev_path=$(realpath $dev)
    echo ${dev_path}
done


# 直接修改是 /proc/acpi/wakeup 是不生效的
# 设置具体设备的方式禁用 rtc 和 AWAC, 位置格式 ${dev_path}/power/wakeup
# 可以将禁用命令配置到 rc.local
echo disabled | tee /sys/devices/platform/rtc_cmos/power/wakeup  # rtc
echo disabled | tee /sys/devices/platform/rtc_cmos/rtc/rtc0/alarmtimer.0.auto/power/wakeup # rtc
echo disabled | tee /sys/devices/platform/ACPI000E:00/power/wakeup  # AWAC

# 检查是否生效
cat /proc/acpi/wakeup | grep enable
```

### apt 设置代理

部分 apt ppa 源需要代理，但是国内的镜像源却不需要。
所以需要给每一个源单独设置代理的功能

有两种设置方式
- 白名单模式（只给需要的配置）
- 黑名单模式（先设置默认代理， 不需要的设置直连）

设置语法
- 设置代理服务器：`Acquire::http::Proxy <proxy-server>`
- 设置某个域名的代理：`Acquire::http::proxy::<domain> <proxy-server|DIRECT>`

示例
```
#  /etc/apt/apt.conf.d/99proxy

# 给每种协议的源设置代理，一般设置 https::Proxy 就行了
#Acquire::http::Proxy "http://yourproxyaddress:proxyport";
#Acquire::https::Proxy "http://yourproxyaddress:proxyport";
#Acquire::ftp::Proxy "http://yourproxyaddress:proxyport";
#Acquire::socks::Proxy "http://yourproxyaddress:proxyport";

# 设置具体域名是否走代理
#Acquire::http::proxy::local.mirror.address "DIRECT";
#Acquire::http::proxy::HOST_NAME_TO_BE_PROXIED "http://yourproxyaddress:proxyport"

# 黑名单模式示例
Acquire::https::Proxy "http://localhost:10808";
Acquire::https::Proxy::"mirrors.aliyun.com" "DIRECT";

```

### 限制硬盘读写速度
某些nvme硬盘的发热很严重, 如果全速运行会导致系统不稳定.
所以需要对硬盘速度进行限制


使用 systemd 设置限速
```shell
# 创建配置目录
sudo mkdir -p mkdir -p /etc/systemd/system/{user,system}.slice.d/

# 设置用户限制
sudo tee /etc/systemd/system/user.slice.d/io-limit.conf  > /dev/null <<EOF
[Slice]
IOReadBandwidthMax=/dev/nvme0n1 800M
IOWriteBandwidthMax=/dev/nvme0n1 300M
IOReadIOPSMax=/dev/nvme0n1 60000
IOWriteIOPSMax=/dev/nvme0n1 30000

EOF

# 系统也使用同样的限制
sudo ln -sf /etc/systemd/system/user.slice.d/io-limit.conf /etc/systemd/system/system.slice.d/

```

速度测试
```shell
~$ dd if=/dev/zero of=testfile bs=1M count=2048 oflag=direct status=progress && rm  testfile
2099249152 bytes (2.1 GB, 2.0 GiB) copied, 7 s, 300 MB/s
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB, 2.0 GiB) copied, 7.16429 s, 300 MB/s
```
