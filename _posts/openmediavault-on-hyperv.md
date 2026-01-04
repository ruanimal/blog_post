---
title: Hyper-V 中安装 openmediavault(OMV) 实现完美 NAS 文件共享
date: 2021-09-21 17:00:00
updated: 2021-09-21 21:15:00
categories: 工作生活
tags: [Hyper-V, NAS]
---

一直在寻找适合自己的 NAS 存储方案，也做过一些尝试，可总有些不完美的点。

最近终于找到一个接近完美的方案：`Hyper-V + NFS + openmediavault`

<!--more-->

## 思路
我对 NAS 几点硬性要求
1. 能支持 NTFS 文件系统，否则现有数据迁移成本很高
2. 文件共享必须支持回收站，否则数据易丢失
3. 文件检索要方便

所以之前一直用 windows 作为 NAS 系统，最大的问题是不支持共享文件夹的回收站。

现有 NAS 方案的对比

|                              | good              | bad                         |
| ---------------------------- | ----------------- | --------------------------- |
| windows smb                  | 性能                | 无法扩展功能（如smb回收站，timemachine） |
| wsl1 samba                   | 性能略低于smb，功能可扩展    | 部分共享文件无法打开,  配置略繁琐          |
| wsl2 samba（omv）              | 功能可扩展             | 无法解决桥接网络，需要更好的cpu        |
| nfs                          | 性能最强              | 无法扩展功能                      |
| 群晖 / OMV / FreeNAS           | 功能多，功能可扩展         | 无法管理底层文件                    |
| windows + nfs + vmware(群晖)   | 可管理底层文件，功能可扩展     | 物理机休眠虚拟机无法唤醒                |
| windows + nfs + hyper-v(omv） | 功能可扩展，性能接近smb，可休眠 | 需要更好的cpu，hyperv使用略繁琐        |

本方案的思路受之前文章的启发 [在WSL2中安装openmediavault(OMV)](/2021/01/02/install-openmediavault-in-WSL2/)

WSL2 的便利之处在于让 linux 系统能以一个足够快的速度访问 windows 文件，据了解是使用 9p(Plan 9 9p remote filesystem protocol) 协议进行文件共享。

那么我们只要在 Hyper-V 上运行虚拟机，并通过某种方式（这里选择NFS）共享文件到虚拟机里，就能绕开 WSL2 的缺点。
实现 NAS 的底层文件系统由 windows 管理， 上层文件共享等应用由虚拟机中的 NAS 系统处理，兼顾了稳定性和扩展性。

## 方案
软件环境选择
- windows 10 21H1
- haneWIN NFS server 1.2.59
- openmediavault

### Windows 10 安装及配置
1. 设置开机自动登录用户（可选）: https://zhuanlan.zhihu.com/p/61262940
2. 禁止自动从睡眠中唤醒（可选）: 控制面板 -> 电源选项 -> 更改计划设置 -> 更改高级计划设置 -> 睡眠 -> 允许使用睡眠唤醒定时器（禁用）
3. 启用 Hyper-V：`DISM /Online /Enable-Feature /All /FeatureName:Microsoft-Hyper-V`
4. Hyper-V 配置桥接网络：虚拟交换机管理器 -> 新建虚拟网络交换机(外部)
5. 安装 haneWIN NFS server 并配置需要共享的硬盘

### openmediavault 安装及配置
1. 创建 Hyper-V 虚拟机：选择第一代，选择桥接网卡，虚拟硬盘需挂载到 IDE 控制器
2. 挂载安装镜像，安装 openmediavault 系统
3. 安装 omv-extras
	```
	wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash
	```
4. 安装插件：openmediavault-sharerootfs(共享系统分区的文件夹) openmediavault-remotemount(远程挂载)
5. 挂载 NFS 共享：存储器 -> 远程挂载
6. 建立共享文件夹: 选择系统分区上的 NFS 挂载文件夹
7. 启用smb共享
8. 关闭虚拟机，并配置虚拟机的网卡为静态MAC地址（如果是导入的虚拟机，注意检查MAC地址是否合法）

![-w610](https://image.ponder.work/mweb/2021-09-21-16322275739423.jpg)
![-w524](https://image.ponder.work/mweb/2021-09-21-16322277511161.jpg)

### 其他优化配置
#### samba 性能优化
配置页面：服务 -> SMB/CIFS -> 设置 -> 高级设置 -> 扩展选项

```
veto files = /.Trashes/$RECYCLE.BIN/System Volume Information/.recycle/
socket options = TCP_NODELAY IPTOS_LOWDELAY SO_KEEPALIVE SO_RCVBUF=98304 SO_SNDBUF=98304
dead time = 30
getwd cache = yes
min protocol = SMB2
#max protocol = SMB2
aio read size = 40960
aio write size = 40960
write cache size = 262144
large readwrite = yes
fake oplocks = yes
oplocks = no
```

#### samba 回收站优化
默认的回收站不能按天对文件进行分类，不方便进行清理

配置页面：服务 -> SMB/CIFS -> 共享 -> 共享文件夹
启用回收站选项，并在扩展选项中增加

```
recycle:repository = .recycle/%U/today
```

配置页面：系统 -> 计划任务
增加共享文件夹回收站整理脚本
```bash
#!/bin/bash

set -x -e

BASE=/srv/nfs_root
TODAY=$(date +'%Y%m%d')
USERS=(
    data
)
# read -r -a USERS <<< $(groupmems -g users -l)

cd $BASE
for share in $(ls); do
    for user in ${USERS[@]}; do
        rec="$BASE/${share}/.recycle/$user"
        if [[ ! -d $rec ]]; then
            mkdir -p $rec
        fi
        cd $rec
        if [[ ! -d $TODAY ]]; then
            mkdir $TODAY
        fi
        if [[ -L today || -f today ]]; then
            rm -f today
        elif [[ -d today ]]; then
            mv today $TODAY/$(date +'bak.%s')
        fi
        ln -s ./$TODAY today
    done
done
```

windows 系统中，增加定时任务，删除NFS共享目录中的回收站文件到系统回收站
Python 代码如下，超过一定时间的文件会被送到 windows 回收站

```Python
import time
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path
from send2trash import send2trash

os.chdir(os.path.dirname(__file__))

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(filename)s:%(lineno)d]\t%(message)s',
    level='INFO',
    filename='log/recycle.log',
)

EXPORTS_FILE='D:\\nas_file\\nfsd\\exports'
KEEP_DAYS = 30
USERS = ['data']


def get_size(path: str) -> int:
    return sum(p.stat().st_size for p in Path(path).rglob('*'))

def main():
    exports = []
    for line in open(EXPORTS_FILE):
        parts = line.strip().split()
        if not parts or parts[0].startswith('#'):
            continue
        exports.append(parts[0])

    dt = (datetime.now() - timedelta(days=KEEP_DAYS)).strftime('%Y%m%d')
    for export in exports:
        for user in USERS:
            rec = os.path.join(export, '.recycle', user)
            if os.path.exists(rec):
                for item in os.listdir(rec):
                    path = os.path.join(rec, item)
                    # print(path, get_size(path))
                    if os.path.isdir(path) and item.startswith('2') and item < dt:
                        size = get_size(path)
                        if size <= 0:
                            logging.info('rm empyt\t%s', path)
                            os.rmdir(path)
                        else:
                            logging.info('trash\t%s', path)
                            send2trash(path)

if __name__ == '__main__':
    while True:
        try:
            logging.info('check')
            main()
            time.sleep(3600)
        except Exception as e:
            logging.exception(e)
```

## 其他
也可考虑将上文 openmediavalut 替换成黑群晖系统，牺牲定制化能力的同时大大增加易用性。
当然，你也可以两者双修

## 参考
- https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v
- https://nelsonslog.wordpress.com/2019/06/01/wsl-access-to-linux-files-via-plan-9/

