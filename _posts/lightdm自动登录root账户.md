title: xubuntu自动登录root账户
date: April 16, 2016 7:42 PM
categories: 编程
tags: [linux, ]

----


## 设置root密码
运行 `sudo passwd`
根据提示输入root帐户密码。

## 修改lightdm配置文件
运行 `ls /usr/share/lightdm/lightdm.conf.d/ -al`
-rw-r--r-- 1 root root   72 12月  3 03:57 50-greeter-wrapper.conf
-rw-r--r-- 1 root root   68 12月  3 03:57 50-guest-wrapper.conf
-rw-r--r-- 1 root root   51 12月  3 03:57 50-xserver-command.conf
-rw-r--r-- 1 root root  118  4月 16 17:08 <b>60-lightdm-gtk-greeter.conf</b>

就是greeter这个文件，不同的发行版可能名字不同。
运行 `sudo gedit /usr/share/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf`
改完以后是这样
```
[SeatDefaults]
autologin-user=root
greeter-session=lightdm-gtk-greeter
greeter-show-manual-login=true
all-guest=false
```

## 修改 `/root/.profile`
在刚修改完root权限自动登录后，发现可能开机出现以下提示：

```
Error found when loading /root/.profile
stdin:is not a tty
…………
```
运行 `gedit /root/.profile`
打开文件后找到`mesg n`，将其更改为`tty -s && mesg n`。