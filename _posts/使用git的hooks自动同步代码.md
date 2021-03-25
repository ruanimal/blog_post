title: 使用git的hooks自动同步代码
date: April 16, 2016 8:01 PM
categories: 编程
tags: [Git,]

----

## 需求
由于最近做Python的linux服务器脚本，经常要同步代码到测试服务器，又不想直接ssh登录到服务器，所以萌生了用git自动同步代码的想法。
具体的要求是：测试机是服务器，需要本地一push代码，测试机能实时更新。
查阅相关资料发现可以用git的hooks来实现。

<!--more-->

## 解决步骤
说明：  
1. 本地项目： git-test  
2. 中转仓库： git-transfer  
3. 目的项目： git-dest  
4. 中转仓库与目的项目都在测试机上

### 初始化中转仓库
```shell
mkdir git-transfer
cd git-transfer
git --bare init
```

### 将中转仓库添加到本地项目的remote
`git remote add transfer ssh://r@192.168.157.129/home/r/git-transfer/`



### 给中转仓库添加hooks
```shell
cd /home/r/git-transfer/hooks/
cp post-update.sample post-update
vi post-update
```

将 post-update 的内容修改为如下
```shell
#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

unset GIT_DIR
DeployPath=/home/r/git-dest

cd $DeployPath
git add . -A && git stash
git pull origin master
```

### 将中转仓库clone到目的项目
`git clone /home/r/git-transfer/ /home/r/git-dest/`

或者
```shell
cd git-dest
git init
git remote add origin /home/r/git-transfer/
```

这样在本地项目一push，目的项目就会马上更新

