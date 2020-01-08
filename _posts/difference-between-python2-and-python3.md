title: Python2 与 Python3 区别
date: 2017-08-30 5:03 PM
categories: 编程
tags: [Python,]

---

## 速查表
Python2 vs Python3

| name          | Python2                | Python3           |                                            |
|---------------|------------------------|-------------------|--------------------------------------------|
| try | try except ValueError, e | try except ValueError as e | 
| exception | ValueError('aa').message | - | python3中可用ValueError('aa').args[0] 替代 |
| \_\_import\_\_ | \_\_import\_\_ | - | 可以用importlib.import_module替代 |
| print         | 关键字                    | 函数                |                                            |
| unicode       | unicode                | str               |     python2默认的string是bytes， Python3中是unicode                                       |
| bytes         | str                    | bytes             |                                            |
| division      | 1 / 2                  | 1 // 2            |                                            |
| division      | 1 / 2.0                | 1 / 2              |                                            |
| round         | round(0.5) == 1.0      | round(0.5) == 0   | Python3内建的 round 是四舍六入五成双的机制               |
| xrange        | xrange                 | range             |                                            |
| range         | range(1,2)             | list(range(1,2))  |                                            |
| reduce	 | reduce | - | Python使用functools.reduce替代 | 
| dict.keys     | dict.keys()            | list(dict.keys()) | python的dict遍历不保证顺序, 同一个字典py2和py3的遍历顺序可能不一样 |
| dict.iterkeys | dict.iterkeys()        | dict.keys()       |                                            |
| dict.items     | dict.items()            | list(dict.items()) |  |
| dict.iteritems | dict.iteritems()        | dict.items()       |                                            |
| 内置库           | commands               | -                 |   用subprocess替代                                         |
| 内置库           | sys.setdefaultencoding | -                 |                                            |
| 内置库           | Queue                  | queue             |                                                                                  |
| 内置库           | ConfigParser           | configparser      |  


## 详细对比
### unicode
Python2
- 字符串分 str('') 和 unicode(u'')
- str，就是以'xxx'形式输入的字符，实际储存的值是xxx经过系统默认字符集encode过的字节串（bytes），如'\xe8\x86\x9c'
- unicode，就是以u'xxx'形式输入的字符，实际储存的值是xxx对应的unicode码， 如u'\u819c'
- str，其实等于python3中的字节串（bytes）
- unicode，其实等于python3中的字符串（str）
- 在python2中unicode才是真正的字符串

<!--more-->

```python
>>> '膜法'
'\xe8\x86\x9c\xe6\xb3\x95'
>>> u'膜法'
u'\u819c\u6cd5'

>>> '膜法'.decode('utf8')
u'\u819c\u6cd5'
>>> print u'\u819c\u6cd5'
膜法
>>> print '\xe8\x86\x9c\xe6\xb3\x95'
膜法
>>> u'膜法'
u'\u819c\u6cd5'
>>> type('膜法')
<type 'str'>
>>> type(u'膜法')
<type 'unicode'>
>>>
```

Python3

```python
>>> '膜法'
'膜法'
>>> '\u819c\u6cd5'
'膜法'
>>> '膜法'.encode('utf8')
b'\xe8\x86\x9c\xe6\xb3\x95'
>>> type('膜法')
<class 'str'>
>>> type(b'\xe8\x86\x9c\xe6\xb3\x95')
<class 'bytes'>
>>> print('\xe8\x86\x9c\xe6\xb3\x95')
èæ³
>>> print(b'\xe8\x86\x9c\xe6\xb3\x95')
b'\xe8\x86\x9c\xe6\xb3\x95'
>>> print(b'\xe8\x86\x9c\xe6\xb3\x95'.decode('utf8'))
膜法
>>> print('\xe8\x86\x9c\xe6\xb3\x95')
èæ³
>>> print(b'\xe8\x86\x9c\xe6\xb3\x95'.decode('utf8'))
膜法
>>> '\xe8\x86\x9c\xe6\xb3\x95'.encode('latin-1')
b'\xe8\x86\x9c\xe6\xb3\x95'
```

### 文件读写
python2

```python
>>> aa = open('/mnt/d/11.txt', 'r')
>>> aa.readline()
' \xe9\xa9\xb1\xe5\x8a\xa8\xe5\x99\xa8 F \xe4\xb8\xad\xe7\x9a\x84\xe5\x8d\xb7\xe6\x98\xaf 20090108_171210\r\n'
>>> bb = open('/mnt/d/11.txt', 'rb')
>>> bb.readline()
' \xe9\xa9\xb1\xe5\x8a\xa8\xe5\x99\xa8 F \xe4\xb8\xad\xe7\x9a\x84\xe5\x8d\xb7\xe6\x98\xaf 20090108_171210\r\n'
>>> cc =  open('/mnt/d/11_gbk.txt', 'rb')
>>> cc.readline()
' \xc7\xfd\xb6\xaf\xc6\xf7 F \xd6\xd0\xb5\xc4\xbe\xed\xca\xc7 20090108_171210'
>>> dd =  open('/mnt/d/11_gbk.txt', 'r')
>>> dd.readline()
' \xc7\xfd\xb6\xaf\xc6\xf7 F \xd6\xd0\xb5\xc4\xbe\xed\xca\xc7 20090108_171210'
```

python3

```python
>>>  aa = open('/mnt/d/11.txt', 'r')  # 11.txt is saved as utf8
>>> aa.readline()
' 驱动器 F 中的卷是 20090108_171210\n'
>>> bb = open('/mnt/d/11.txt', 'rb')
>>> bb.readline()
b' \xe9\xa9\xb1\xe5\x8a\xa8\xe5\x99\xa8 F \xe4\xb8\xad\xe7\x9a\x84\xe5\x8d\xb7\xe6\x98\xaf 20090108_171210\r\n'
>>> cc =  open('/mnt/d/11_gbk.txt', 'rb')
>>> cc.readline()
b' \xc7\xfd\xb6\xaf\xc6\xf7 F \xd6\xd0\xb5\xc4\xbe\xed\xca\xc7 20090108_171210'
>>> dd = open('/mnt/d/11_gbk.txt', 'r')
>>> dd.readline()
Traceback (most recent call last):
  File "<ipython-input-10-ba8f5810b020>", line 1, in <module>
    dd.readline()
  File "/home/jayruan/.pyenv/versions/3.6.1/lib/python3.6/codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc7 in position 1: invalid continuation byte
```
