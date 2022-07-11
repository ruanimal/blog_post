title: 游戏内进程优雅退出
date: 2022-07-10 9:48 PM
categories: 编程
tags: [Docker, Linux]

--- 

在使用 docker 时，常常会碰到进程退出时资源清理的问题，比如保证当前请求处理完成，再退出程序。

当执行 `docker stop xxx` 时，docker会向主进程（pid=1）发送 `SIGTERM` 信号
如果在一定时间(默认为10s)内进程没有退出，会进一步发送 `SIGKILL` 直接杀死程序，该信号既不能被捕捉也不能被忽略。

一般的web框架或者rpc框架都集成了 `SIGTERM` 信号处理程序， 一般不用担心优雅退出的问题。
但是如果你的容器内有多个程序（称为胖容器，一般不推荐），那么就需要做一些操作保证所有程序优雅退出。
<!--more-->
## signals
信号是一种进程间通信机制，它给应用程序提供一种异步的软件中断，使应用程序有机会接受其他程序活终端发送的命令(即信号)。

应用程序收到信号后，有三种处理方式：忽略，默认，或捕捉。

常见信号：

| 信号名称    | 信号数 | 描述                                                                            | 默认操作           |
|---------|-----|-------------------------------------------------------------------------------|:---------------|
| SIGHUP  | 1   | 当用户退出Linux登录时，前台进程组和后台有对终端输出的进程将会收到SIGHUP信号。对于与终端脱离关系的守护进程，这个信号用于通知它重新读取配置文件。 | 终止进程           |
| SIGINT  | 2   | 程序终止(interrupt)信号，在用户键入 Ctrl+C 时发出。                                           | 终止进程           |
| SIGQUIT | 3   | 和SIGINT类似，但由QUIT字符(通常是Ctrl /)来控制。                                             | 终止进程并dump core |
| SIGFPE  | 8   | 在发生致命的算术运算错误时发出。不仅包括浮点运算错误，还包括溢出及除数为0等其它所有的算术错误。                              | 终止进程并dump core |
| SIGKILL | 9   | 用来立即结束程序的运行。本信号不能被阻塞，处理和忽略。                                                   | 终止进程           |
| SIGALRM | 14  | 时钟定时信号，计算的是实际的时间或时钟时间。alarm 函数使用该信号。                                          | 终止进程           |
| SIGTERM | 15  | 通常用来要求程序自己正常退出；kill 命令缺省产生这个信号。                                               | 终止进程           |


## Dockerfile
以是supervisor为例，Dockerfile 如下

```Dockerfile
FROM centos:centos7
ENV PYTHONUNBUFFERED=1 TZ=Asia/Shanghai
RUN yum -y install epel-release && \
    yum -y install supervisor && \
    yum -y clean all  && rm -rf /var/cache

COPY ./ /root/
ENTRYPOINT [ "/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf" ]
```

## trap
正常情况，容器退出时supervisor启动的其他程序并不会收到 `SIGTERM` 信号，导致子程序直接退出了。

这里使用 `trap` 对程序的异常处理进行包装
```bash
trap <siginal handler> <signal 1> <signal 2> ...
```

新建一个初始化脚本，`init.sh`
```bash
#!/bin/sh

/usr/bin/supervisord -n -c /etc/supervisord.conf &

trap "supervisorctl stop all && sleep 3" TERM INT

wait
```

修改 ENTRYPOINT 为如下
```
ENTRYPOINT ["sh", "/root/init.sh"]
```

## 参考
- https://www.ctl.io/developers/blog/post/gracefully-stopping-docker-containers/
- https://www.cnblogs.com/taobataoma/archive/2007/08/30/875743.html
- https://wangchujiang.com/linux-command/c/trap.html