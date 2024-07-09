title: 树莓派系统备份
date: 2020-10-31 8:17 PM
categories: 工作生活
tags: [树莓派, Linux]

----

在玩树莓派的过程中难免会碰到如何高效的备份系统的问题。

由于树莓派用的是Linux系统，所以常见的有两种备份方式
1. 基于文件的备份，比如tar，rsync
2. 基于磁盘的备份，比如dd

这两种备份方式各有利弊：
基于文件的备份占用空间小，而且可以在系统在线时操作，比较方便，但是当要还原整个系统时就会比较麻烦（引导重建等等）。
基于磁盘的备份就比较简单粗暴了，直接克隆硬盘，恢复时直接还原映像文件就好了，但是由于是整盘备份，空间占用比较大。

<!--more-->

我这里是采用的第二种备份方式，通过缩减分区大小，排除未使用空间来减小备份文件大小

## 具体步骤
首先需要将树莓派的SD取下，插入到一台Linux机器上。

### 使用Gparted缩小分区
这一步操作比较耗时，跟SD卡大小和速度有关，基本在几分钟到几十分钟不等。

![-w761](https://image.ponder.work/mweb/2020-11-01-16041166087052.jpg)
![-w764](https://image.ponder.work/mweb/2020-11-01-16041166419441.jpg)
![-w760](https://image.ponder.work/mweb/2020-11-01-16041167175534.jpg)
![-w756](https://image.ponder.work/mweb/2020-11-01-16041167579651.jpg)
![-w764](https://image.ponder.work/mweb/2020-11-01-16041167920279.jpg)
![-w708](https://image.ponder.work/mweb/2020-11-01-16041169311741.jpg)

### 挂载网络存储
如果不想把备份文件存到网络存储上，该步骤可以忽略

```shell
sudo  mount.cifs -o vers=2.0,user=${nas_user},password=${nas_password},uid=$(id -u),gid=$(id -g) \
	//192.168.123.100/D-soft/ /mnt/
```

### 使用DD备份硬盘
```shell
sudo dd if=/dev/sda of=/mnt/backup.img bs=1M count=6000 status=progress
```

备份耗时跟SD卡大小和速度有关，基本在几分钟到几十分钟不等。

bs参数代表备份文件大小的单位，这里是1M

count代表有多少bs，也就是备份大小是`count*bs=6000M`
这个数值需要根据你磁盘使用空间来计算，取一个大于已使用空间的值就好了。

例如，我这个SD卡已使用的空间是 `4M + 256M + 5.24GiB = 5625.76M`，则备份大小取6000M

### 还原系统
还原系统和新安装系统是一样的，用官方的[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)还原备份镜像文件即可

还原完成之后，还需要使用Gparted将缩小的分区还原到原来的大小，耗时大概十几秒。

然后插卡开机即可
