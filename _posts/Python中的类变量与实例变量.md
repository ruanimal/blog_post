title: Python中的类变量与实例变量
date: May 10, 2016 10:27 PM
categories: 编程
tags: [Python]


----

　　对于初学者来说，python的类变量（也就是java中的静态变量）和实例变量（也就是属性）有一些很容易混淆的地方，同时对这些特性深入了解有助于理解python的面向对象思想。

## 类变量与实例变量区分
```python
>>> class ClassA(object):  # 1
...     num1 = 1  # 类变量
...     def __init__(self):
...         self.num2 = 2  # 实例变量，或者说属性

>>> a1 = ClassA()
>>> a1.num1
1
>>> ClassA.num1
1
>>> a1.num1 is ClassA.num1  # 2
True

>>> a1.num1 = 3
>>> a1.num1 is ClassA.num1  # 3
False

>>> a1.__class__.num1
1
>>> a1.__class__.num1 = 4  # 4
>>> ClassA.num1
4

>>> a2 = ClassA()
>>> a2.num1
4
```

1. 这里我们定义了`ClassA`类，它有一个类变量`num1`，还有一个实例变量`num2`。  
2. a1是ClassA的一个实例，当我们写下`a1.num1`的时候，实际上是引用类变量num1，因此`a1.num1 is ClassA.num1`值为`True`。  
3. 运行`a1.num1 = 3`的时候，其实给a1绑定了一个属性num1，这是动态语言的特性，此时`a1.num1 is ClassA.num1`值为`False`。
**因此我不建议通过实例的名称来引用类变量，这样容易引起混淆，你以为改变了ClassA.num1，其实没有。**
这里就扯到了Python的作用域与命名空间，运行`a1.num1`的时候，先是在a1自己的命名空间内查找num1，没找到就在所属类的命名空间找，还没有就抛出`AttributeError: 'ClassA' object has no attribute 'num3'`.
运行`a1.num1 = 3`之后，a1自己的命名空间内找到了num1，就不继续往上查找了。
4. 如果此时还想通过a1访问和改变类变量num1，可以通过`a1.__class__.num1`来访问。


以上这些，也适用于`staticmethod`和`classmethod`。


## 如果ClassA还有父类
<!--more-->

```python
>>> class FatherI(object):
...     num1 = 11

>>> class FatherII(object):
...     num1 = 111

>>> class ClassA(FatherI, FatherII):
...     num1 = 1
...     def __init__(self):
...         self.num2 = 2

>>> a1 = ClassA()
>>> a1.__class__
<class 'ClassA'>
>>> a1.__class__.__mro__
(<class 'ClassA'>, <class 'FatherI'>, <class 'FatherII'>, <type 'object'>)
>>> a1.__class__.__mro__[0].num1
1
>>> a1.__class__.__mro__[1].num1
11
>>> a1.__class__.__mro__[2].num1
111

>>> super(ClassA, a1).num1
11
>>> super(ClassA.__mro__[0], a1).num1
11
>>> super(FatherI, a1).num1
111
>>> super(ClassA.__mro__[1], a1).num1
111
>>> super(FatherII, a1).num1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'super' object has no attribute 'num1'
'super' object has no attribute 'num1'
```

- 如果ClassA还有父类，而且可能还有多个，想访问父类的类变量可以通过`__mro__`或者`super`。
- `__mro__`属性显示了一个类的继承树，也就是记录了所有属性和方法的查找顺序，由于此处是新式类，mro为广度优先。
由于`__mro__`是一个元祖，所以我们可以用`__mro__[1]`这种方式来访问继承树树上每个类的属性和方法。
- 使用super也能达到相同的效果，不过稍有不同.`super(ClassA, a1).num1`这个语句的意思其实是，在`__mro__`中访问`<class 'ClassA'>`后一个类，也就是`<class 'FatherI'>`的num1，所以此处值是11
