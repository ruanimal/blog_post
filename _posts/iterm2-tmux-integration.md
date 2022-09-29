title: 使用 iTerm2 管理 Tmux 会话
date: 2021-08-02 20:00:00
categories: 编程
tags: [tmux, ]

----

Tmux 是一个终端复用器（terminal multiplexer），非常有用，属于常用的开发工具。

Tmux 可以维持和管理我们的远程终端会话，和服务断线重连后也不会丢失工作状态, 同时可以在一个终端连接中开启多个窗口（window）和窗格（pane）。

一个典型的例子就是，SSH 登录远程计算机，打开一个远程窗口执行命令。这时，网络突然断线，再次登录的时候，是找不回上一次执行的命令的。因为上一次 SSH 会话已经终止了，里面的进程也随之消失了。
<!--more-->
比如，下面就包含了2个窗口和3个窗格
![](http://image.runjf.com/mweb/2021-08-03-16279763351692.jpg)

具体 Tmux 的细节和使用可以参考 [阮一峰的文章](https://www.ruanyifeng.com/blog/2019/10/tmux.html)

但是 Tmux 也存在以下几个问题（个人观点）
1. 窗口和会话管理默认是全键盘操作，需要记比较多快捷键
2. 由于窗口是 Tmux 虚拟的, 不支持文本回滚（scrollback），文本复制不完美
3. 在 mouse mode 下，无法复制文本，非 mouse mode，调整窗格比较麻烦
4. 不支持rzsz

而 iTerm2 内置了 Tmux 绑定功能，可以将 tmux 的窗口和窗格映射成原生的窗口和窗格，可以用 iTerm2 的菜单和快捷键来操作窗口，解决了前3点问题。

至于第4点，rzsz 由于 tmux 的实现机制决定了是无解的。
然而 [lonnywong](https://github.com/lonnywong) 实现了替代方案 [trzsz](https://github.com/trzsz/trzsz) ，**完美解决了文件上传下载的问题**，亲测非常好用。

## iTerm2 配置
可以对 tmux 窗口的映射进行一些定制

iTerm2 对于 tmux 会话有一个profile，建议对终端颜色和外观进行一些定制化，将原生窗口和 tmux 窗口区分开来。

![](http://image.runjf.com/mweb/2021-08-03-16279767130639.jpg)
![](http://image.runjf.com/mweb/2021-08-03-16279767560503.jpg)

## 使用
对于终端机器的 Tmux 版本有要求，需要支持`-CC`命令

**具体方法**
* 新建tmux会话: `tmux -CC`
* 断开重连(attach): `tmux -CC attach`
* 如已存在会话则连接，否则新建会话：`tmux -CC new -A -s main`
* 如果是ssh连接的机器: `ssh -t user@host 'tmux -CC new -A -s main'`
* 断开连接(dettach): 在连接的窗口按 esc，或者直接关掉连接的 tab 吧
* 关掉 session(destroy): 关闭当前 session 的所有 tab 即可

还可以使用 iTerm 的 tmux dashboard 来管理多个会话。

![](http://image.runjf.com/mweb/2021-08-03-16279791270158.jpg)

![](http://image.runjf.com/mweb/2021-08-03-16279791503013.jpg)

![](http://image.runjf.com/mweb/2021-08-03-16279775548246.jpg)

## 其他
- tmux静态编译版本 https://github.com/mjakob-gh/build-static-tmux/releases
- tmux显示颜色 `set -g default-terminal "screen-256color" >> ~/.tmux.conf`

## 参考
- https://www.ruanyifeng.com/blog/2019/10/tmux.html
- https://www.v2ex.com/t/589453
- https://iterm2.com/documentation-tmux-integration.html
- https://gitlab.com/gnachman/iterm2/-/wikis/tmux-Integration-Best-Practices