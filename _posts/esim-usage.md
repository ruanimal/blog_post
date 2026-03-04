---
title: esim 使用相关
date: 2026-03-04 01:02:56
updated: 2026-03-04 01:02:56
categories:
  - 工作生活
tags: [esim, Android]
---

国行手机的 esim 功能有较多限制，使用不太方便。
但我们可以使用 esim 适配器，将 esim 转为实体 sim 卡。
<!--more-->
## esim 适配器
esim 适配器就是个 sim 卡，需要占用一个卡槽，可以通过软件将 esim 卡号写入到适配器。
可以写入多个 esim 号码，并且支持切换，但同时只能有一个在线。
适配器有不少品牌，如 estk、5ber、9esim，价格也各不相同，但是我都没怎么试过。
我使用的的适配器是 pdd 购买，20-30元，容量468KB。


## esim 套餐
一般海外套餐都可以使用，我这里只用于接收短信，故使用 clubsim。成本大概50元。


## 号码写入
购买套餐后，运营商会提供二维码，安卓手机通过 [OpenEUICC](https://gitea.angry.im/PeterCxy/OpenEUICC) 扫描就可以写入和管理 esim。

如果是 iphone，需要使用 esim 读卡器来管理 esim 号码。

## 注意事项
由于安卓操作系统（11+）的 bug，在“移动网络”中禁用 esim 适配器会无法打开。
需要通过 adb 清除移动网络的数据才能恢复
```
adb shell pm clear com.android.providers.telephony
```

如果是小米等手机，清除过程可能会遇到adb权限相关问题
需要额外开启开发者选项中的“OEM解锁”和“USB调试（安全设置）”
```
adb shell pm clear com.android.providers.telephony

Exception occurred while executing 'clear':
java.lang.SecurityException: PID 29160 does not have permission android.permission.CLEAR_APP_USER_DATA to clear data of package com.android.providers.telephony
	at com.android.server.am.ActivityManagerService.clearApplicationUserData(ActivityManagerService.java:4101)
	at com.android.server.am.ActivityManagerService.clearApplicationUserData(ActivityManagerService.java:4054)
	at com.android.server.pm.PackageManagerShellCommand.runClear(PackageManagerShellCommand.java:2385)
	at com.android.server.pm.PackageManagerShellCommand.onCommand(PackageManagerShellCommand.java:289)
	at com.android.modules.utils.BasicShellCommandHandler.exec(BasicShellCommandHandler.java:97)
	at android.os.ShellCommand.exec(ShellCommand.java:38)
	at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onShellCommand(PackageManagerService.java:7022)
	at android.os.Binder.shellCommand(Binder.java:1158)
	at android.os.Binder.onTransact(Binder.java:960)
	at android.content.pm.IPackageManager$Stub.onTransact(IPackageManager.java:4729)
	at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onTransact(PackageManagerService.java:7006)
	at android.os.Binder.execTransactInternal(Binder.java:1433)
	at android.os.Binder.execTransact(Binder.java:1372)
```

## 参考
- https://linux.do/t/topic/1276447/5
- https://v2.b2og.com/archives/15