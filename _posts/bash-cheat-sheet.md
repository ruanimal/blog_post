title: bash 语法备忘
date: 2021-11-28 15:00:00
categories: 编程
tags:  [Shell, ]

---

bash 语法作为程序员好像都了解一些，但又缺少体系化学习，需要使用到某些功能时又经常手忙脚乱地查。
本文主要参考[阮一峰的bash教程](https://wangdoc.com/bash/)，对bash的知识点进行了梳理。
本文目的是作为bash的语法备忘录、语法速查表。
<!--more-->
## 模式扩展
模式扩展（globbing），类似C语言中的宏展开，我们通常使用的通配符`*`就是其中之一。
Bash 一共提供八种扩展。

* `~` 波浪线扩展
* `?` 问号扩展
* `*` 星号扩展
* `[]` 方括号扩展
* `{}` 大括号扩展
* `$var` 变量扩展
* `$(date)` 命令扩展
* `$((1 + 1))` 算术扩展

### 波浪线扩展
波浪线`~`会自动扩展成当前用户的主目录。
`~user`表示扩展成用户`user`的主目录。如果用户不存在，则波浪号扩展不起作用。

```
bash-5.1$ echo ~/projects/
/Users/ruan/projects/

bash-5.1$ echo ~root/.ssh
/var/root/.ssh

bash-5.1$ echo ~aaa/.ssh
~aaa/.ssh
```

### 问号扩展
`?`字符代表文件路径里面的任意单个字符，不包括空字符。
**只有文件确实存在的前提下，才会发生扩展。**

```
bash-5.1$ touch {a,b}.txt ab.txt

bash-5.1$ ls ?.txt
a.txt  b.txt

bash-5.1$ ls ??.txt
ab.txt
```

### 星号扩展
*字符代表文件路径里面的任意数量的任意字符，包括零个字符。

```
bash-5.1$ ls *.txt
a.txt  ab.txt  b.txt

bash-5.1$ ls /usr/local/Cellar/*/*/bin/z*
/usr/local/Cellar/ffmpeg/4.4_2/bin/zmqsend
/usr/local/Cellar/mysql-client/8.0.26/bin/zlib_decompress
/usr/local/Cellar/netpbm/10.86.24/bin/zeisstopnm
/usr/local/Cellar/perl/5.34.0/bin/zipdetails
/usr/local/Cellar/zstd/1.5.0/bin/zstd
```

### 方括号扩展
方括号扩展的形式是`[...]`，只有文件确实存在的前提下才会扩展。

`[^...]`和`[!...]`。它们表示匹配不在方括号里面的字符

方括号扩展有一个简写形式[start-end]，表示匹配一个连续的范围

```
bash-5.1$ ls [ab].txt
a.txt  b.txt

bash-5.1$ ls [^b]b.txt
ab.txt

bash-5.1$ ls [a-b].txt
a.txt  b.txt
```

### 大括号扩展
大括号扩展`{...}`表示分别扩展成大括号里面的所有值
大括号也可以与其他模式联用，并且总是先于其他模式进行扩展。

```
bash-5.1$ echo {1,2,3}
1 2 3

bash-5.1$ echo a{1,2,3}b
a1b a2b a3b

bash-5.1$ echo --exclude={a,b,c}
--exclude=a --exclude=b --exclude=c

bash-5.1$ echo foo{1,2{1,2}0,3}bar
foo1bar foo210bar foo220bar foo3bar

bash-5.1$ echo {1..3}
1 2 3

bash-5.1$ echo {1..10..2}
1 3 5 7 9
```

### 变量扩展
Bash 将美元符号`$`开头的词元视为变量，将其扩展成变量值

```
bash-5.1$ echo $HOME
/Users/ruan
```

### 命令扩展
`$(...)`可以扩展成另一个命令的运行结果，该命令的所有输出都会作为返回值。

```
bash-5.1$ echo $(date)
日 11 28 16:22:09 CST 2021

bash-5.1$ echo `date`
日 11 28 16:22:24 CST 2021
```

### 算术扩展
`$((...))`可以扩展成整数运算的结果

```
bash-5.1$ echo $((1+1))
2
```

## 引号使用
### 单引号
单引号用于保留字符的字面含义，在单引号里转义字符和模式扩展都会失效。

```
bash-5.1$ ls '[ab].txt'
ls: cannot access '[ab].txt': No such file or directory

bash-5.1$ ls '*'
ls: cannot access '*': No such file or directory
```

### 双引号
双引号比单引号宽松，三个特殊字符除外：美元符号（`$`）、反引号（`` ` ``）和反斜杠（`\`）。这三个字符，会被 Bash 自动扩展。

也就是说，相比单引号在双引号中变量扩展，命令扩展，算术扩展以及转义字符是有效的。

```
bash-5.1$ echo "$((1+1))"
2

bash-5.1$ echo "$HOME"
/Users/ruan

bash-5.1$ echo "$(date)"
日 11 28 16:35:27 CST 2021

bash-5.1$ echo -e "1\t2"
1	2
```

### 引号嵌套
```
# 双引号中使用单引号
bash-5.1$ echo '"'
"
bash-5.1$ echo '"${HOME}"'
"${HOME}"
# 单引号中使用双引号
bash-5.1$ echo "'${HOME}'"
'/Users/ruan'
bash-5.1$ echo "'\"${HOME}\"'"
'"/Users/ruan"'

# 引号嵌套中使用模式扩展，将需要扩展的字符放在单引号中；典型的有json变量填充
bash-5.1$ echo '{"user": "'${USER}'"}'
{"user": "ruan"}
```

### here doc
Here 文档（here document）是一种输入多行字符串的方法，格式如下。
它的格式分成开始标记（`<< token`）和结束标记（`token`）, 一般用字符串`EOF`作为token

```
<< token
text
token
```

例如

```
bash-5.1$ cat << EOF
> 11
> 22
> 33
> EOF
11
22
33
```

### here string 
Here 文档还有一个变体，叫做 Here 字符串（Here string），使用三个小于号（`<<<`）表示。
它的作用是将字符串通过标准输入，传递给命令。

```
bash-5.1$ cat <<< foobar
foobar
bash-5.1$ echo foobar | cat
foobar
```

## 变量
bash 是基于标准输入在不同进程间交互数据的，大部分功能都是在操作字符串，所以**变量的默认类型也是字符串**。

### 声明变量和读取变量
声明时等号两边不能有空格。
Bash 变量名区分大小写，`HOME`和`home`是两个不同的变量。

```
bash-5.1$ foo=1
bash-5.1$ echo $foo
1

```

### 变量查看和删除
```
# 查看所有变量, 其中包含父进程export的变量
bash-5.1$ set
UID=501
USER=ruan
bar=2
foo=1

bash-5.1$ unset foo
bash-5.1$ set
UID=501
USER=ruan
bar=2
```

### 变量输出
用户创建的变量仅可用于当前 Shell，子 Shell 默认读取不到父 Shell 定义的变量。
如果希望子进程能够读到这个变量，需要使用export命令。

```
bash-5.1$ bash -c set  | grep foo
bash-5.1$ export foo=1
bash-5.1$ bash -c set  | grep foo
foo=1
```

### 环境变量
平时所说的环境变量，就是init进程export输出的。子进程对变量的修改不会影响父进程，也就是说变量不是共享的。

```
# 查看环境变量
bash-5.1$ env
SHELL=/bin/zsh
LSCOLORS=Gxfxcxdxbxegedabagacad
ITERM_PROFILE=Default
```

下面是一些常见的环境变量。
*   `BASHPID`：Bash 进程的进程 ID。
*   `BASHOPTS`：当前 Shell 的参数，可以用`shopt`命令修改。
*   `DISPLAY`：图形环境的显示器名字，通常是`:0`，表示 X Server 的第一个显示器。
*   `EDITOR`：默认的文本编辑器。
*   `HOME`：用户的主目录。
*   `HOST`：当前主机的名称。
*   `IFS`：词与词之间的分隔符，默认为空格。
*   `LANG`：字符集以及语言编码，比如`zh_CN.UTF-8`。
*   `PATH`：由冒号分开的目录列表，当输入可执行程序名后，会搜索这个目录列表。
*   `PS1`：Shell 提示符。
*   `PS2`： 输入多行命令时，次要的 Shell 提示符。
*   `PWD`：当前工作目录。
*   `RANDOM`：返回一个0到32767之间的随机数。
*   `SHELL`：Shell 的名字。
*   `SHELLOPTS`：启动当前 Shell 的`set`命令的参数
*   `TERM`：终端类型名，即终端仿真器所用的协议。
*   `UID`：当前用户的 ID 编号。
*   `USER`：当前用户的用户名。

### 特殊变量
Bash 提供一些特殊变量。这些变量的值由 Shell 提供，用户不能进行赋值。
- `$?`: 上一个命令的退出码, 0为成功，其他为失败
- `$$`: 当前进程的pid
- `$_`: 为上一个命令的最后一个参数
- `$!`: 为最近一个后台执行的异步命令的进程 ID。
- `$0`: bash脚本的参数列表，0是脚本文件路径，1到n是第1到第n个参数

### 变量默认值
- `${varname:-word}`: 如果变量varname存在且不为空，则返回它的值，否则返回word
- `${varname:=word}`: 如果变量varname存在且不为空，则返回它的值，否则将它设为word，并且返回word。
- `${varname:+word}`: 如果变量名存在且不为空，则返回word，否则返回空值。它的目的是测试变量是否存在。
- `${varname:?message}`: 如果变量varname存在且不为空，则返回它的值，否则打印出varname: message，并中断脚本的执行。

### declare 命令
`declare`命令的主要参数（OPTION）如下。
*   `-a`：声明数组变量。
*   `-A`：声明关联数组变量。
*   `-f`：输出所有函数定义。
*   `-F`：输出所有函数名。
*   `-i`：声明整数变量。
*   `-p`：查看变量信息。
*   `-r`：声明只读变量。
*   `-x`：该变量输出为环境变量。 

```
# 声明为整数，可以直接计算，不需要使用$符号
bash-5.1$ declare -i val1=12 val2=5
bash-5.1$ echo $val1
12
bash-5.1$ val1+=val2
bash-5.1$ echo $val1
17

# 一个变量声明为整数以后，依然可以被改写为字符串。Bash 不会报错，但会赋以不确定的值
bash-5.1$ val1=aaa
bash-5.1$ echo $val1
0
```

## 数据类型
bash 有字符串，数字，数字，关联数组四种数据类型，默认是字符串，其他类型需要手动声明。

### 字符串
#### 定义
语法 `varname=value`
```
bash-5.1$ s1=abcdefg
bash-5.1$ echo $s1
abcdefg
```

#### 获取长度（length）
语法 `${#varname}`
```
bash-5.1$ echo ${#s1}
7
```

#### 子字符串（substr）
语法 `${varname:offset:length}`, offset为负数的时候，前面要加空格，防止与默认值语法冲突。
```
bash-5.1$ echo ${s1:1:3}
bcd
bash-5.1$ echo ${s1: -6:2}
bc
bash-5.1$ echo ${s1: -6:3}
bcd
``` 

#### 替换 （replace）
##### 字符串头部的模式匹配
- `${variable#pattern}`: 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
- `${variable##pattern}`: 删除最长匹配（贪婪匹配）的部分，返回剩余部分

匹配模式pattern可以使用*、?、[]等通配符。
```
$ myPath=/home/cam/book/long.file.name

$ echo ${myPath#/*/}
cam/book/long.file.name

$ echo ${myPath##/*/}
long.file.name
```

##### 字符串尾部的模式匹配
- `${variable%pattern}`: 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
- `${variable%%pattern}`: 删除最长匹配（贪婪匹配）的部分，返回剩余部分

```
$ path=/home/cam/book/long.file.name

$ echo ${path%.*}
/home/cam/book/long.file

$ echo ${path%%.*}
/home/cam/book/long
```

##### 任意位置的模式匹配
如果匹配`pattern`则用`replace`替换匹配的内容
- `${variable/pattern/replace}`: 替换第一个匹配
- `${variable//pattern/replace}`: 替换所有匹配

```
$ path=/home/cam/foo/foo.name

$ echo ${path/foo/bar}
/home/cam/bar/foo.name

$ echo ${path//foo/bar}
/home/cam/bar/bar.name
```

### 数字
### 数组
### 关联数组

## 控制流
### 条件判断
### 循环
### 分支

## 函数

## 脚本相关
### 几个关键概念
#### shebang
#### 返回码
#### 参数
#### 文件描述符

未完待续

## 参考
- https://wangdoc.com/bash/