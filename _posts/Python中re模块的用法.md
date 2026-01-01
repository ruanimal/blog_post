---
title: Python中re模块的用法
date: 2016-05-08 21:37:00
updated: 2020-04-30 22:39:01
categories: 编程
tags: [Python, 正则表达式]


---
## 概述
re是python中的正则表达式处理模块，本文是为了总结re模块的用法。

至于正则表达式的写法可以看[正则表达式30分钟入门教程](http://deerchao.net/tutorials/regex/regex.htm)

## 用法
### re.compile
`re.complie(pattern, flags=0)`
把正则编译为`_sre.SRE_Pattern object`对象，在多次匹配的时候可提高运行效率。
```python
>>> pattern = re.compile(r'\w(o)')
>>> pattern.match('doooo')
<_sre.SRE_Match object at 0x7f45fc3d9990>
>>> pattern.match('doooo').group(1)
'o'
>>> re.match(r'\w(o)', 'doooo')
<_sre.SRE_Match object at 0x7f45ec0be0a8>
>>> re.match(r'\w(o)', 'doooo').group(1)
'o'
```
<!--more-->
### re.search
`re.search(pattern, string, flags=0)`
寻找整个文本，直到发现一个匹配的位置，返回MatchObject，未找到返回None

### re.match
`re.match(pattern, string, flags=0)`
检查文本的开头是否匹配，返回MatchObject，未找到返回None

### re.split
`re.split(pattern, string, maxsplit=0, flags=0)`
通过正则表达式分割字符，返回list对象。若表达式里使用了组，组匹配到的内容会加到结果中。
```python
>>> re.split(r'g(o)', 'Wo-rds, words, words.')
['Wo-rds, words, words.']
>>> re.split(r'\wo', 'Wo-rds, words, words.')
['', '-rds, ', 'rds, ', 'rds.']
>>> re.split(r'\w(o)', 'Wo-rds, words, words.')
['', 'o', '-rds, ', 'o', 'rds, ', 'o', 'rds.']
```
### re.findall
`re.findall(pattern, string, flags=0)`
查找所有匹配的对象，返回list。
```python
>>> re.findall(r'g(o)', 'Wo-rds, words, words.')
[]
>>> re.findall(r'w(o)', 'Wo-rds, words, words.')
['o', 'o']
>>> re.findall(r'w(o)(r)', 'Wo-rds, words, words.')
[('o', 'r'), ('o', 'r')]
```

### re.sub
`re.sub(pattern, repl, string, count=0, flags=0`
替换，返回替换后的字符。
repl参数可以为一个函数，该函数接受MatchObject，返回值为替换的字符串。
```python
>>> re.sub(r'w(o)(r)',r'*', 'Wo-rds, words, words.')
'Wo-rds, *ds, *ds.'
>>> def repl(match):
...     return '***%s***|+++%s+++' % (match.group(1), match.group(2))
>>> re.sub(r'w(o)(r)', repl, 'Wo-rds, words, words.')
'Wo-rds, ***o***|+++r+++ds, ***o***|+++r+++ds.'
```

### 匹配可选项 flags
flags是正则表达式匹配的一些选项
- `re.DEBUG`  输出匹配过程中的调试信息
- `re.IGNORECASE`  忽略大小写
- `re.LOCALE`  本地化标志
- `re.MULTILINE`  多行模式，使`^`和`$`匹配每行的行首和行尾
- `re.DOTALL`  使`.`匹配换行符
- `re.UNICODE`  使`\w`等匹配unicode字符
- `re.VERBOSE`  使正则表达式使用`""""""`能够跨多行，并且每行使用`#`添加注释

### re.compile对匹配效率的影响
```python
# -*- coding:utf-8 -*-

import re, time

def aa():
    now = time.time()
    string = 'sfsfdsdffffffffffsxcsdsffffffsdsfsffssadfsaasfffffsdssfssssdsdcvfgbdgssdfvdfsss'
    for i in xrange(5000000):
        re.match(r'f(s)', string)
    seconds = time.time() -now
    return seconds

def bb():
    now = time.time()
    string = 'sfsfdsdffffffffffsxcsdsffffffsdsfsffssadfsaasfffffsdssfssssdsdcvfgbdgssdfvdfsss'
    pp = re.compile(r'f(s)')
    for i in xrange(5000000):
        re.match(pp, string)
    seconds = time.time() -now
    return seconds

def cc():
    now = time.time()
    string = 'sfsfdsdffffffffffsxcsdsffffffsdsfsffssadfsaasfffffsdssfssssdsdcvfgbdgssdfvdfsss'
    pp = re.compile(r'f(s)')
    for i in xrange(5000000):
        pp.match(string)
    seconds = time.time() -now
    return seconds

print u'未使用compile: %s' % aa()
print u'通过re.match调用compile后的对象: %s' % bb()
print u'使用compile: %s' % cc()
```

**输出**
```
未使用compile: 5.53200006485
通过re.match调用compile后的对象: 11.4990000725
使用compile: 1.66799998283
```

* 可以看出，通过compile过的`_sre.SRE_Pattern object`对象进行match操作，效率大概比re.mathc高几倍。
* 而bb函数通过re.match调用compile后的对象，花费时间是未使用compile的两倍。
因为`re.match(pattern, string)`通过调用`re._compile(pattern).match(string)`来实现的，这样相当于每次匹配都进行了两次compile。
