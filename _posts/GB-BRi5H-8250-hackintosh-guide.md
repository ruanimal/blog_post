title: 技嘉GB-BRi5H-8250黑苹果安装指南
date: 2020-07-24 8:17 PM
categories: 工作生活
tags: [mac, Hackintosh, 电子产品]

----

## 硬件信息
### GB-BRi5H-8250 准系统
![](http://image.runjf.com/mweb/2020-07-25-15955608894288.png)
<!--more-->
![](http://image.runjf.com/mweb/2020-07-25-15955609109238.png)
![](http://image.runjf.com/mweb/2020-07-25-15955609232489.png)

| 硬件 | 规格 |
| --- | --- |
| 尺寸 | 4‎6.8 mm x 112.6 mm x 119.4 mm (1.84" x 4.43" x 4.7") |
| 中央处理器 | Intel® Core™ 四核 i5-8250U 3.4GHz|
| 内存 | 内建2组SO-DIMM DDR4插槽 2400MHz 最高支持 64GB|
| 有线网络 | 内建千兆网卡 (Intel i219V) |
| 无线网卡 | 可扩展Intel® Dual Band Wireless-AC 3168 |
| 图形处理器 | Intel® UHD Graphics 620 |
| 音频 | Realtek ALC255 |
| HDMI视频输出 | HDMI2.0a ws HDCP 2.2 4096 x 2304 @ 60Hz  |
| MiniDP视频输出 | DP1.2a ws HDCP 2.2 4096 x 2304 @ 60Hz |
| 扩展槽 | 内建1组M.2 SSD (2280) 插槽 PCIe X4 /SATA 支持Intel傲腾内存<br/>1x PCIe M.2 NGFF 2230 A-E key slot 支持 WiFi+BT card|
| 存储 | 支持 2.5 英寸 HDD/SSD, 7.0/9.5 mm (6 Gbps SATA3) |

### 其他配件
- 内存：SEIWHALE 枭鲸笔记本内存条 DDR4 16G
- 硬盘：Samsung 850 EVO M.2 SATA 250G
- 无线网卡：DW1820A (08PKF4)

## 总体成果
OpenCore配置文件我放到github了 https://github.com/ruanima/GB-BRi5H-8250-hackintosh

### 正常工作项目
- CPU，变频
- 显卡，硬件加速
- HDMI输出，MiniDP输出，HDMI音频，双屏
- 蓝牙
- WiFi
- Handoff, Airdrop
- iMessage, iCloud, Photos, Mac App Store
- USB
- 音频接口，mic
- 苹果电源管理
- 睡眠，关机，唤醒

### 不正常工作项目
- 系统偏好设置-节能（错误识别为有电池）
    ![](http://image.runjf.com/mweb/2020-07-25-15956404046858.jpg)
- HDMI睡眠唤醒，有时屏幕黑屏，需要按一下屏幕开关；DP睡眠正常 (添加启动参数`igfxonln=1`应该可以解决)
- 显示器喇叭开机时不正常，拔插接口后或者开关屏幕电源后正常。(添加启动参数`igfxonln=1`应该可以解决)

## 安装教程
安装过程大部分参考[dortania](https://dortania.github.io/OpenCore-Install-Guide/)，这里采用的是双系统安装方法。

先安装Windows10, 然后在Windows10下配置OpenCore，制作macOS安装镜像。

### 准备工作
预先下载的工具软件
- [微PE工具箱V2.1](http://www.wepe.com.cn/download.html)：Windows系统安装工具
- [Windows10镜像](https://www.microsoft.com/zh-cn/software-download/windows10ISO/)
- [Hackintool](http://www.pc6.com/mac/691696.html): 黑苹果多功能工具
- [Python](https://www.python.org/downloads/): ProperTree等软件的依赖
- [DiskGenius](https://www.diskgenius.cn/download.php): 磁盘分区
- [bootice](https://bootice.softonic.cn/?ex=MOB-615.2): uefi引导编辑
- [ProperTree](https://github.com/corpnewt/ProperTree): 编辑OpenCore配置
- [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS)：用于生成苹果设备序列号信息
- [OpenCorePkg](https://github.com/acidanthera/OpenCorePkg/releases): OpenCore引导文件，注意下载release版本
- ~~[gibMacOS](https://github.com/corpnewt/gibMacOS): 下载，制作macOS安装镜像~~
- [speccy](https://www.ccleaner.com/speccy/download): 查看电脑硬件信息

其他
- 能正常访问Google的网络
- 另外一台电脑，用于查资料（可选）
- U盘1-2个

前置知识
- [技术术语了解](https://dortania.github.io/OpenCore-Install-Guide/terminology.html)

### Windows安装和分区
1. 制作Windows安装U盘
2. 开机安装Delete键进入bios，选择从U盘启动
3. 安装Windows系统，具体安装过程可以参考[这个教程](https://zhuanlan.zhihu.com/p/49181786)，注意安装时不要Windows分区不要占用所有空间，建议50G就好了。
4. 安装完成后，新建一个分区，后续作为macOS的安装分区，建议预留100G以上

### macOS安装U盘制作
#### macOS准备
具体步骤参考[这个](https://dortania.github.io/OpenCore-Install-Guide/installer-guide/winblows-install.html#downloading-macos)，gibMacOS已被官方教程废弃
~~1. 使用gibMacOS的gibMacOS.bat，下载最新macOS~~
~~2. 使用gibMacOS的MakeInstall.bat，制作安装U盘~~

#### OpenCore文件准备
1. 将下载的OpenCorePkg解压，复制EFI文件夹到U盘
2. 删除EFI文件夹中多余的文件，只保留以下内容
    ![](http://image.runjf.com/mweb/2020-07-25-15955829462860.png)
3. 添加必要的.efi驱动到U盘EFI/OC/Drivers文件夹，不同的机型需要的有所区别
    - [HfsPlus.efi](https://github.com/acidanthera/OcBinaryData/blob/master/Drivers/HfsPlus.efi): 用于读写苹果HFS分区

#### Kexts驱动准备
添加必要的Kexts驱动到U盘EFI/OC/Kexts文件夹，不同的机型需要的有所区别
- [VirtualSMC](https://github.com/acidanthera/VirtualSMC/releases)：将电脑伪装成苹果设备
- SMCProcessor.kext: VirtualSMC附带驱动，用于监控cpu状态
- SMCSuperIO：VirtualSMC附带驱动，用于监控风扇状态
- [Lilu](https://github.com/acidanthera/Lilu/releases): 用于加载音频等驱动
- [WhateverGreen](https://github.com/acidanthera/WhateverGreen/releases)：显卡驱动
- [AppleALC](https://github.com/acidanthera/AppleALC/releases): 声卡驱动
- [IntelMausi](https://github.com/acidanthera/IntelMausi/releases): 有线网卡驱动

#### SSDT准备
添加必要的Kexts驱动到U盘EFI/OC/ACPI文件夹，不同的机型需要的有所区别

![-w828](http://image.runjf.com/mweb/2020-07-25-15955842564825.jpg)

从opencore的[文档](https://dortania.github.io/OpenCore-Install-Guide/ktext.html#desktop)可以看出，我们至少需要以下几个SSDT
- [SSDT-PLUG](https://dortania.github.io/Getting-Started-With-ACPI/Universal/plug.html)：电源管理相关，影响睡眠
- [SSDT-EC-USBX](https://dortania.github.io/Getting-Started-With-ACPI/Universal/ec-fix.html)：内置控制器，和USB相关，影响睡眠
- [SSDT-PMC](https://dortania.github.io/Getting-Started-With-ACPI/Universal/nvram.html)：NVRAM相关
- [SSDT-AWAC](https://dortania.github.io/Getting-Started-With-ACPI/Universal/awac.html)：系统时钟（通过查看DSDT，我们并不需要这个）

为了更完美，我们还需要以下SSDT，这些可以等macOS安装完之后，根据情况再考虑是否制作
- [SSDT-SBUS-MCHC](https://dortania.github.io/Getting-Started-With-ACPI/Universal/smbus.html)：SMBus相关
- [SSDT-RHUB](https://dortania.github.io/Getting-Started-With-ACPI/Universal/rhub.html)：USB相关
- [SSDT-HPET](https://dortania.github.io/Getting-Started-With-ACPI/Universal/irq.html)：IRQ Conflicts相关

具体SSDT的制作过程比较繁琐，详细过程参考[文档](https://dortania.github.io/Getting-Started-With-ACPI/)

#### OpenCore配置文件准备
1. 复制OpenCorePKG的Docs/Sample.plist到U盘EFI/OC/config.plist
2. 打开ProperTree的ProperTree.bat脚本，打开前面的config.plist，选择OC Clean Snapshot, 根据我们的驱动文件自动修改配置，保存。
    ![-w355](http://image.runjf.com/mweb/2020-07-25-15955861876823.jpg)
3. 配置文件各项微调，参考[文档](https://dortania.github.io/OpenCore-Install-Guide/config.plist/coffee-lake.html)，注意DeviceProperties，PlatformInfo配置项，影响比较大。
4. 配置准确性校验 https://opencore.slowgeek.com/

**注意**：配置文件中kext的顺序是有影响的，建议前两个是lilu和virtualsmc

### Bios设置
如果bios没有相关设置项，可以跳过

#### 禁用项
* Fast Boot
* Secure Boot
* VT-d (can be enabled if you set `DisableIoMapper` to YES)
* CSM
* Thunderbolt(For initial install, as Thunderbolt can cause issues if not setup correctly)
* Intel SGX
* Intel Platform Trust
* CFG Lock

#### 启用项
* VT-x
* Above 4G decoding
* Hyper-Threading
* Execute Disable Bit
* EHCI/XHCI Hand-off
* OS type: Windows 8.1/10 UEFI Mode
* DVMT Pre-Allocated(iGPU Memory): 64MB
* SATA Mode: AHCI

### macOS安装
**注意**：这时我们先不要替换无线网卡为DW1820A，可能会导致系统安装失败或者卡死。

1. 重启电脑，从macOS安装U盘启动
2. 从OpenCore启动菜单选择macOS安装启动项
3. 等待macOS系统加载完成，选择我们预留的分区，格式为APFS, 安装系统
4. 等待多次重启之后，macOS系统初步安装完成

### 驱动安装及优化
#### 显卡驱动优化
如果只使用免驱的独立显卡，可以跳过这一步
前面配置macOS安装U盘时，其实已经对显卡做了简单驱动，如果一切功能正常，也可以跳过这一步。

显卡驱动不正常会影响双屏显示，睡眠假死，睡眠变重启，HDMI音频输出等

内置显卡的驱动，注意做的是以下几个点
- 选择合适的缓冲帧`AAPL,ig-platform-id`，必要时仿冒设备id`device-id`
- 定制正确的显示输出接口，将物理接口和PCI设备正确对应
- 显存，HDMI相关补丁

这一步使用hackintool的应用补丁功能可以完成，详细步骤参考[这个](https://blog.daliansky.net/Tutorial-Using-Hackintool-to-open-the-correct-pose-of-the-8th-generation-core-display-HDMI-or-DVI-output.html)

**注意**：hackintool在配置过程中，有时改动会被重置，应用补丁时注意二次确认

#### 声卡驱动
声卡驱动大部分工作由AppleALC自动完成，我们需要的是选择正确的layout-id.
建议先去github的release日志上查看，是否在某次release添加了你主板的layout-id。如果没有相关记录，那就只能尝试wiki中对应声卡型号的所有可能的layout-id

详细步骤参考[这个](https://dortania.github.io/OpenCore-Post-Install/universal/audio.html)

#### USB定制
USB定制直接影响睡眠是否正常

使用hackintool完成USB定制，主要过程
1. SSDT-EC-USBX定制（前面已经完成）
2. 加载USBInjectAll.kext驱动，重启，注入所有接口。
3. 分别使用USB2.0，USB3.0，Type-C设备拔插所有USB接口，找到物理接口和PCI设备的映射关系，并删除没有用到的USB接口。
4. 生成USBPorts.kext驱动，加载。

详细步骤参考[这个](https://blog.daliansky.net/Intel-FB-Patcher-tutorial-and-insertion-pose.html#%E5%AE%9A%E5%88%B6usb)

#### DW1820A无线网卡
无线网卡驱动和系统序列号影响iMessage, sidecar等Apple服务使用。

1. 找到无线的PCI设备地址
    ![](http://image.runjf.com/mweb/2020-07-25-15956404767924.jpg)
2. 在config.plist中`DeviceProperties->Add`配置项下加入设备信息, 注意替换PCI设备地址
    ```xml
			<key>PciRoot(0x0)/Pci(0x1C,0x5)/Pci(0x0,0x0)</key>
			<dict>
				<key>AAPL,slot-name</key>
				<string>WLAN</string>
				<key>compatible</key>
				<string>pci14e4,43a3</string>
				<key>device_type</key>
				<string>Airport Extreme</string>
				<key>model</key>
				<string>DW1820A (BCM4350) 802.11ac Wireless</string>
				<key>name</key>
				<string>Airport</string>
				<key>pci-aspm-default</key>
				<integer>0</integer>
			</dict>
    ```
3. 加入Airport驱动[AirportBrcmFixup.kext](https://github.com/acidanthera/airportbrcmfixup/releases), 加入[蓝牙驱动](http://7.daliansky.net/DW1820A/DW1820A_BT_for_Mojave_v2.5.3.zip)
4. 在config.plist的boot-args项中加入`brcmfx-country=#a`
5. 关机替换网卡为DW1820A（有的机器可能需要屏蔽针脚）

详细步骤参考[这个](https://blog.daliansky.net/DW1820A_BCM94350ZAE-driver-inserts-the-correct-posture.html)和[这个](https://osxlatitude.com/forums/topic/11322-broadcom-bcm4350-cards-under-high-sierramojavecatalina/?tab=comments#comment-89830)

#### 电源管理
这一步是为了启动苹果内置电源管理，影响睡眠

详细步骤参考[这个](https://dortania.github.io/OpenCore-Post-Install/universal/pm.html#enabling-x86platformplugin)

#### CPU变频
使CPU的变频挡位更多，台式机不是特别必要。

可以使用`CPU-S`软件来查看变频状态

详细步骤参考[这个](https://dortania.github.io/OpenCore-Post-Install/universal/pm.html#using-cpu-friend)

#### 睡眠修复
如果上面的SSDT和驱动都做好了，睡眠的问题基本不大了，可能要设置下系统参数，禁止休眠到硬盘。

详细步骤参考[这个](https://dortania.github.io/OpenCore-Post-Install/universal/sleep.html)

#### 启动项，图形化界面
到此黑苹果配置基本完成了，我们可以去除`boot-args`中的`-v`等debug启动参数，添加相关声音和图片资源，配置config.plist启动OpenCore图形界面。（在开机中启用声音，个人觉得不太不要）

详细步骤参考[这个](https://dortania.github.io/OpenCore-Post-Install/cosmetic/gui.html#setting-up-opencore-s-gui)

### 将OpenCore迁移到硬盘
上面的OpenCore的各种配置都是在U盘上完成的，当配置完成没啥问题之后，我们就可以把OpenCore的文件迁移到硬盘了。
这样就不需要每次都从U盘启动了，并且开启会默认进入macOS

1. 在pe系统下，使用DiskGenius挂载硬盘ESP分区（右键ESP分区-指派新的驱动器号）
	![-w1059](http://image.runjf.com/mweb/2020-09-19-16004770939670.jpg)
2. 复制U盘的EFI文件夹到ESP分区根目录，和原有的文件夹合并
3. 使用bootice，添加硬盘ESP分区的`\EFI\BOOT\BOOTx64.efi`文件到启动条目，并上移到第一位
![-w446](http://image.runjf.com/mweb/2020-09-19-16004775381948.jpg)
![-w548](http://image.runjf.com/mweb/2020-09-19-16004776841057.jpg)


### 其他注意事项
- 每个SSDT基本都可以用手动修改和自动修改，如果某种方法不生效建议尝试另外一种。
- 如果不是配置完全一样，不要直接使用别人的EFI文件
- FakePCIID相关驱动会改动PCI设备信息，可能导致USB设备地址变化，导致USB定制失效，需要重新定制
- 不同的SMBios机型会影响驱动成功率
- 修改序列号会影响iCloud账户识别

## 感谢
- https://dortania.github.io
- https://github.com/acidanthera
- https://blog.daliansky.net
- https://blog.skk.moe/post/hackintosh-fix-magenta-screen/
