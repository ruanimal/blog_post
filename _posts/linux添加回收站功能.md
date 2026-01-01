---
title: linux添加回收站功能
date: 2016-06-12 21:48:00
updated: 2021-03-25 21:41:32
categories: 编程
tags: [Linux,]

---
## 背景
在linux服务器上工作，常常和`rm`打交道，难免手滑删除了重要的东西。而且linux又没有回收站功能，一旦删错东西真是欲哭无泪。别问我为什么知道，说多了都是泪。
**主要思路是用`mv`命令代替`rm`，将要删除的东西移动到回收站目录。**

## 方案
### 新建删除到回收站脚本
`mkdir ~/bin`

`vim ~/bin/trash`  # 将下面的内容写入
```bash
mv -v $@ ${trash_bin}
```
`chmod +x ~/bin/trash`   # 增加执行权限

### 登录时初始化回收站
```bash
# 将以下内容追加到"~/.bashrc"中，回收站是以每天的日期新建文件夹

today=$(date "+%Y%m%d")  # 形如20160606格式的日期

trash_bin="/tmp/trash/${today}"

if [ ! -d "/tmp/trash" ]; then
    mkdir "/tmp/trash"
fi

if [ ! -d ${trash_bin} ]; then
    mkdir ${trash_bin}
fi

export trash_bin   # 加入环境变量

alias rm="~/bin/trash"
```
