title: Python2 与 Python3 的一些区别（未完待续）
date: 2017-08-30 5:03 PM
categories: 编程
tags:

---

### unicode
Python2
- 字符串分 str('') 和 unicode(u'')
- str，就是以'xxx'形式输入的字符，实际储存的值是xxx经过系统默认字符集encode过的字节串（bytes），如'\xe8\x86\x9c'
- unicode，就是以u'xxx'形式输入的字符，实际储存的值是xxx对应的unicode码， 如u'\u819c'
- str，其实等于python3中的字节串（bytes）
- unicode，其实等于python3中的字符串（str）
- 在python2中unicode才是真正的字符串


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
>>> subprocess.check_output(['ls', '/mnt/d'])
'11\n11.txt\n1C63638E19E9\n360\xe6\x9e\x81\xe9\x80\x9f\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe4\xb8\x8                                                                                                                                          b\xe8\xbd\xbd\nBaiduNetdiskDownload\nBOOTICEx64.exe\nChrome\nDesktop.tar.gz\nDriverGenius\nGames\nJav                                                                                                                                          a\nModOrganizer\nmsys64\nmsys64.7z\nMy Documents\nMyDrivers\nNexus Mod Manager\nnodejs\nNVIDIA\npagef                                                                                                                                          ile.sys\nPortableApps\nProgram Files (x86)\nProjects\nreadme.png\n$RECYCLE.BIN\nSystem Volume Informa                                                                                                                                          tion\ntables.zip\nubuntu\nUsers\nVirtualBox VMs\n\xe6\x96\xb0\xe5\xbb\xba\xe6\x96\x87\xe4\xbb\xb6\xe5                                                                                                                                          \xa4\xb9\n\xe8\xbf\x85\xe9\x9b\xb7\xe4\xb8\x8b\xe8\xbd\xbd\n'
>>> _.decode('utf8')
u'11\n11.txt\n1C63638E19E9\n360\u6781\u901f\u6d4f\u89c8\u5668\u4e0b\u8f7d\nBaiduNetdiskDownload\nBOOT                                                                                                                                          ICEx64.exe\nChrome\nDesktop.tar.gz\nDriverGenius\nGames\nJava\nModOrganizer\nmsys64\nmsys64.7z\nMy Do                                                                                                                                          cuments\nMyDrivers\nNexus Mod Manager\nnodejs\nNVIDIA\npagefile.sys\nPortableApps\nProgram Files (x86                                                                                                                                          )\nProjects\nreadme.png\n$RECYCLE.BIN\nSystem Volume Information\ntables.zip\nubuntu\nUsers\nVirtualB                                                                                                                                          ox VMs\n\u65b0\u5efa\u6587\u4ef6\u5939\n\u8fc5\u96f7\u4e0b\u8f7d\n'
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

### 语法上区别
#### print
print 由内置关键字转变为print函数

### 一些库的区别
#### commands 

commands是python2中用来执行shell命令的一个内置库

python3 中已移除

#### supervisor

用于进程管理，只支持Python2