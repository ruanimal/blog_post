title: Git 常用命令备忘录
date: January 21, 2016 5:03 PM
categories: 编程
tags: 

---

### git 简介
git是一个分散式版本控制软件，最初由林纳斯·托瓦兹（Linus Torvalds）創作，於2005年以GPL釋出。最初目的是为更好地管理Linux内核开发而设计。
初始版本由Linus大神在两个星期内写出来，之后基本一统文件版本控制的天下。

### 名词解释
工作区：就是你在电脑里能看到的目录。
暂存区：英文叫stage, 或index。一般存放在"git目录"下的index文件（.git/index）中，所以我们把暂存区有时也叫作索引（index）。
版本库：工作区有一个隐藏目录.git，这个不算工作区，而是Git的版本库。
branch：分支，相当于不同的平行世界
remote：远程仓库
origin：默认的远程仓库名词
HEAD：一个指向当前版本号的指针

<!--more-->

### 开始项目
`git init`    初始化git仓库
`git clone <repository> [<directory>]`    复制项目
`git config user.name yourname`   设置用户名
`git config user.email youremail`    设置邮箱

### 管理修改
`git status`  查看当前仓库状态，绿色为未commit的stage内容，红色为未stage、为添加到版本库内容
`git show <commit-hash-id|tag_name>`   查看某次commit的修改内容
`git add filename`    保存文件修改到暂存区
`git rm filename`     删除工作区的文件和git记录
`git rm --cached filename`    删除暂存区的新文件
`git diff`    查看工作区和暂存区(stage)的不同
`git diff --cached`   比较的是暂存区和版本库的差别
`git diff HEAD` 可以查看工作区和版本库的差别
`git diff commit1 commit2`    比较不同commit
`git diff commit1 commit2 -- filepath` 比较不同commit指定文件更改
`git commit`  提交暂存区内容到当前分支，会新加一个commit
`git commit  --amend`     追加暂存区内容到当前分支的最近一个commit
`git rebase -i HEAD~4`   合并最近4个commit

### 分支与Tag
`git branch -a`   查看所有分支信息
`git branch new_branch_name`      新建分支
`git branch -d branch_name`      删除分支
`git branch --set-upstream dev origin/dev`   指定本地dev分支与远程origin/dev分支的链接
`git checkout branch_name`      切换到分支头部
`git checkout tags/tag_name`      切换到某个tag对应的版本
`git checkout -b new_branch_name`    新建分支，并切换到新分支
`git checkout -b dev origin/dev`  创建远程origin的dev分支到本地，并切换到新分支
`git merge dev` 合并dev到当前分支，保留commit信息
`git merge --squash dev`  合并dev分枝代码到暂存区，不保留commit信息
`git tag`     查看tag列表
`git tag tag_name`    打tag
`git tag -d tag_name`     删除tag


### 仓库操作
`git remote -v`   查看远程仓库详细信息
`git remote add <name> <url>`     添加远程仓库
`git remote rename <old> <new>`   重命名远程仓库
`git remote remove <name>`    删除远程仓库
`git remote set-url [--push] <name> <newurl>`     设置远程仓库链接
`git remote prune origin`     清除本地无用remote
`git pull`      <远程主机名> <远程分支名>:<本地分支名>    从远程仓库更新
`git fetch git@github.com:ruanima/Mysite.git`    从其他仓库获取代码，但不更新到本地分支
`git push <远程主机名> <本地分支名>:<远程分支名>`    提交到远程仓库
`git push origin <本地分支名>`     将本地分支推送与之存在“追踪关系”的远程分支(通常两者同名)
`git push`    如果当前分支只有一个追踪分支，那么主机名都可以省略。
`git push -f`     强制提交


### 怎么吃后悔药
`git log`     查看commit的历史
`git log -p`      <filename>查看某个文件的修改历史
`git log -p -2`   查看最近2次的更新内容
`git log --graph`     命令可以看到分支合并图。
`git whatchanged filename`    显示文件更改的相关commit
`git checkout [commit id] -- file`      丢弃工作区文件修改，其实是切换文件版本到commit 版本
`git reset HEAD filename`    可以把暂存区的修改撤销掉（unstage），重新放回工作区：
`git reset –mixed`      此为默认方式，不带任何参数的git reset，即时这种方式，它回退到某个版本，只保留源码，回退commit和index信息
`git reset –soft`       回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可
`git reset –hard`       彻底回退到某个版本，本地的源码也会变为上一个版本的内容，若无版本号则回退到最新的版本。
`git reset [commit-id] -- filename`   以commit的版本替换stage的文件
`git revert [commit-id]`      是用一次新的commit来逆向操作之前的commit


### 其他
`git gc`      压缩历史信息来节约磁盘和内存空间
`git <command> --abort`   一般用于中断某次操作

