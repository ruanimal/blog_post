---
title: Python2 中 enum 枚举库诡异行为探究
date: 2019-11-21 20:17:00
updated: 2021-03-25 21:41:32
categories: 编程
tags: [Enum, Python, ]

---
## 缘起
最近接手了一个82年的~~拉菲~~Python项目，简直酸爽。
Python版本用的是2.7.5，里面用的第三方库各种老旧，潜藏了不少深坑。这次我们就先讲enum库的坑，其他有空再聊。

enum是一个枚举类型的第三方库，在Python3.4以后就作为官方库存在了，[使用参考](https://www.liaoxuefeng.com/wiki/1016959663602400/1017595944503424)。
所以如果用新版本的Python就不会存在这个问题了，版本老旧害死人啊。

<!--more-->

## 症状
刚接手这个项目，在搭建环境的时候，装完依赖发现enum库不能按照预期工作（没有完善的requirements.txt是个坑）

**正式环境**
```python
>>> import sys
>>> sys.version
'2.7.5 (default, Nov  2 2019, 14:10:22) \n[GCC 4.4.7 20120313 (Red Hat 4.4.7-23)]'

>>> from enum import Enum
>>> class Weekday(Enum):
...     Sun = 0 # Sun的value被设定为0
...     Mon = 1
...     Tue = 2
...     Wed = 3
...     Thu = 4
...     Fri = 5
...     Sat = 6

>>> type(Weekday.Sun)
<type 'int'>

>>> Weekday.Sun
0
```

**开发环境**

```python
>>> import sys

>>> sys.version
'2.7.16 (default, Oct 31 2019, 06:57:54) \n[GCC 4.4.7 20120313 (Red Hat 4.4.7-23)]'

>>> from enum import Enum
... class Weekday(Enum):
...     Sun = 0 # Sun的value被设定为0
...     Mon = 1
...     Tue = 2
...     Wed = 3
...     Thu = 4
...     Fri = 5
...     Sat = 6

>>> type(Weekday.Sun)
<enum 'Weekday'>

>>> Weekday.Sun.value
0
```

很明显可以看到，`Weekday.Sun`的行为在两个环境不一致（其实第一个库用法不对）。
- 正式环境：`Weekday.Sun`的类型是`int`
- 我的开发环境: `Weekday.Sun`的类型是`<enum 'Weekday'>`

## 归因
一开始我以为的enum库的bug，在不同版本的Python中行为不一致。

打开库源码路径一看，还真是大吃一惊。

原来两个环境的enum库压根就不一样，实现方式也不太一样，所以行为不一样。

### 正式环境的库
安装的是：enum==0.4.7 [pypi](https://pypi.org/project/enum/)

目录结构:
```
enum.py
enum-0.4.7-py2.7.egg-info
├── PKG-INFO
├── SOURCES.txt
├── dependency_links.txt
├── installed-files.txt
├── not-zip-safe
├── requires.txt
└── top_level.txt
```

只包含了enum.py这个文件，而且里面的代码实现很糟糕，和Python官方库的行为不一致。
也没找到源码管理仓库，总体来说质量糟糕。

### 开发环境的库
安装的是：enum34==1.1.6 [pypi](https://pypi.org/project/enum34/)

目录结构:
```
enum
├── LICENSE
├── README
├── __init__.py
└── __init__.pyc
enum34-1.1.6.dist-info
├── DESCRIPTION.rst
├── INSTALLER
├── METADATA
├── RECORD
├── WHEEL
├── metadata.json
└── top_level.txt
```

和上面的库不同的是，这个库是个Python包，通过元类的方法实现枚举类，行为和Python3的官方库一致。
代码质量较高，并且有Python2和Python3的兼容代码。

### 然而
这个老项目用的是第一个库，牵涉的东西比较多，暂时不能改动，只能将错就错。

## 思考
### pip和pypi的问题
1. 库名称和Python包、模块名称可能是不一致的。
2. pip安装的时候，没有对同名包、模块做冲突检测

这个两个问题都与Python Zen的“显式胜于隐含”的理念相冲突，这个是很不应该的。

### 同名模块和包优先级
在同一目录存在同名包和模块的情况下，疑似Python会优先加载包，没有查到确切的文档。

具体的加载行为，后面看一下源码分析一下。

### 技术人员知识储备
一开始调侃说，82年的Python项目。其实这个项目是在2017年左右启动的，但是里面使用的大部分是过时的技术。

为何呢？无非是舒适区，或者说紧跟时代是一件挺难的事情。
