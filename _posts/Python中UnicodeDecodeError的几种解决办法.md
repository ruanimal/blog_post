---
title: Python2中UnicodeDecodeError的几种解决办法
date: 2016-04-16 21:45:00
updated: 2016-08-25 18:05:00
categories: 编程
tags: [Python, 编码]
---

## 原理
由于在Python2中字符串有两种类型`str`和`unicode`，他们都是`basestring`的子类。

str类型，即是ascii字符或者经过encode的unicode，一个字符占用1byte。ascii码是美国信息交换标准代码，主要用于显示现代英语和其他西欧语言，用一个字节储存一个字符，所以ascii字符最多只有256(2^8)个。

而unicode包含了256个ascii码之外还包含其他各个国家的文字的编码，所以unicode的一个字符占用2个字节，这样理论上一共最多可以表示2^16（即65536）个字符，远大于256。

utf-8是unicode的一中实现，是unicode的一种编码方式。而且utf-8的编码方式，包含了ascii码的内容，也就是utf-8兼容ascii。

打个比方，unicode是商品，utf-8就是打包好的一个个包裹(encode)，打包是为了传输和储存的方便。而不同的编码之间不能直接互相转换，都需要转成unicode，也就是decode。

所以碰到一个str，你就得明白它是encode过的，你得调用相应的decode方法才不会乱码。

python2解释器的默认编码方式是ascii，如果我们给系统的输入是非ascii编码的字符，系统在尝试解码时就会出现`UnicodeDecodeError`

```
>>> s = '2'
>>> u = u'2'
>>> type(s)
<type 'str'>
>>> type(u)
<type 'unicode'>
>>> issubclass(str,basestring)
>>> issubclass(unicode,basestring)
True
>>> '啊'.decode('ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
```

## 几种解决方法

<!--more-->

### 修改系统编码
这种方法较为普遍
```python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

### 使用codec模块
常用于文本文件操作
```python
import codecs
with codecs.open('somefile.txt', 'r', 'utf-8') as fp:
    pass
```

### 改用Python3
此乃釜底抽薪，一劳永逸的办法。





