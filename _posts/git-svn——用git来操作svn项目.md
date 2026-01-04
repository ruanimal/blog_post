---
title: git-svn：通过git来管理svn代码
categories: 编程
date: 2016-09-10 12:00:00
updated: 2016-12-12 19:10:00
tags: [Git, SVN]
---

## 简介
svn和git都是常用的版本管理软件，但是git无论在理念或是功能上都比svn更为先进。但是有的公司是以svn作为中央仓库，这时git与svn代码的同步就可以通过 git-svn这个软件进行，从而用git管理svn代码。最后的效果相当于把svn仓库当作git的一个remote（远程仓库），而你本地的代码都是通过git来管理，只有push到svn时才会把你本地的commit同步到svn。

<!--more-->
## 从svn克隆
首先看一看用于测试的svn项目结构，svn的仓库路径是`file:///d/Projects/svn_repo`，可以用`svnadmin create svn_repo`命令新建。该仓库有2个分支，1个tag，属于svn标准布局。

SVN项目结构：
```
/d/proj1
├── branches
│   ├── a
│   │   └── readme.txt
│   └── b
│       ├── 11.txt
│       └── readme.txt
├── tags
│   └── v1.0
│       ├── 11.txt
│       └── readme.txt
└── trunk
    └── readme.txt
```

命令格式：`git svn clone <svn仓库路径> [本地文件夹名] [其他参数]` 相当于`git clone`
示例： `git svn clone file:///d/Projects/svn_repo proj1_git -s --prefix=svn/`
参数说明：
- `-s` 告诉 Git 该 Subversion 仓库遵循了基本的分支和标签命名法则，也就是标准布局。
如果你的主干(trunk，相当于非分布式版本控制里的master分支，代表开发的主线），分支(branches)或者标签(tags)以不同的方式命名，则应做出相应改变。
`-s`参数其实是`-T trunk -b branches -t tags`的缩写，这些参数告诉git这些文件夹与git分支、tag、master的对应关系。
- `--prefix=svn/` 给svn的所有remote名称增加了一个前缀svn，这样比较统一，而且可以防止`warning: refname 'xxx' is ambiguous.`

现在，看下用git-svn克隆的项目情况（运行git branch -a），此处git的分支情况是与svn文件夹对应的。
```
* master
  remotes/svn/a
  remotes/svn/b
  remotes/svn/tags/v1.0
  remotes/svn/trunk
```

### 只下载指定版本之后的历史
如果svn上的commit次数非常多, git svn clone 就会非常慢，一般超过几百个版本就要大概十分钟。此时可以在clone的时候只下载部分版本，
命令：`git svn clone -r<开始版本号>:<结束版本号> <svn项目地址> [其他参数]`
示例：`git svn clone -r2:HEAD file:///d/Projects/svn_repo proj1_git -s`
说明：其中2为svn版本号，HEAD代表最新版本号，就是只下载svn服务器上版本2到最新的版本的代码.

## 工作流程
简单来说就是，首次新建分支会记录和svn远程对应分支的追踪关系，之后你的所有commit都是在本地的；并且和纯git管理的项目没有区别，只是在`git svn rebase`和`git svn dcommit`的时候才会和svn仓库发生关系
### 一般工作流程（推荐）
1. 新建分支`git checkout -b <本地分支名称> <远程分支名称>`
示例：`git checkout -b a svn/a`
说明：此处新建了一个本地分支a，与svn的a分支对应。
2. 在本地工作，commit到对应分支上
3. `git svn rebase` 从svn上更新代码, 相当于svn的update。
4. `git svn dcommit` 提交你的commit到svn远程仓库，建议提交前都先运行下git svn rebase。

### 在git本地其他分支工作的情况
1. `git chechout -b a svn/a` 此处新建了一个本地分支a，与svn的a分支对应。
2. `git checkout -b feature1` 在a分支的基础上，开一个本地feture1分支
3. 在feture1分支进行开发，有了多次commit
4. 在feture1分支上进行`git svn rebase` 和 `git svn dcommit`，这样feature1的commit也会提交到svn的a分支上。
   需要注意的是要记住feture1是从哪个分支checkout的，它的svn远程分支就与哪个相同。比如此处是a分支，那么svn分支就是svn/a，commit就会提交到svn的a分支。

## SVN分支管理
### 新建分支到svn
命令：`git svn branch <分支名称>`
示例：`git svn branch c_by_git`
说明：在svn仓库上建了了一个c_by_git分支
分支情况
```
  a
* master
  remotes/svn/a
  remotes/svn/b
  remotes/svn/c_by_git
  remotes/svn/tags/v1.0
  remotes/svn/trunk
```
### 删除svn分支
- 删除svn分支目录`svn rm <svn分支路径> -m <commit信息>`
示例：`svn rm file:///d/Projects/svn_repo/branches/c_by_git -m 'rm branch'`
- 删除远程跟踪分支`git branch -D -r <远程分支名称>`
示例：`git branch -D -r svn/c_by_git`


## SVN上tag管理
### 新建tag
命令：`git svn tag <tag名称>`
示例：`git svn tag v1.1`
说明：在svn仓库上建了一个v1.1tag
### 删除tag
1. 删除svn目录`svn rm <svntag路径> -m <commit信息>`
示例：`svn rm file:///d/Projects/svn_repo/tags/v1.1 -m 'rm tag'`

2. 删除远程跟踪分支`git branch -D -r <远程分支名称>`
示例：`git branch -D -r svn/tags/v1.1`
说明：svn的tag和分支在git看来是一样的，所以此处还是用的git branch

## 冲突解决
如果本地和svn都进行了修改，则不能快速前进，git svn rebase 会出现错误。
这时应该按以下步骤操作：

1. 手动修改冲突文件，修改完成后`git add`

2. `git rebase --continue`

3. `git svn dcommit`


## svn不遵循规范的情况
**以上讲的都是svn仓库是标准的情况，如果不标准，则以下几个地方都会有所不同。**主要就是每个步骤基本都要添加svn的具体路径。
先看看，示例项目的结构，仓库路径是`file:///d/Projects/svn_repo2`。这个项目主分支是dev文件夹，branch1和tag1文件夹分别代表的是一个分支和tag。

svn项目结构：
```
/d/proj2
├── branch1
│   └── file1.txt
├── dev
│   └── file1.txt
└── tag1
    └── file1.txt
```

### 从svn克隆
命令：`git svn clone <svn项目地址，要包含具体分支路径> [本地文件夹名]`
示例：`git svn clone file:///d/Projects/svn_repo2/dev proj2_svn`

### 添加远程分支信息
命令：
  1. `git config --add svn-remote.<远程分支名称>.url <svn地址，要包含具体分支路径>`
  2. `git config --add svn-remote.<远程分支名称>.fetch :refs/remotes/<远程分支名称>`

示例：
  1. `git config --add svn-remote.svn/branch1.url file:///d/Projects/svn_repo2/branch1`
  2. `git config --add svn-remote.svn/branch1.fetch :refs/remotes/svn/branch1`

说明：此处的“远程分支名称”可以随意填写，只要这三个保持一致即可。建议都给他们增加`svn/`前缀，这样svn的所有分支显示起来会比较一致，与上面clone时的`--prefix=svn/`类似。

### 新建本地分支，与svn对应
命令：
  1. `git svn fetch <远程分支名称>` 获取svn仓库该分支的代码
  2. `git checkout -b <本地分支名> <远程分支名称>`

示例：
  1. `git svn fetch svn/branch1`
  2. `git checkout -b branch1 svn/branch1`

分支情况：
```
* branch1
  master
  remotes/git-svn
  remotes/svn/branch1
```
