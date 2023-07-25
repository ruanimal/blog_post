title: HomeBrew 与无 root 权限 Linux 环境包管理
date: 2023-05-28 8:00 PM
categories: 编程
tags: [Linux,]

---

一些公用的 Linux 服务器，处于维护以及安全考虑，一般只会提供普通权限用户给使用者。
普通用户的权限满足日常使用是够了，但是难以配置自己的开发环境，安装一些自己需要的包。

如果都从源码编译安装软件，依赖的维护过于复杂，初始编译工具链的版本可能也不满足需求，如 gcc 版本过低。
如果申请 sudo 权限或者请求更新系统或安装 docker，后期责任难以界定，运维和管理员一般也不会同意。

所以，最优方案还是有需求的用户在个人目录维护自己的工具链和环境。下文方案为围绕 HomeBrew 构建。
<!--more-->

## 安装 miniconda 解决前置依赖
如果你的系统比较新，可以直接尝试`安装 HomeBrew`。

基于上面讨论的内容，公用服务器一般存在系统版本低的问题，是 centos7 或者 centos6 也毫不稀奇，而且如 glibc 等库的版本也非常低。

安装 HomeBrew 有两个强依赖，git 及 curl，而且依赖的版本都比较高，centos7 的版本也不能满足。
另外，由于 Brew 不少软件都需要从源码编译，gcc 和良好的网络环境也不可缺少。

幸好 miniconda 能够解决以上几点问题。miniconda 只是提供 HomeBrew 安装的依赖，后续可以删除。

配置 conda 源（可选）： 新建 `.condarc`，包含以下内容

```
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

下载及安装 miniconda

```shell
# 下载
# 如果服务器的内置证书已过期， 增加 --no-check-certificate 条件跳过证书验证
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && chmod +x Miniconda3-latest-Linux-x86_64.sh

# 安装
./Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
source ~/miniconda3/etc/profile.d/conda.sh

# 安装所需包
conda install -y gcc_linux-64 gxx_linux-64 curl git

# 链接 gcc，等 HomeBrew 安装完成这些链接可以删掉
cd ~/miniconda3/bin/
ln -s x86_64-conda_cos6-linux-gnu-gcc gcc
ln -s x86_64-conda_cos6-linux-gnu-cpp c++
ln -s gcc cc
```

## 配置安装环境变量
这些环境变量也可以配置到 bashrc 等文件，使之永久生效

```shell
# 设置 curl 和 git，可选
export HOMEBREW_CURL_PATH=~/miniconda3/bin/curl
export HOMEBREW_GIT_PATH=~/miniconda3/bin/git

# 设置安装源为清华源，如果网络畅通可忽略，清华源也可能403
export HOMEBREW_INSTALL_FROM_API=1
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"

```

## 安装 HomeBrew
由于没有 root 权限，HomeBrew 需要手动安装。
由于是手动安装，位置与默认安装位置不同，很多预编译的包就不能用了，都得从源码编译，所以网络和机器性能以及耐心很重要。

```shell
# 下载，也可使用清华源 https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git
git clone https://github.com/Homebrew/brew ~/.homebrew

# 安装
eval "$(~/.homebrew/bin/brew shellenv)"
brew update --force --quiet
chmod -R go-w "$(brew --prefix)/share/zsh"

# 自动加载 brew
echo 'eval "$(~/.homebrew/bin/brew shellenv)"' >> ~/.bashrc
```

## 参考
- https://docs.brew.sh/Installation
- https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
- https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/
- https://github.com/tuna/issues/issues/1353
 