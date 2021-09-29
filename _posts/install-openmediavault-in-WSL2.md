title: 在WSL2中安装openmediavault(OMV)
date: 2021-01-02 17:00
categories: 工作生活
tags: [Linux, WSL, NAS]

----

**本方案存在不可解决的缺点，已被笔者放弃，请移步[最新解决方案](/2021/09/21/openmediavault-on-hyperv/)**

NAS的文件系统一直是我比较纠结的一个点。NAS的系统基本上是基于Linux(Unix)，文件系统不是ntfs，数据迁移不方便，数据恢复工具也没那么全。

WSL就完美解决了这个问题，用Linux提供服务，数据最终还是落在ntfs上，而且重要的是everything也能用上。

openmediavault(OMV)是一个基于Debian的NAS系统，而且能在原生Debian系统上自行安装，正好能够实现我们的功能。
<!--more-->

## WSL2 相关准备工作
需要安装WSL2并启用桥接网络，同时安装好Debian系统

参考本人[这篇文章](/2021/01/02/WSL2-bridge-mode/)

## 安装 systemd
由于openmediavault对systemd有强依赖，而WSL的系统默认是由`/init`启动的，会导致安装出错
所以得先把systemd的问题解决。

经过一番google，找到了[systemd-genie](https://github.com/arkane-systems/genie)能够解决问题

### 安装 dotnet 源
systemd-genie 依赖 dotnet-runtime-5.0, 所以把dotnet源配好，参考[文档](https://docs.microsoft.com/zh-cn/dotnet/core/install/linux-debian#debian-10-)

```bash
wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update; \
  sudo apt-get install -y apt-transport-https && \
  sudo apt-get update
```

### 安装 systemd-genie
官网提供了安装脚本, 执行完会配置好systemd-genie源并安装
```bash
curl -s https://packagecloud.io/install/repositories/arkane-systems/wsl-translinux/script.deb.sh | sudo bash
```

但是安装过程中，发现systemd-genie源的访问有些问题，所以只能从gitbub下载安装
```bash
cd /tmp && wget https://github.com/arkane-systems/genie/releases/download/1.30/systemd-genie_1.30_amd64.deb
dpkg -i systemd-genie_1.30_amd64.deb
apt --fix-broken install
```

### 默认启动 systemd-genie
修改`/root/.bashrc`, 添加以下内容
```
if [[ ! -v INSIDE_GENIE ]]; then
    echo "Starting genie"
    exec /usr/bin/genie -s
fi
```

## 网络相关配置
主机名和网口配置重启WSL后可能会失效，建议修改配置文件来实现

### 主机名
修改`/etc/wsl.conf`，增加`hostname = openmediavault`
```
[network]
hostname = openmediavault
generateResolvConf = false
```

修改`/etc/genie.ini`，设置`update-hostname`为false
```
[genie]
secure-path=/lib/systemd:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
unshare=/usr/bin/unshare
update-hostname=false
clone-path=false
clone-env=WSL_DISTRO_NAME,WSL_INTEROP,WSLENV
```

### ip地址
注意，由于WSL的mac地址每次重启都会变，该问题暂时无法解决，参考[issue](https://github.com/microsoft/WSL/issues/5352)
所以这里采用静态IPv4地址和DHCPv6来配置网络地址

新建`/etc/systemd/network/lan.network`，内容如下
```
[Match]
Name=eth0

[Network]
Description=lan
DHCP=ipv6
Address=192.168.123.31/24
Gateway=192.168.123.1
DNS=192.168.123.1
LLDP=true
EmitLLDP=true
```

然后执行执行`systemctl enable systemd-networkd && systemctl start systemd-networkd`

## 安装 openmediavault
参考[官方文档](https://openmediavault.readthedocs.io/en/5.x/installation/on_debian.html)

由于要安装的包比较多，建议先把Debian软件源替换成国内镜像，参考[这个](https://mirrors.tuna.tsinghua.edu.cn/help/debian/)

1. 添加软件源keyring
    ```bash
    apt-get install --yes gnupg
    wget -O "/etc/apt/trusted.gpg.d/openmediavault-archive-keyring.asc" https://packages.openmediavault.org/public/archive.key
    apt-key add "/etc/apt/trusted.gpg.d/openmediavault-archive-keyring.asc"
    ```

2. 添加openmediavault软件源
    ```bash
    cat <<EOF >> /etc/apt/sources.list.d/openmediavault.list
    deb https://packages.openmediavault.org/public usul main
    # deb https://downloads.sourceforge.net/project/openmediavault/packages usul main
    ## Uncomment the following line to add software from the proposed repository.
    # deb https://packages.openmediavault.org/public usul-proposed main
    # deb https://downloads.sourceforge.net/project/openmediavault/packages usul-proposed main
    ## This software is not part of OpenMediaVault, but is offered by third-party
    ## developers as a service to OpenMediaVault users.
    # deb https://packages.openmediavault.org/public usul partner
    # deb https://downloads.sourceforge.net/project/openmediavault/packages usul partner
    EOF
    ```

3. 安装
    ```bash
    export LANG=C.UTF-8
    export DEBIAN_FRONTEND=noninteractive
    export APT_LISTCHANGES_FRONTEND=none
    wget -O "/etc/apt/trusted.gpg.d/openmediavault-archive-keyring.asc" https://packages.openmediavault.org/public/archive.key
    apt-key add "/etc/apt/trusted.gpg.d/openmediavault-archive-keyring.asc"
    apt-get update
    apt-get --yes --auto-remove --show-upgraded \
        --allow-downgrades --allow-change-held-packages \
        --no-install-recommends \
        --option Dpkg::Options::="--force-confdef" \
        --option DPkg::Options::="--force-confold" \
        install openmediavault-keyring openmediavault

    omv-confdbadm populate
    ```

## 安装 omv-extras（可选）
参考[官方文档](https://forum.openmediavault.org/index.php?thread/5549-omv-extras-org-plugin/)
```bash
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash
```

## 配置 openmediavault
### 系统配置
OMV里的主机名和网络配置就配置成和上面配置文件里的一样，防止OMV的服务工作异常

1. 修改主机名，防止WSL默认主机名过长（必须小于15位），导致samba配置失败
    ![2021-01-02_180911](http://image.runjf.com/mweb/2021-01-02-2021-01-02_180911.png)

2. 打开`系统 -> 网络 -> 添加 -> 以太网`，配置网口ip，这里配置为DHCP自动获取
    ![2021-01-02_181342](http://image.runjf.com/mweb/2021-01-02-2021-01-02_181342.png)

3. 打开`系统 -> 常规设置 -> Web管理员密码`，修改管理员密码，默认密码为`admin:openmediavault`

### 共享文件夹配置
由于WSL2读写本机硬盘是使用的微软的驱动，OMV并不支持，默认只能识别到根目录的虚拟硬盘。

又因为WSL2的本地硬盘都挂载在`/mnt/`路径下，所以只要能将`/mnt/`目录共享就ok了

这里参考[openmediavault-sharerootfs](https://github.com/openmediavault/openmediavault/blob/master/deb/openmediavault-sharerootfs/debian/openmediavault-sharerootfs.postinst)的实现

修改`/etc/openmediavault/config.xml`配置文件， 在`fstab`标签下增加`mntent`挂载点配置，修改完如下
```xml
    <!--省略其他部分-->
    <fstab>
      <mntent>
        <uuid>79684322-3eac-11ea-a974-63a080abab18</uuid>
        <fsname>/dev/sdb</fsname>
        <dir>/</dir>
        <type>ext4</type>
        <opts>errors=remount-ro</opts>
        <freq>0</freq>
        <passno>1</passno>
        <hidden>1</hidden>
      </mntent>
    </fstab>
```

打开`访问权限管理 -> 共享文件夹 -> 添加`，添加D盘（/mnt/d）作为共享文件夹，然后在samba服务中就能引用这个共享文件夹了
![2021-01-02_183349](http://image.runjf.com/mweb/2021-01-02-2021-01-02_183349.png)

![2021-01-02_183046](http://image.runjf.com/mweb/2021-01-02-2021-01-02_183046.png)


## 参考
1. https://github.com/arkane-systems/genie
2. https://docs.microsoft.com/zh-cn/dotnet/core/install/linux-debian#debian-10-
3. https://openmediavault.readthedocs.io/en/5.x/installation/on_debian.html
4. https://forum.openmediavault.org/index.php?thread/5549-omv-extras-org-plugin/
5. https://github.com/openmediavault/openmediavault/blob/master/deb/openmediavault-sharerootfs/debian/openmediavault-sharerootfs.postinst
