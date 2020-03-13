title: Python不完全指北
date: 2018-03-31 9:48 PM
categories: 编程
tags: [Python,]

----

## 缘起
从大学开始接触Python，到现在也差不多四年了，也算小有所成。期间也有很多人问我如何学习Python，也只是零散地回答，刚好最近要做个Python的分享，就将这一块东西整理一下。

## 简介
Python（音：派森），是一种强类型的动态语言，由吉多·范罗苏姆 创造，第一版发布于 1991 年。

### 名称由来
Python的创始人为吉多·范罗苏姆。1989年的圣诞节期间，吉多·范罗苏姆为了在阿姆斯特丹打发时间，决心开发一个新的脚本解释程序，作为ABC语言的一种继承。之所以选中Python作为程序的名字，是因为他是BBC电视剧——蒙提·派森的飞行马戏团的爱好者。

<!--more-->

### 创始人
吉多·范罗苏姆（荷兰语：Guido van Rossum，1956年1月31日－），生于荷兰哈勒姆，计算机程序员，为Python程序设计语言的最初设计者及主要架构师。

在Python社区，吉多·范罗苏姆被人们认为是“仁慈的独裁者”（BDFL），意思是他仍然关注Python的开发进程，并在必要的时刻做出决定。

1982年，在阿姆斯特丹大学获得数学和计算机科学硕士学位，后来他在多个研究机构工作。
2002年，获得由自由软件基金会颁发的2001年自由软件进步奖。
2003年，获得了荷兰UNIX用户小组奖。
2006年，被美国计算机协会（ACM）认定为著名工程师。
2005年，加入Google。他用Python语言为Google写了面向网页的代码浏览工具Mondrian，之后又开发了Rietveld。在那里他把一半的时间用来维护Python的开发。
2012年，Dropbox宣布吉多·范罗苏姆加入Dropbox公司。

### 设计哲学
Python的设计哲学是“优雅”、“明确”、“简单”。

Python开发者的哲学是“用一种方法，最好是只有一种方法来做一件事”，也因此它和拥有明显个人风格的其他语言很不一样。

在设计Python语言时，如果面临多种选择，Python开发者一般会拒绝花俏的语法，而选择明确没有或者很少有歧义的语法。

这些准则被称为“Python格言”。在Python解释器内运行import this可以获得完整的列表。

```python
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

Python之禅 by Tim Peters

优美胜于丑陋（Python 以编写优美的代码为目标）
明了胜于晦涩（优美的代码应当是明了的，命名规范，风格相似）
简洁胜于复杂（优美的代码应当是简洁的，不要有复杂的内部实现）
复杂胜于凌乱（如果复杂不可避免，那代码间也不能有难懂的关系，要保持接口简洁）
扁平胜于嵌套（优美的代码应当是扁平的，不能有太多的嵌套）
间隔胜于紧凑（优美的代码有适当的间隔，不要奢望一行代码解决问题）
可读性很重要（优美的代码是可读的）
即便假借特例的实用性之名，也不可违背这些规则（这些规则至高无上）
不要包容所有错误，除非你确定需要这样做（精准地捕获异常，不写 except:pass 风格的代码）
当存在多种可能，不要尝试去猜测
而是尽量找一种，最好是唯一一种明显的解决方案（如果不确定，就用穷举法）
虽然这并不容易，因为你不是 Python 之父（这里的 Dutch 是指 Guido ）
也许好过不做，但不假思索就动手还不如不做（动手之前要细思量）
如果你无法向人描述你的方案，那肯定不是一个好方案；反之亦然（方案测评标准）
命名空间是一种绝妙的理念，我们应当多加利用（倡导与号召）
```

## 特色

### 简单
Python 是一门简单且简约的语言。阅读一份优秀的 Python 程序代码就如同在阅读英语文章一样，尽管这门英语要求十分严格！

Python 这种伪代码式的特质正是它的一大优势。它能够让你专注于解决问题的方案，而不是语言本身。

### 跨平台性
由于其开放源码的特性，Python 已被移植到其它诸多平台。

如果你小心地避开了所有系统依赖型的特性, 你所有的 Python 程序可以在其中任何一个平台上工作，不必作出任何改动。

你可以在 GNU/Linux、Windows、FreeBSD、Macintosh、 Solaris、 OS/2、 Andorid 等等平台上运行 Python！

### 解释性
有关这一特性，需要一些详细的解释。

Python 不需要将其编译成二进制码, 你只需要直接从源代码运行该程序。

这使得 Python 程序更便携且易于迁移，你只需要将 Python 程序拷贝到另一台电脑便可让它立即开始工作！

### 面向对象
Python 同时支持面向过程编程与面向对象编程。

在面向过程的编程语言中，程序是由仅仅带有可重用特性的子程序与函数所构建起来的。

在面向对象的编程语言中，程序是由结合了数据与功能的对象所构建起来的。

与 C++ 或 Java 这些大型语言相比，Python 具有其特别的、功能强大又简单的方式来实现面向对象编程, 而且`万物皆对象`。

### 胶水语言
Python 很容易和其他语言一同开发, 从而享受到各种不同语言的便利。

如果你需要代码的某一重要部分能够快速地运行，或希望算法的某些部分不被公开，你可以在 C 或 C++ 语言中编写这些程序，然后再将其运用于你的 Python 程序中。

同时，你也可以在你的 C 或 C++ 程序中嵌入 Python，从而向你的程序用户提供脚本功能。

### 丰富的库
Python 标准库的规模非常庞大, 可谓`自带军需`。

它能够帮助你完成诸多事情，包括正则表达式、文档生成、单元测试、多线程、数据库、网页浏览器、CGI、FTP、邮件、XML、XML-RPC、HTML、WAV 文件、密码系统、GUI，以及其它系统依赖型的活动。

除了标准库以外，你还可以在 [PYPI（Python Package Index）](https://pypi.org/) 中发掘许多其它高质量的库。

## 语法简介
### 基本数据类型
1. string 字符串
一个由字符组成的不可更改的有序列。又单引号或双引号包围，如: `"strings"`。

2. byte 字节串
一个由字节组成的不可更改的有序列。常用来表示二进制数据，如: `b"bytes"`

3. float 浮点数
浮点数， 精度与系统相关， 不区分单精度双精度。如: `3.1415926`

4. int 整数
整数，不区分是否是长整型。如：`3`

5. complax 复数
复数，如：`3+2.7j`

6. list 列表
可以包含多种类型的可改变的有序列，如： `[1, "a", b"c", ]`

7. touple 元组
可以包含多种类型的不可改变的有序列，如： `(1, "a", b"c", )`

8. set 集合
与数学中集合的概念类似。无序的、每个元素唯一。，如： `{1, "a", b"c", }`

9. dict 字典
一个可改变的由键值对组成的无序列。如： `{"a": 1, "b": 2}`

10. bool 布尔值
逻辑值。只有两个值：真: `True`、假: `False`。

### 变量与赋值
1. 变量的使用不用预先定义，在使用时赋值即可. 变量只是值的容器，没有类型的限制.
2. 赋值：用等号连接左侧的变量和右侧的值，格式 `name = value`
```
>>> a = 1
>>> a
1
>>> a = "@@@"
>>> a
'@@@'
```

### 运算符
主要的算术运算符与C/C++类似。
- +, -, *, /, //, **, ~, %分别表示加法或者取正、减法或者取负、乘法、除法、整除、乘方、取补、取模。
- \>\>, <<表示右移和左移。
- &, |, ^表示二进制的AND, OR, XOR运算。
- \>, <, ==, !=, <=, >=用于比较两个表达式的值，分别表示大于、小于、等于、不等于、小于等于、大于等于。
- 在这些运算符里面，~, |, ^, &, <<, >>必须应用于整数。
- Python使用and, or, not表示逻辑运算。
- is, is not用于比较两个变量是否是同一个对象。in, not in用于判断一个对象是否属于另外一个对象。

### 控制流
#### 循环
1. for
```Python
>>> for i in [1,2,3]:
...     print(i)
1
2
3
```

2. while
```
>>> i = 1
>>> while i <= 3:
...     print(i)
...     i = i + 1
1
2
3
```

3. break 结束循环
```
>>> for i in [1, 2, 3]:
...     print(i)
...     if i > 1:
...         break
1
2
```

4. continue 跳过本次循环
```
>>> for i in [1, 2, 3]:
...     if i == 2:
...         continue
...     print(i)
1
3
```

#### 分支
if/else, 其中else不是必须的

```
>>> a = 1
>>> if a > 0:
...     print(1)
... else:
...     print(2)
1

>>> if a > 0:
...     print(1)
... elif a == 1:
...     print(2)
... else:
...     print(3)
1
```

### 函数
#### 调用函数
函数的多条语句的集合

Python内置了很多有用的函数，我们可以直接调用。

要调用一个函数，需要知道函数的名称和参数，比如求绝对值的函数abs，只有一个参数。

```
>>> abs(-1)
1
```

#### 定义函数
```
>>> def my_abs(x):
...     if x >= 0:
...         return x
...     else:
...         return -x

>>> my_abs(-1)
1
```

### 类和实例
类是面向对象的重要组成元素, 是创造对象的模板, 比如Person类.

而实例是根据类创建出来的一个个具体的“对象”，每个对象都拥有相同的方法，但各自的数据可能不同, 实例是数据和方法的集合.

```
>>> class Person(object):
...     total = 0
...     def __init__(self, name, age):
...         self.name = name
...         self.age = age
...         Person.total = Person.total + 1
...     def talk(self):
...         print('My name is {}, I am {} years old.'.format(self.name, self.age))

>>> tom = Person('tom', 1)

>>> tom.talk()
My name is tom, I am 1 years old.
>>> Person.total
1

>>> jerry = Person('jerry', 2)

>>> jerry.talk()
My name is jerry, I am 2 years old.

>>> Person.total
2
```

## 应用场景
### Web应用开发
Python经常被用于Web开发, Python定义了WSGI标准应用接口来协调Http服务器与基于Python的Web程序之间的通信。

一些Web框架，可以让程序员轻松地开发和管理复杂的Web程序。

下面介绍最为常见的几个web框架

#### Django
[Django](https://www.djangoproject.com/)的主要目标是使得开发复杂的、数据库驱动的网站变得简单。
Django注重组件的重用性和“可插拔性”，敏捷开发和DRY法则（Don't Repeat Yourself）

大而全的Web框架，适合快速建站，自带的网站管理后台功能（admin）非常强大。

#### Flask
[Flask](http://flask.pocoo.org/)被称为“microframework”，因为它使用简单的核心，同时提供很好的扩展性, 可以用Flask-extension加入这些功能：ORM、窗体验证工具、文件上传、各种开放式身份验证技术。

小而美，适合写api服务，只需10行代码就能写好一个简单服务。Flask的扩展性固然很好，但是如果上面的功能你都需要，那么还是用Django比较好。

#### Tornado
[Tornado](http://www.tornadoweb.org/)全称Tornado Web Server，是一个用Python语言写成的Web服务器兼Web应用框架。
- 作为Web框架，是一个轻量级的Web框架，其拥有异步非阻塞IO的处理方式。
- 作为Web服务器，Tornado有较为出色的抗负载能力，官方用nginx反向代理的方式部署Tornado和其它Python web应用框架进行对比，结果最大浏览量超过第二名近40%。

性能强劲的异步框架，但是如果出问题调起来比较蛋疼。而且有了gevent之后，个人觉得用tornado的性能意义不大。
#### Sanic
[Sanic](https://github.com/huge-success/sanic)是异步框架新秀, 基于原生asyncio构建, 性能强劲, 适合编写高性能服务.

### 桌面软件
#### tkinter
Tkinter 是 Python 的标准 GUI 库。Tkinter只适合简单界面的程序开发，界面效果是系统原生框体，总之是比较丑。

如果是简单的工具开发，可以用这个。

#### wxPython
[wxPython](http://wxpython.org/)是Python语言的GUI工具包，作为Python的扩展模块实现，包装了wxWidgets。

可配置项比tkinter多些，配起来也比较复杂。

#### PyQt
- PyQt的API与Qt类似，Qt的文档通常仍然可以应用于PyQt。因此，PyQt的文档非常丰富。
- 如果程序员具备使用Qt的经验，一般很快就可以过渡到PyQt上。
- 由于PyQt同时使用Qt以及Python的两种内存管理方法，所以在使用PyQt的过程中要注意避免内存泄露以及悬挂指针。需要学习一些C++知识，主要是C++类型、内存管理两个方面，以便于阅读Qt文档和理解PyQt的行为。

PyQt应该是最全的跨平台GUI解决方案了，linux上不少程序都是PyQt开发的，而且只要程序颜值也ok，个人推荐。

### 系统管理
在很多操作系统里，Python是标准的系统组件。Python标准库包含了多个调用操作系统功能的库。

通过调用这些库, 可以编写很多系统管理的脚本. 例如, 通过pywin32这个第三方软件 包，Python能够访问Windows的COM服务及其它Windows API。

一般说来，Python编写的系统管理脚本在可读性、性能、代码重用度、扩展性几方面都优于普通的shell脚本, 可作为shell脚本的替代。

一般来说100行以上的shell脚本就可以考虑使用Python编写。

### 云计算
归功于Python提供覆盖了完善的标准库，以及Python代码的可读性和可维护性，Python在云计算这块也有较广的应用。

#### OpenStack
OpenStack是一个美国宇航局和Rackspace合作研发的开源云计算软件

OpenStack是基础设施即服务（IaaS）软件，提供了IaaS整套解决方案，让任何人都可以自行创建和提供云计算服务。

此外，OpenStack也用作创建防火墙内的“私有云”（Private Cloud），提供机构或企业内各部门共享资源。

#### 腾讯云
据了解，腾讯云大量使用Python做网络以及计算资源的管理。

### 科学计算
#### Matplotlib
用Python实现的类matlab的第三方库，用以绘制一些高质量的数学二维图形。

#### NumPy
基于Python的科学计算第三方库，提供了矩阵，线性代数，傅立叶变换等等的解决方案。

#### Pandas
Pandas对numpy进行了封装，是用于数据分析、数据建模、数据可视化的第三方库。

#### SciPy
基于Python的matlab实现，旨在实现matlab的所有功能。

### 游戏
很多游戏使用C++编写图形显示等高性能模块，而使用Python或者Lua编写游戏的逻辑、服务器。

#### PyGame
[Pygame](http://www.pygame.org/)是跨平台Python模块，专为电子游戏设计。

PyGame适合开发小游戏，大型游戏难度颇大。

#### cocos2d
[cocos2d](http://cocos2d.org/)是一个基于MIT协议的开源框架，最初的Cocos2D框架是使用Python编写的，基于pyglet开发。

可以用于构建游戏、应用程序和其他图形界面交互应用。被大量应用于手机游戏市场，愤怒的小鸟就是基于cocos2d开发。

### 爬虫
#### 简单爬虫
一个简单的爬虫，使用 requests + BeatifulSoup就可以快速实现。

requests请求获取html，通过BeatifulSoup进行解析，就能很轻松拿到想要的数据。

#### Scrapy
[Scrapy](https://scrapy.org/) 是一个爬虫的框架, 而不是一个简单的爬虫.

它整合了爬取, 处理数据, 存储数据的一条龙服务. 能够高效的开发, 爬取网页, 记录数据。

### 人工智能
对于整个机器学习，应用层面放眼望去基本就是Python与R的天下了，而R更偏向与统计学领域，而在深度学习Python简直是红透了半边天。

#### scikit-learn
[Scikit-learn](http://scikit-learn.org/)项目最早由数据科学家 David Cournapeau 在 2007 年发起，需要NumPy和SciPy等其他包的支持，是Python语言中专门针对机器学习应用而发展起来的一款开源框架。

Scikit-learn的基本功能主要被分为六大部分：分类，回归，聚类，数据降维，模型选择和数据预处理。

Scikit-learn本身不支持深度学习，也不支持GPU加速，因此这里对于MLP的实现并不适合于处理大规模问题。

#### TensorFlow
[TensorFlow](https://www.tensorflow.org/) 是一个针对深度学习的库，并藉由和谷歌的关系赢得了许多关注。

- 核心库“不仅”适用深度学习，且面向绝大部分的机器学习技术。
- 除了主要的机器学习功能以外，TensorFlow 还有自己的日志（logging）系统、可交互的日志可视化工具（interactive log visualizer），甚至有工程性非常强的（heavily engineered）服务架构（serving architecture）。
- TensorFlow 的执行（execution）模型有别于 Python 的 scikit-learn，或是 R 语言中大部分的工具。

#### Keras
[Keras](https://keras.io/)是基于TensorFlow，Theano与CNTK的高阶神经网络API。

keras+tensorflow应该算是比较好的一种解决办法。对于初学者可以用keras搭搭积木，熟悉之后可以和tensorflow配合起来实现很多复杂功能。

### 局限性
上面说了这么多Python的应用场景，接下来就说下Python的局限。
由于Python本身是解释性语言的，以及GIL的限制，使得其不可避免地由于性能问题被大家诟病。

这里说下个人的几点看法
- 一般情况，开发效率比运行效率，这时Python的运行效率可以接受
- 适用于IO密集型场景，CPU密集场景不建议适用
- 动态语言的特性, 对团队技术人员水准有一点要求, 否则代码很可能难以维护.

## 常见问题
### Python3还是Python2
如果是5年前问这个问题，可能还需要犹豫一下，今天来看毫无疑问是选择3。

到2020年Python2就会完全失去支持，也不会有新的版本出现。还有人专门设立了一个网站进行[Python2的死亡倒计时](https://pythonclock.org/)。

Python3还是Python2的问题，其实基本是每一个学习Python的人都会问的问题。

Python3还是Python2的区别主要在unicode的处理，以及一些内置库的命名上，具体可以看[这里](http://ponder.work/2017/08/30/difference-between-python2-and-python3/)

### 安装
#### Windows
访问 [](https://www.python.org/downloads/) 并下载最新版本的 Python 其安装过程与其它 Windows 平台的软件的安装过程无异。
注意：请务必确认你勾选了 Add Python 3.x to PATH 选项。

#### linux
- Ubuntu/Debain `sudo apt-get update && sudo apt-get install python3`
- fedora `yum update && yum install python3`
- centos 由于centos不支持Python3，只能自行编译安装

#### macOS
对于 Mac OS X 用户，你可以使用 [Homebrew](http://brew.sh/) 并通过命令 `brew install python3` 进行安装。

#### pyenv
对于macOS，linux，bsd等类unix系统来说，最好的安装管理Python的方式是通过[pyenv](https://github.com/yyuu/pyenv)。

pyenv 是 Python 版本管理工具。 pyenv 可以改变全局的 Python 版本，安装多个版本的 Python， 设置目录级别的 Python 版本，还能创建和管理 virtualenv 。所有的设置都是用户级别的操作，不需要 sudo 命令。

### 编辑器/IDE
#### pycharm
[pycharm](http://www.jetbrains.com/pycharm/)是jetbrains出品的ide，应该是宇宙最强的吧，有用过他家其他产品的应该很容易上手，有免费的社区版，功能基本够用。

唯一的不足是内存占用有点多，反应偏慢。

功能齐全适合新手使用

#### Visual Studio Code
[vscode](https://code.visualstudio.com/) 微软出品，免费开源。

安装Python插件之后可作为ide使用，功能也很全，本人主力使用。

#### Sublime Text 3
[Sublime Text](https://www.sublimetext.com/)是我第一个使用的代码编辑器，插件很多，响应很快。

vscode、atom一开始都是从Sublime Text上抄功能的。但是随着一段时间的发展Sublime Text渐渐赶不上这两家了，比较它只有一个开发者同时开发3个平台。

通过安装各种插件，基本上都是达到vscode、atom同等水平的易用性，需要多花一些时间配置。

不推荐新手使用

### 调试
#### print大法
通过打印变量的值进行调试，是最传统也是最直接的调试方法。但是过多的print信息比较难以清理

#### logging
Python自带logging模块，通过简单配置就可以方便地进行日志控制

#### IDLE（交互式命令行）
启动`python`命令就可以进入IDLE，通过IDLE，我们可以交互式地查看输入语句的执行结果，适用于新库的使用探索。
内置的IDLE功能比较简单，使用起来不是很方便。
其实有不少第三方的idle，实现了代码补全、历史记录等实用功能，非常推荐使用。
下面是我常用的两个第三方idle
- ptpython 执行`pip install ptpython`安装，执行`ptpython`启动
- ipython 执行`pip install ipython`安装，执行`ipython`启动

#### pdb
pdb是Python内置的单步调试库，通过打断点可以方便地对Python代码逐行调试。

#### gdb
pdb的使用需要预先在源码中引入，对于已经运行的程序无法调试。
这时就可以用到gdb进行调试，通过加载gdb的python插件，可以方便地对运行中的Python程序调试，对程序假死卡住的问题定位很有帮助。

### 性能优化
记住一个原则，不要过早优化。
一般的应用场景Python的性能都是够用的，如果真的遇到问题，下面也有几个方法解决

#### C扩展
通过将程序中计算密集，耗时最多的部分通过编写C扩展的形式脱离出来，在用Python去调用该扩展。该方法可以绕过GIL，能基本彻底解决性能问题，但开发成本基本高。

#### pypy
[pypy](http://pypy.org/)是用Python自身实现的解释器。针对CPython的缺点进行了各方面的改良, 最重要的一点就是Pypy集成了JIT（即时编译器），性能得到很大的提升， 可达CPython的几十倍以上的性能。
使用方便，可惜兼容性不佳，有些第三方库不能很好地支持，如numpy。

#### 异步
如果是IO密集型的性能问题，可通过异步的方式解决问题。
- 特别是对于web服务器，通过gevent的monkey patch，能够解决大部分的并发性能问题，方便快捷无痛，但是C扩展的IO不能被patch。
- 透过async def、await 编写异步代码，编写成本较高

### 代码规范
#### pep8
[pep8](https://www.jianshu.com/p/52f4416c267d)是python最普遍接受的代码规范，只要认真阅读一遍 PEP 8，并尽量遵守，你的代码就足够 Pythonic 了。

#### Google Python风格规范
[Google Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)，对pep8规范进行了扩充，并且有很多实际的例子。个人推荐

## 学习资源
### 快速上手
- [简明Python教程](https://www.gitbook.com/book/lenkimo/byte-of-python-chinese-edition/details)
- [廖雪峰Python教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
- 官方Tutorial[英文](https://docs.python.org/3/tutorial/index.html)[中文](http://docspy3zh.readthedocs.io/en/latest/tutorial/)

### 体系化学习
- [Python语言及其应用](https://book.douban.com/subject/26675127/)
- [Python参考手册](https://book.douban.com/subject/5401851/)
- [Python Cookbook](https://book.douban.com/subject/4828875/)

### 深入学习
- [流畅的Python](https://book.douban.com/subject/27028517/)
- [Python源码剖析](https://book.douban.com/subject/3117898/)
- [Python高性能编程](https://book.douban.com/subject/27064848/)

### 特定领域学习
- [Flask Web开发](https://book.douban.com/subject/26274202/)
- [利用Python进行数据分析](https://book.douban.com/subject/25779298/)
- [Python Web开发：测试驱动方法](https://book.douban.com/subject/26640135/)
