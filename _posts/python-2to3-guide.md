---
title: Python2迁移Python3指南
date: 2020-05-11 20:17:00
updated: 2020-07-08 14:53:00
categories: 编程
tags: [2to3, Python]
---

## 前置要求
- 了解Python3和Python2的区别，参考[Python2和Python3区别](/2017/08/30/difference-between-python2-and-python3/)，[Python3新特性](https://github.com/wjo1212/PythonChinaMeetup2020/blob/master/PythonChinaMeetup-20200510-Python3%E6%96%B0%E7%89%B9%E6%80%A7%E4%BB%8B%E7%BB%8D.pdf)
- 完备的测试用例
- 必要的工具：future，用于自动修改不兼容的语法。six，用于Python版本判断。pylint，语法检查
- 做好备份
- 测试（至关重要），下面的每一步改动都得确保代码行为没有发生变化。

### future安装
`pip install future -U`

<!--more-->

### 项目大致结构
```
├── ReadMe.md
├── requirements.txt
├── run.py
├── src
│   ├── __init__.py
│   ├── conf.py
│   ├── handlers
│   │   ├── __init__.py
│   │   └── draw.py
│   ├── process
│   │   ├── __init__.py
│   │   ├── decision.py
│   │   ├── preprocess.py
│   │   └── process.py
│   ├── service.py
│   └── workflow.py
├── tests
│   ├── __init__.py
│   ├── test_preprocess.py
```

## 修改过时的Python2代码
这一步用于测试的解释器是Python2
这一步是避免使用过于古老的Python2语法，将项目代码升级为更现代的Python2代码。

执行: `futurize --stage1 -w src tests`

可能涉及的改动
```Python
# 异常处理
-    except Exception, err:
+    except Exception as err:

# 字典元素判断
- if lr_space_dict.has_key(str(feature)):
+ if str(feature) in lr_space_dict:

# import方式改变
- from workflow import WorkFlow
+ from .workflow import WorkFlow

# print
- print 'load model %s' % self.name
+ print('load model %s' % self.name)
```

## 代码升级Python3， 并添加Python2支持
这一步用于测试的解释器是Python2
一般在升级过程中，不直接移除Python2支持，否则一旦发现问题难以回滚。
也不方便确认，代码改动是否产生了非预期的变化。

执行：`futurize --stage2 -x libfuturize.fixes.fix_unicode_keep_u -w src tests`

**注意**：由于futurize关于unicode的处理存在一些bug，所以字符编码的我们自己单独处理（见后文）。这里的`-x libfuturize.fixes.fix_unicode_keep_u`参数，跳过对unicode的自动处理，不将代码中的unicode替换为str。同时，我们要逐一去除文件中自动添加的`from builtins import str`，避免类似`import unicode as str`的行为。

可能涉及的改动:
1. 迭代器对象相关改动
2. 内置库重命名相关改动

```Python
# map() -> list(map())
- year1, month1, day1 = map(int, date_created.split(' ')[0].split('-'))
+ year1, month1, day1 = list(map(int, date_created.split(' ')[0].split('-')))

# dict.keys() - list(dict.keys())
- for city in city_dict.keys():
+ for city in list(city_dict.keys()):

# dict.iteritems() -> dict.items()
- for k, v in hawk_info.iteritems():
+ for k, v in hawk_info.items():
 
# dict.items() -> list(dict.iteritems())
- for name, val in trans_td_schema.items():
+ for name, val in list(trans_td_schema.items()):

# xrange -> list(range)
- for index in xrange(len(rule_files)):
+ for index in range(len(rule_files)):

# ConfigParser -> configparser
- import ConfigParser
+ from future import standard_library
+ standard_library.install_aliases()
+ import configparser
```

## Python文本处理改为unicode
这一步用于测试的解释器是Python2和Python3

正确处理字符的原则：
1. 程序内部均使用unicode，所以大部分业务代码不需要进行编码处理。
2. 对输入的二进制数据（文本，网络包等），使用对应的字符集进行decode(), 转为unicode
3. 将内部数据encode后进行传输存储

也就是：`外部数据（字节）-> decode -> unicode -> encode -> 输出数据（字节`

### 启用默认unicode支持
启用默认unicode支持：`futurize --stage1 --unicode-literals src tests -w`

涉及的改动:
```Python
# 所有文件的头部会增加下面的语句，作用是将源码中的所有字符串视作unicode
# 也就是 "中" 会等效于 u"中"， 不需要`u`作为unicode的前缀 
+ from __future__ import unicode_literals
```

### 修改编码相关的代码
1. str() -> unicode()
2. open -> io.open
3. 去除程序内部多余的encode，decode
4. redis, requests等库，增加必要的decode代码

涉及的改动:
```Python
# str() -> unicode()
- feature = str(feature)
+ feature = unicode(feature)

# open -> io.open
- with open(v) as f:
+ with io.open(v, encoding='utf8') as f:

# redis增加必要的decode代码
-     return self.connection.get(key)
+     res = self.connection.get(key)
+     return res.decode('utf8') if res is not None else None
```

### 为Python3添加unicode函数
为了代码在Python2和Python3都正确运行，必须给Python增加unicode函数。

如果后面代码不需要Python2支持，则这一步的改动可以去除，并且把所有的unicode调用改为str即可。

实现
```Python
import six

if six.PY2:
    from __builtin__ import unicode
else:
    class unicode(str):
        def __new__(cls, unicode_or_bytes=''):
            if isinstance(unicode_or_bytes, bytes):
                return str.__new__(cls, unicode_or_bytes, encoding='utf8')
            return str.__new__(cls, unicode_or_bytes)
```

## 修复于解释器版本相关的行为
这一步用于测试的解释器是Python2和Python3

### 字典/集合遍历顺序
python的字典遍历是不保证顺序的，不同版本解释器遍历顺序可能不同。
如果你的代码对遍历顺序有依赖，建议固定遍历顺序，可以使用OrderedDict，或者遍历前排序，或者指定遍历的key。

### round
Python2和Python3的四舍五入行为不一样。
如果有数值处理相关的代码，建议做如下修复.

```Python
def python2round(number, ndigits=0):
    if sys.version_info[0] == 2:
        return round(number, ndigits)

    from decimal import Decimal, ROUND_HALF_UP
    res = Decimal.from_float(number).quantize(Decimal(10) ** -ndigits, rounding=ROUND_HALF_UP)
    return float(res)
```

## 大功告成
至此，Python2到Python3的迁移已然完成，你获得了支持python3和python2的代码。

值得小酌一杯

## 参考
1. https://python-future.org/automatic_conversion.html
2. https://github.com/PythonCharmers/python-future
3. https://stackoverflow.com/questions/10825926/python-3-x-rounding-behavior#answer-10826537