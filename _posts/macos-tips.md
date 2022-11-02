title: macOS 使用技巧
date: 2021-10-10 3:00 PM
categories: 工作生活
tags: [mac,]

----

对程序员来说，macOS 就是一个桌面支持比较好的 Linux/Unix，给日常开发带来了许多便利

本文记录一些日常使用中的小技巧。
<!--more-->
## macOS mojave 密码位数限制
苹果在10.14的系统上增加了密码最小长度的限制
可以通过这个命令去除

```bash
pwpolicy -clearaccountpolicies 
```

**注意**：去除限制之后，通过time machine备份的系统，还原到有限制的机器上，可能会导致一些bug。如卡死在登陆页面，部分应用的资源库损坏等等。

## 重置账户、配置
如果出现上面的问题，可以尝试重置下系统设置（选择任意一种，建议选1或2）

1. 新建管理员账号，在新机器上去除密码限制。
2. 进入恢复模式（开机按command+r），删除对应用户账户配置文件（恢复模式下文件挂载路径可能不同）, 重新开机
```bash
mv ~/Library/Preferences ~/Library/Preferences.bak
mv ~/Library/PreferencePanes ~/Library/PreferencePanes.bak
```

3. 清除机器配置状态，重新设置一个新账户（开机按住command+s；）
```bash
/sbin/mount -uaw
rm var/db/.applesetupdone
reboot
```

## Mac 开启任何来源选项
```
sudo spctl --master-disable
```


## 让系统更流畅
macOS 10.14 以后系统动画越来越复杂，对显卡要求比较高，导致配置比较老的设备运行起来很卡顿。
特别是big sur系统，使用intel核显的机器都不建议安装。

通过关闭一些动画和特效可以让系统更流畅些

![](http://image.runjf.com/mweb/2021-10-10-16338756772783.jpg)

## 键位修改
使用 [karabiner](https://karabiner-elements.pqrs.org/) 可以对系统全局快捷键和应用快捷键进行修改。

通过配置 karabiner 将 command，control，option 按键进行重映射，可以让 macOS 的键位 和 Windows/Linux 接近。


## 使 macOS 的命令风格与Linux相同
macOS 的命令应该是 Unix 风格的，和 Linux 有些不同，可选参数必须放在前面，会有些不方便。
比如
```shell
# mac
➜  ~ /bin/ls /tmp -al
ls: -al: No such file or directory
```

可以安装 gnu 工具，覆盖这些命令
```bash
brew install coreutils findutils gnu-tar htop
export   PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"
export  MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"
```

## 清除一些 macOS 系统默认快捷键

创建文件 ~/Library/KeyBindings/DefaultKeyBinding.dict
这里是清除了默认的 `Control + Command + 方向键`的行为

修改完成后必须重新打开现有app才能生效

```
{
"^@\UF701" = ("noop:");
"^@\UF702" = ("noop:");
"^@\UF703" = ("noop:");
}
```

字符含义

| Prefix | Meaning |
| --- | --- |
| `~` | ⌥ Option key |
| `$` | ⇧ Shift key |
| `^` | ^ Control key |
| `@` | ⌘ Command key |
| `#` | keys on number pad |

参考：
- http://xahlee.info/kbd/osx_keybinding.html
- https://blog.victormendonca.com/2020/04/27/how-to-change-macos-key-bindings/

## 关闭启动声音
```
# 关闭提示音
sudo nvram StartupMute=%01

# 打开duang
sudo nvram StartupMute=%00
```

## crontab 文件路径
用户执行`crontab -e`之后定时任务存储位置`/private/var/at/tabs/<username>`

## hostname 更改
macos 默认没有设置hostname，导致终端`PS1`显示时会用网卡的mac地址作为主机名，看起来比较别扭。

可以通过`sudo scutil --set HostName <name>`设置想要的主机名

```
➜  ~ hostname
a8a159010000
➜  ~ scutil --get HostName
HostName: not set
➜  ~ sudo scutil --set HostName Mac-mini
Password:
➜  ~ hostname
ruandeMac-mini
```

## catalina 禁用系统更新提示
在终端中输入
```
defaults write com.apple.systempreferences AttentionPrefBundleIDs 0 ; killall  Dock
```

在 /etc/hosts 中加入
```
# disable mac update
0.0.0.0 swdist.apple.com.edgekey.net
0.0.0.0 swdist.apple.com.akadns.net
```

## 固定dock位置，防止在不同屏幕间移动
```
defaults write com.apple.Dock position-immutable -bool yes; killall Dock
```