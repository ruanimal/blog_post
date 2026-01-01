---
title: 在 iOS 上访问安卓应用
date: 2025-04-26 18:00:00
updated: 2025-04-27 14:53:17
categories: 工作生活
tags: [Android, iOS]

---
有些应用在安卓上是独占的，iOS 上又没有比较好的替代品，而且 iOS 上没有能用安卓模拟器。
如果使用多个设备，维护的心智成本又高，被这个问题困扰了许久。

最近碰巧了解了 [scrcpy](https://github.com/Genymobile/scrcpy), 用于远程控制安卓，终于解决了这个问题。
<!--more-->

需要的工具
1. 安卓环境：虚拟环境或者物理设备均可，这里使用虚拟环境。以下是可选的虚拟环境
- PVE 的 PCT容器 (Proxmox Container Toolkit)，需要打[补丁](https://github.com/lurenJBD/PCT-patches)
- docker，基于[Redroid](https://github.com/remote-android/redroid-doc) 需要调整内核参数
- WSA (Windows Subsystem for Android)，与 scrcpy 配合有点问题，窗口有黑边。
- VMware、VirtualBox等虚拟化平台，需要解决虚拟显卡。
2. 使用 [scrcpy-mobile](https://github.com/wsvn53/scrcpy-mobile) 远程控制安卓环境, 当然 scrcpy 也支持 Windows、Linux、macOS

## PCT 安卓容器
由于已有PVE环境，这里选用PCT，主要步骤
1. 根据 [PCT-patches](https://github.com/lurenJBD/PCT-patches) 文档，给 PCT 打好补丁
2. 根据 [lineageOS 模板](https://github.com/lurenJBD/PCT-patches/releases/download/lineage/lineage19.1-x86_64-houdini-magisk-gapps.tar.gz)，新建安卓容器，注意去除Unprivileged container的勾选。
3. 修改 lxc.init.cmd 选项，在后面增加以下参数，调整分辨率和iPad一致。
    ```
    androidboot.redroid_width=1668 androidboot.redroid_height=2388 androidboot.redroid_fps=60
    ```

ps: 安卓容器对宿主机性能似乎有一定要求，J4125 只是勉强够用，流畅度一般。

## macOS 中使用 scrcpy
安装 [scrcpy](https://github.com/Genymobile/scrcpy) ，连接命令
```
scrcpy --audio-codec=aac \
  --video-codec=h264 \
  --video-bit-rate=16M \
  --max-fps=60 \
  --tcpip=192.168.10.181:5555 \
  --start-app=io.legado.app.release
```

参数解释
* `--audio-codec=aac`	同步声音，使用 AAC 编码，默认参数可能导致没有声音
* `--video-codec=h264`	使用 H.264 视频压缩编码
* `--video-bit-rate=16M`	16Mbps 码率，高画质
* `--max-fps=60`	最大帧率 60FPS，画面流畅
* `--tcpip=192.168.10.181:5555`	Wi-Fi adb 连接设备
* `--start-app=io.legado.app.release` （可选）连接后直接启动 Legado App，应用列表可使用`adb shell pm list packages -3`查看

## iOS 中使用 scrcpy-mobile
appstore中安装 [scrcpy-mobile](https://apps.apple.com/cn/app/scrcpy-remote/id1629352527)

由于该应用的用户界面易用性比较差，表单也不支持有些 scrcpy 参数，这里直接使用`快捷指令`打开应用。
设置打开 scrcpy-mobile 后，开启`引导式访问`，防止误触。同时可以在 iOS 设置中开启引导式访问的`面容id`，防止频繁输入密码。

![](https://image.ponder.work/mweb/2025-04-27---17457324901465.jpg)

scrcpy-mobile 的 url schema
```
scrcpy2://192.168.10.181:5555?enable-audio=true&audio-codec=aac&video-bit-rate=16M&video-codec=h264&max-fps=60
```

最后，这也未尝不算一种 NTR
![IMG_202504275684_512x682](https://image.ponder.work/mweb/2025-04-27---IMG_202504275684_512x682.jpg)

## 安卓环境设置（可选）
1. 关闭导航栏：系统 > 手势 > 系统导航 > 手势导航
2. 加快或者关闭系统动画：开发者选项 > 窗口动画缩放、过渡动画缩放、Animator 时长比例 > 关闭或者0.5x