title: 《改善python的91建议》笔记
date: June 5, 2016 9:36 PM
categories: 编程
tags: [读书笔记, Python]

----

## 概述
文如其名，是由91篇关系不是很紧密的python文章集合而成
这本书和国内很多技术类书籍一样，排版的代码缩进很有问题，还有文章有些观点并不正确。

除此之外，还是有很多有用的知识点，需要读者自己辨别。

## 笔记
### Python的包和模块规范
结构日益规范化。现在的库或框架跟随了以下潮流：
- 包和模块的命名采用小写、单数形式，而且短小。
- 包通常仅作为命名空间，如只包含空的`__init__`.py文件。

### x, y=y, x赋值
Python表达式计算的顺序说起。

一般情况下Python表达式的计算顺序是从左到右，但遇到表达式赋值的时候表达式右边的操作数先于左边的操作数计算，因此表达式`expr3, expr4=exprl, expr2`的计算顺序是`exprl, expr2 —> expr3, expr4`。

因此对于表达式`x, y=y, x`,其在内存中执行的顺序如下：
1. 先计算右边的表达式`y,x`,因此先在内存中创建元组`(y,x)`，其标示符和值分别为y、x及其对应的值，其中y和x是在初始化时已经存在于内存中的对象。
2. 计算表达式左边的值并进行赋值，元组被依次分配给左边的标示符，通过解压缩(unpacking),元组第一标识符（为y)分配给左边第一个元素（此时为X)，元组第二个标识符(为x)分配给第二个元素（此时为y),从而达到x、y值交换的目的。

### 提高and、or表达式的效率
python的and、or表达式并不会将每个值都算出，一旦整个表达式的值已知，其他部分就不会被计算，并且返回最后计算的那个值。
因此，在编程过程中，如果对于or条件表达式应该将`值为真可能性较高的变量`写在or的前面；
而对于and则相反，应该推后。

<!--more-->

### 防止注入攻击
- `().__class__.__bases__[0].__subclasses__`可返回当前解释器进程中的所有类对象。
- `__import__("os").system("dir")`使用`__import__`可以导入模块，并且返回这个模块

### 不要在Python中使用++i
因为Python解释器会将`++i`操作解释为`+(+i)`,其中`+`表示正数符号。对于`--i`操作也是类似。

### for与while中的else子句
循环如果**正常结束**（没有break），则执行else子句。
```python
>>> for i in range(10):
...     if i < 4:
...         print i
... else:
...     print 'for loop completed'
0
1
2
3
for loop completed
```

### 不要在try...except的finally子句中return或break
1. 当try块中发生异常的时候，如果在except语句中找不到对应的异常处理，异常将会被临时保存起来。
2. 当finally执行完毕的时候，临时保存的异常将会再次被抛出，但如果finally语句中产生了新的异常或者执行了return或者break语句，那么临时保存的异常将会被丢失，从而导致异常屏蔽。
3. 在实际应用程序开发过程中，并不推荐在finally中使用return语句进行返回，这种处理方式不仅会带来误解而且可能会引起非常严重的错误。

### `__nonzero__()`方法约定了如何判断对象的真假
该内部方法用于对自身对象迸行空值测试，返回`0/1`或`True/False`。

如果一个对象没有定义该方法，Python将获取`__len__()`方法调用的结果来进行判断。`__len__()`返回值为0则表示为空。

如果一个类中既没有定义`__len__()`方法也没有定义`__nonzero__()`方法，该类的实例用if判断的结果都为True。

### 字符串是不可变对象
对于不可变对象来说，当我们对其进行相关操作的时候，Python实际上仍然保持原来的值而是重新创建一个新的对象，所以字符串对象不允许以索引的方式进行賦值.

当有两个对象同时指向一个字符串对象的时候，对其中一个对象的操作并不会影响另一个对象。

### 注意`*args`与`**kwargs`与默认参数
首先满足普通参数，然后是默认参数;
如果剩余的参数个数能够覆盖所有的默认参数，则默认参数会使用传递时候的值；
如果剩余参数个数不够，则尽最大可能满足默认参数的值（从前往后）。
除此之外其余的参数除了键值对以外所有的参数都将作为args的可变参数，kwargs则与键值对对应。
若kwargs中有键与默认参数重复，会抛出`TypeError`。

### 关于排序
1. `sorted()`与`sort()`
从函数的定义形式可以看出，sorted()接收任意可迭代的对象作为参数，返回排序后对象，而sort()—般作用于列表（是bound method），原位操作。针对元组使用sort()方法会抛出`AttributeError`，而使用sorted()函数则没有这个问题。

2. dict或者嵌套list排序，注意`itemgetter`用法
```python
>>> from operator import itemgetter
>>> itemgetter(1)('ABCDEFG')
'B'
>>> itemgetter(1,3,5)('ABCDEFG')
('B', 'D', 'F')
>>> itemgetter(slice(2,None))('ABCDEFG')
'CDEFG'

>>> phonebook = {'Linda': '7750', 'Bob': '9345', 'Carol': '5834'}
>>> sorted(phonebook.iteritems(),key=itemgetter(1))
[('Carol', '5834'), ('Linda', '7750'), ('Bob', '9345')]

>>> gameresult = [['Bob',95.00,'A'], ['Alan',86.0,'C'], ['Mandy',82.5,'A'],['Rob',86,'E']]
>>> sorted(gameresult, key=itemgetter(2,1))
[['Mandy', 82.5, 'A'], ['Bob', 95.0, 'A'], ['Alan', 86.0, 'C'], ['Rob', 86, 'E']]

>>> mydict={'Li':['M', 7], 'Zhang':['E',2], 'Wang': ['P', 3], 'Du':['C',2], 'Ma': ['C', 9], 'Zhe':['H', 7]}

>>> sorted(mydict.iteritems(), key=lambda (k,v): itemgetter(1)(v))
[('Zhang', ['E', 2]), ('Du', ['C', 2]), ('Wang', ['P', 3]), ('Li', ['M', 7]), ('Zhe', ['H', 7]), ('Ma', ['C', 9])]
```

### 元素频次统计
使用collections.Counter来对可迭代对象统计各元素出现次数，Counter类是dict的子类。
```python
>>> from collections import Counter
>>> Counter('qqqaaaasdfsdf')
Counter({'a': 4, 'q': 3, 's': 2, 'd': 2, 'f': 2})
```

### 处理csv用pandas模块
使用pandas处理大型CSV文件。

Pandas即PythonDataAnalysisLibrary,是为了解决数据分析而创建的第三方工具，它不仅提供了丰富的数据模型，而且支持多种文件格式处理，包括CSV、HDF5、HTML等，能够提供高效的大型数据处理。

### 解析xml使用cElementTree或lxml
一般情况使用ElementTree解析XML。

cElementTree是ElementTree的Cython实现，速度更快，消耗内存更少，性能上更占优势，在实际使用过程中应该尽量优先使用cElementTree。一般情况指的是XML文件大小适中，对性能要求并非非常严格。
如果在实际过程中需要处理的XML文件大小在GB或近似GB级别，第三方模块lxml会获得较优的处理结果。

### pickle与对象序列化
pickle估计是最通用的序列化模块了。
它还有个C语言的实现cPickle，相比pickle来说具有较好的性能，其速度大概是pickle的1000倍，因此在大多数应用程序中应该优先使用cPickle(注：cPickle除了不能被继承之外，它们两者的使用基本上区别不大)。
pickle中最主要的两个函数对为dump()和load(),分别用来进行对象的序列化和反序列化。

### logging非进程安全
Logging只是线程安全的，不支持多进程写人同一个日子文件.
因此对于多个进程，需要配置不同的日志文件，否则会出现log覆盖。

### mixin运行时动态改变基类
用mixin模式让程序更加灵活.，每个类都有`__bases__`属性，它是一个元组，用来存放所有的基类。
与其他静态语言不同，Python语言中的基类在运行中可以动态改变。所以当我们向其中增加新的基类时，这个类就拥有了新的方法，也就是所谓的混人（mixin）。这种动态性的好处在于代码获得了更丰富的扩展功能。

### `__init__()`与`__new__()`哪个才是构造方法
`__init__()`并不是真正意义上的构造方法，`__init__()`方法所做的工作是在类的对象创建好之后进行变量的初始化。

`__new__()`方法才会真正创建实例，是类的构造方法。`__new__()`方法是静态方法，而`__init__()`为实例方法。
`__new__()`方法一般需要返回类的对象，当返回类的对象时将会自动调用`__init__()`方法进行初始化，如果没有对象返回，则`__init__()`方法不会被调用。
`__init__()`方法不需要显式返回，默认为`None`,否则会在运行时抛出`TypeError`。**（新式类）**

```python
>>> class MyC(object):
...     @staticmethod
...     def __new__(cls,*args):
...         pass
...     def __init__(self):
...         print 'aa'

>>> a = MyC() 
# 此处的__init__()方法没被调用
###################################
>>> class MyC(object):
...     @staticmethod
...     def __new__(cls,*args):
...         return super(MyC, cls).__new__(cls, *args)
...     def __init__(self):
...         print 'aa'

>>> a = MyC()
aa
```

### 重写`__getattr__()`和`__getattribute__()`的注意事项
1. 在覆盖类的`__getattr__()`和`__getattribute__()`方法的时候需要特别小心，否则可能出现无穷递归。
2. 覆盖`__getattribute__()`方法之后，任何属性的访问都会调用用户定义的`__getattribute__()`方法，性能上会有所损耗，比使用默认的方法要慢。
3. 覆盖的`__getattr__()`方法如果能够动态处理事先未定义的属性，可以更好地实现数据隐藏。因为dir()通常只显示正常的属性和方法，因此不会将该属性列为可用属性

### `__metaclass__`与元编程
在新式类中当一个类未设置`__metaclass__`属性的时候，它将使用默认的type元类来生成类。而当该属性被设置时查找规则如下：
1. 如果存在`__dict__['__metadass__']`，则使用对应的值来构建类；否则使用其父类`__dict__['__metaclass__']`中所指定的元类来构建类，当父类中也不存在指定的metadass的情形下使用默认元类type。
2. 对于古典类，条件1不满足的情况下，如果存在全局变量`__metaclass__`，则使用该变量所对应的元类来构建类；否则使用`types.ClassType`。元方法可以从元类或者类中调用，而不能从类的实例中调用；但类方法可以从类中调用，也可以从类的实例中调用。

### `__hash__()`与可哈希
可哈希对象，它是通过`__hash__()`这个内置函数的，这在创建自己的类型时非常有用，因为只有支持可哈希协议的类型才能作为dict的键类型（不过只要继承自object的新式类默认就支持了）。

### 生成器用作上下文管理器。
```python
>>> from contextlib import contextmanager
... @contextmanager
... def tag(name):
... 	print"<%s>"%name
... 	yield
... 	print"</%s>"%name

>>> with tag("h1"):
... 	print"foo"
<h1>
foo
</h1>
```

