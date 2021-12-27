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
`*`字符代表文件路径里面的任意数量的任意字符，包括零个字符。

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

方括号扩展有一个简写形式`[start-end]`，表示匹配一个连续的范围

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

```shell
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
* `BASHPID`：Bash 进程的进程 ID。
* `BASHOPTS`：当前 Shell 的参数，可以用`shopt`命令修改。
* `DISPLAY`：图形环境的显示器名字，通常是`:0`，表示 X Server 的第一个显示器。
* `EDITOR`：默认的文本编辑器。
* `HOME`：用户的主目录。
* `HOST`：当前主机的名称。
* `IFS`：词与词之间的分隔符，默认为空格。
* `LANG`：字符集以及语言编码，比如`zh_CN.UTF-8`。
* `PATH`：由冒号分开的目录列表，当输入可执行程序名后，会搜索这个目录列表。
* `PS1`：Shell 提示符。
* `PS2`： 输入多行命令时，次要的 Shell 提示符。
* `PWD`：当前工作目录。
* `RANDOM`：返回一个0到32767之间的随机数。
* `SHELL`：Shell 的名字。
* `SHELLOPTS`：启动当前 Shell 的`set`命令的参数
* `TERM`：终端类型名，即终端仿真器所用的协议。
* `UID`：当前用户的 ID 编号。
* `USER`：当前用户的用户名。

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
* `-a`：声明数组变量。
* `-A`：声明关联数组变量。
* `-f`：输出所有函数定义。
* `-F`：输出所有函数名。
* `-i`：声明整数变量。
* `-p`：查看变量信息。
* `-r`：声明只读变量。
* `-x`：该变量输出为环境变量。

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
bash-5.1$ s1=abcdefg
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

匹配模式pattern可以使用`*`、`?`、`[]`等通配符。

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
使用 `declare -i`声明整数变量。

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

#### 数值的进制
Bash 的数值默认都是十进制，但是在算术表达式中，也可以使用其他进制。

*   `number`：没有任何特殊表示法的数字是十进制数（以10为底）。
*   `0number`：八进制数。
*   `0xnumber`：十六进制数。
*   `base#number`：`base`进制的数。

```
bash-5.1$ declare -i a=0x77
bash-5.1$ echo $a
119

bash-5.1$ declare -i a=0xfe
bash-5.1$ echo $a
254

bash-5.1$ declare -i a=2#111
bash-5.1$ echo $a
7
```

#### 算术表达式
`((...))`语法可以进行整数的算术运算。
支持的算术运算符如下。
*   `+`：加法
*   `-`：减法
*   `*`：乘法
*   `/`：除法（整除）
*   `%`：余数
*   `**`：指数
*   `++`：自增运算（前缀或后缀）
*   `--`：自减运算（前缀或后缀）

如果要读取算术运算的结果，需要在`((...))`前面加上美元符号`$((...))`，使其变成算术表达式，返回算术运算的值。

```
bash-5.1$ echo $((1+1))
2
bash-5.1$ echo $((1-1))
0
bash-5.1$ echo $((1*2))
2
bash-5.1$ echo $((1/2))
0
bash-5.1$ echo $((5%2))
1
bash-5.1$ a=1
bash-5.1$ echo $((a++))
1
bash-5.1$ echo $((a++))
2
bash-5.1$ echo $((++a))
4
```

### 数组
#### 创建数组 
`array=(item1 item2)` 语法可初始化数组，括号内可以换行，多行初始化可以用`#`注释。

```
# 直接初始化数组
bash-5.1$ a=(1 2 3)
bash-5.1$ echo ${a[@]}
1 2 3

# 多行初始化数组
bash-5.1$ a=(
> 1
> 2
> 3
> #4
> )
bash-5.1$ echo ${a[@]}
1 2 3

# 模式扩展初始化
bash-5.1$ a=({1..3})
bash-5.1$ echo ${a[@]}
1 2 3

# declare -a命令声明一个数组，也是可以的。
bash-5.1$ declare -a b
bash-5.1$ b+=(1)
bash-5.1$ echo ${b[@]}
1

#read -a命令则是将用户的命令行输入，存入一个数组。
bash-5.1$ read -a c
11 22 33
bash-5.1$ echo ${c[@]}
11 22 33
```

#### 访问数组元素
`array[index]` 语法可访问数组元素，不带index访问则是访问数组首个元素。

```
bash-5.1$ a=(1 2 3)
# 查看元素
bash-5.1$ echo ${a[1]}
2
# 元素赋值
bash-5.1$ a[1]+=1
bash-5.1$ echo ${a[1]}
21
bash-5.1$ a[1]=22
bash-5.1$ echo ${a[1]}
22
# 
bash-5.1$ a[0]=1111
bash-5.1$ echo ${a}
1111
bash-5.1$ echo ${a[0]}
1111
```

#### 数组长度
`${#array[@]}` 和 `${#array[*]}` 可访问获得数组长度

```
bash-5.1$ a=(1 2 3)
bash-5.1$ echo ${#a[*]}
3
bash-5.1$ echo ${#a[@]}
3
```

#### 获取非空元素下标
`${!array[@]}` 或 `${!array[*]}`, 可以获得非空元素的下标

```
bash-5.1$ a=(1 2 3)
bash-5.1$ a[6]=6
bash-5.1$ echo ${a[0]}
1
bash-5.1$ echo ${a[@]}
1 2 3 6
bash-5.1$ echo ${a[3]}

bash-5.1$ echo ${a[4]}

bash-5.1$ echo ${!a[@]}
0 1 2 6
# 注意此时数组长度为4，并不是7
bash-5.1$ echo ${#a[@]}
4
```

#### 数组元素切片
`${array[@]:position:length}`的语法可以提取数组成员。

```
bash-5.1$ a=({1..10})
bash-5.1$ echo ${a[@]}
1 2 3 4 5 6 7 8 9 10
bash-5.1$ echo ${a[@]:1:3}
2 3 4
```

#### 数组追加元素
数组末尾追加元素，可以使用`+=`赋值运算符。

```
bash-5.1$ a=({1..10})
bash-5.1$ echo ${a[@]}
1 2 3 4 5 6 7 8 9 10
bash-5.1$ a+=(11 12)
bash-5.1$ echo ${a[@]}
1 2 3 4 5 6 7 8 9 10 11 12
```

#### 删除元素
删除一个数组成员，使用`unset`命令。

```
bash-5.1$ a=(1 2 3)
# 删除单个元素
bash-5.1$ unset a[1]
bash-5.1$ echo ${a[@]}
1 3
# 删除整个数组
bash-5.1$ unset a
bash-5.1$ echo ${a[@]}
```

### 关联数组
`declare -A`可以声明关联数组，关联数组使用字符串而不是整数作为数组索引。

除了初始化外，使用方法和数组基本相同

```
bash-5.1$ declare -A a
bash-5.1$ a['red']=1
bash-5.1$ a['blue']=2
bash-5.1$ echo ${a[@]}
2 1
bash-5.1$ echo ${a[@]:0:1}
2
```

## 控制流
### 注释
`#`表示注释，每行从`#`开始之后的内容代表注释，会被bash忽略.

```
bash-5.1$ echo 1111 # 222
1111
```

### 条件判断
bash 和常规编程语言一样使用`if`作为分支条件的关键字, `fi`作为结束的关键字，`else`和
`elif`子句是可选的

其中`if`和`elif`的`condition`所判断的内容是命令的[状态码](#状态码)是否为0，为0则执行关联的语句。

```shell
# 因为bash中分号(;)和换行是等价的，所以有下面两种风格，其他多行语句也是类似的
# 本人偏好风格1
# 风格1
if condition; then
    command
elif condition; then
    command
else
    command
fi

# 风格2
if condition
then
    command
elif condition
then
    command
else
    command
fi
```

这里的`condition`可以是多个命令，如`command1 && command2`，或者`command1 || command2`，则if判断的是这两个命令的状态码的逻辑计算结果。

`condition`也是可以是`command1; command2`， 则则if判断的是最后一个命令的状态码。

这里最常用的`condition`是`test`命令, 也就是`[[]]`和`[]`. `test`是bash的内置命令，会执行给定的表达式，结果为真满足则返回状态码0, 否则返回状态码1.

下文循环语言的`condition`也是相同的，就不赘述了

```
bash-5.1$ test 1 -eq 1
bash-5.1$ echo $?
0
bash-5.1$ test 1 -eq 2
bash-5.1$ echo $?
1
```

`[[]]`和`[]`的区别是`[[]]`内部支持`&&`，`||`逻辑判断，所以以下三种写法是等价的。

由于`[`和`]`是命令， 所以两侧一定要有空格，也是就是`[ 1 -eq 1 ]`，否则bash会认为命令找不到。

```shell
# test 
if test 1 -eq 2 || test 1 -eq 1; then
    echo True
fi  

# [ ] 
if [ 1 -eq 2 ] || [ 1 -eq 1 ]; then
    echo True
fi  

# [[ ]]
if [[ 1 -eq 2  || 1 -eq 1 ]]; then
    echo True
fi  
```

#### 字符串判断
bash默认数据类型为字符串，所以常见的 `>`, `<`是用于字符串判断。

注意：字符串判断不支持`>=`和`<=`, 得使用逻辑组合来替代

* `-z string`：字符串串长度为0
* `-n string`: 字符串长度大于0
* `string1 == string2`: string1 等于 string2
* `string1 = string2`: string1 等于 string2
* `string1 > string2`: 如果按照字典顺序string1排列在string2之后
* `string1 < string2`: 如果按照字典顺序string1排列在string2之前

#### 数字(整数)判断
下面的表达式用于判断整数。
* `[ integer1 -eq integer2 ]`：如果`integer1`等于`integer2`，则为`true`。
* `[ integer1 -ne integer2 ]`：如果`integer1`不等于`integer2`，则为`true`。
* `[ integer1 -le integer2 ]`：如果`integer1`小于或等于`integer2`，则为`true`。
* `[ integer1 -lt integer2 ]`：如果`integer1`小于`integer2`，则为`true`。
* `[ integer1 -ge integer2 ]`：如果`integer1`大于或等于`integer2`，则为`true`。
* `[ integer1 -gt integer2 ]`：如果`integer1`大于`integer2`，则为`true`。

#### 文件判断
以下表达式用来判断文件状态。仅列举常用判断，详细支持列表参考 https://tldp.org/LDP/abs/html/fto.html

*   `[ -a file ]`：如果 file 存在，则为`true`。
*   `[ -d file ]`：如果 file 存在并且是一个目录，则为`true`。
*   `[ -e file ]`：如果 file 存在，则为`true`, 同`-a`。
*   `[ -f file ]`：如果 file 存在并且是一个普通文件，则为`true`。
*   `[ -h file ]`：如果 file 存在并且是符号链接，则为`true`。
*   `[ -L file ]`：如果 file 存在并且是符号链接，则为`true`, 同`-h`。
*   `[ -p file ]`：如果 file 存在并且是一个命名管道，则为`true`。
*   `[ -r file ]`：如果 file 存在并且可读（当前用户有可读权限），则为`true`。
*   `[ -s file ]`：如果 file 存在且其长度大于零，则为`true`。
*   `[ -w file ]`：如果 file 存在并且可写（当前用户拥有可写权限），则为`true`。
*   `[ -x file ]`：如果 file 存在并且可执行（有效用户有执行／搜索权限），则为`true`。

### switch case
bash也支持，switch case，语法如下。

```shell
case EXPRESSION in

  PATTERN_1)
    STATEMENTS
    ;;

  PATTERN_2)
    STATEMENTS
    ;;

  PATTERN_N)
    STATEMENTS
    ;;

  *)
    STATEMENTS
    ;;
esac
```

例如
```
a=2
case $a in  
1) 
    echo 11
    ;; 
2) 
    echo 22
    ;; 
*) 
    ;; 
esac
```

### 循环
#### while 循环
`while`循环有一个判断条件，只要符合条件，就不断循环执行指定的语句。
`condition`与if语句的相同，就不赘述了。

```shell
while condition; do
  command
done
```

#### unitl 循环
`until`循环与`while`循环恰好相反，只要不符合判断条件（判断条件失败），就不断循环执行指定的语句。一旦符合判断条件，就退出循环。

```shell
until condition; do
  command
done
```

#### for-in 循环
`for...in`循环用于遍历列表的每一项。

```shell
for variable in list; do
  commands
done
```

常见的几种用法
```shell
for i in 1 2 3; do
    echo $i
done

for i in {1..3}; do
    echo $i
done

list=(1 2 3)
for i in ${list[@]}; do
    echo $i
done
```

#### for 循环
`for`循环还支持 C 语言的循环语法。

```shell
for (( expression1; expression2; expression3 )); do
  commands
done
```

上面代码中，`expression1`用来初始化循环条件，`expression2`用来决定循环结束的条件，`expression3`在每次循环迭代的末尾执行，用于更新值。

注意，循环条件放在双重圆括号之中。另外，圆括号之中使用变量，不必加上美元符号`$`。

例如
```shell
for ((i=1; i<=3; i++)); do
    echo $i
done
```

#### 跳出循环
Bash 提供了两个内部命令`break`和`continue`，用来在循环内部跳出循环。

`break`命令立即终止循环，程序继续执行循环块之后的语句，即不再执行剩下的循环。
`continue`命令立即终止本轮循环，开始执行下一轮循环。

## 函数
### 函数定义
Bash 函数定义的语法有两种，其中`fn`为定义的函数名称。

```shell
# 第一种
fn() {
  # codes
}

# 第二种
function fn() {
  # codes
}
```

### 函数参数
函数体内可以使用参数变量，获取函数参数。函数的参数变量，与脚本参数变量是一致的。

*   `${N}`：函数的第一个到第N个的参数。
*   `$0`：函数所在的脚本名。
*   `$#`：函数的参数总数。
*   `$@`：函数的全部参数，参数之间使用空格分隔。
*   `$*`：函数的全部参数，参数之间使用变量`$IFS`值的第一个字符分隔，默认为空格，但是可以自定义。

### 函数调用
`funcname arg1 arg ... argN` 的语法进行函数调用。主要函数的返回值和输出值（标准输出）的区别，这和主流编程语言不同

```shell
add() {
    declare -i res
    res=0 
    for i in $@; do 
        res+=$i
    done
    echo $res
}

# 结果为10
add 1 2 3 4
```

### 函数返回值
`return`命令用于从函数返回一个值。返回值和命令的状态码一样，可以用`$?`拿到值。
`return`也可以不接具体的值，则返回值是return命令的上一条命令的状态码。
如果不加`return`，则返回值是函数体最后一条命令的状态码。

```shell
function func_return_value {
  return 10
}
```

## 关键概念
### shebang
Shebang（也称为Hashbang）是一个由井号和叹号构成的字符序列`#!`， 其出现在可执行文本文件的第一行的前两个字符。
在文件中存在Shebang的情况下，类Unix操作系统的程序加载器会分析Shebang后的内容，将这些内容作为解释器指令，并调用该指令.

例如，shell脚本
```bash
#!/bin/bash

echo Hello, world!
```

python 脚本
```python
#!/usr/bin/env python -u

print("Hello, world!")
```

### 状态码
每个命令都会返回一个退出状态码（有时候也被称为返回状态）。

成功的命令返回 0，不成功的命令返回非零值，非零值通常都被解释成一个错误码。行为良好的 UNIX 命令、程序和工具都会返回 0 作为退出码来表示成功，虽然偶尔也会有例外。

状态码一般是程序的main函数的返回码，如c,c++。
如果是bash脚本，状态码的值则是 `exit` 命令的参数值。
当脚本以不带参数的 `exit` 命令来结束时，脚本的退出状态码就由脚本中最后执行的命令来决定，这与函数的 `return` 行为是一致的。

### 文件描述符
文件描述符在形式上是一个非负整数。指向内核为每一个进程所维护的该进程打开文件的记录表。
当程序打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。

#### 标准输入输出
每个Unix进程（除了可能的守护进程）应均有三个标准的POSIX文件描述符，对应于三个标准流：
* `0`：标准输入
* `1`：标准输出
* `2`：错误输出

#### 打开新的文件描述符
手动指定描述符
```shell
exec 3<> /tmp/foo  #open fd 3.
echo "test" >&3
exec 3>&- #close fd 3.
```

系统自动分配描述符，bash4.1开始支持(在macos报错，原因不明)
```shell
#!/bin/bash

FILENAME=abc.txt

exec {FD}<>"$FILENAME"
echo 11 >&FD
echo 22 >&FD
$FD>&-
```

#### 描述符重定向
* `command > file`: 将输出重定向到 file。
* `command < file`: 将输入重定向到 file。
* `command >> file`: 将输出以追加的方式重定向到 file。
* `n > file`: 将文件描述符为 n 的文件重定向到 file。
* `n >> file`: 将文件描述符为 n 的文件以追加的方式重定向到 file。
* `n >& m`: 将输出文件 m 和 n 合并。
* `n <& m`: 将输入文件 m 和 n 合并。

所以命令中常见的`ls -al > output.txt 2>&1`, 就是将标准输出和错误输出都重定向到一个文件。
等价于`ls -al &>output.txt`，本人偏好这种写法，比较简洁。

### IFS (Input Field Separators)
IFS决定了bash在处理字符串的时候是如何进行单词切分。 
IFS的默认值是空格，TAB，换行符，即` \t\n`

```shell
$ echo "$IFS" | cat -et
 ^I$
$
```

例如，在for循环的时候，如何区分每个item
```shell
for i in `echo -e "foo bar\tfoobar\nfoofoo"`; do 
    echo "'$i' is the substring"; 
done
```

也可以自定义
```shell
OLD_IFS="$IFS"
IFS=":"
string="1:2:3"
for i in $string; do 
    echo "'$i' is the substring";
done 
IFS=$OLD_IFS
```


## 参考
- https://wangdoc.com/bash/
- https://tldp.org/LDP/abs/html/fto.html
- https://zh.wikipedia.org/wiki/Shebang
- https://en.wikipedia.org/wiki/File_descriptor
