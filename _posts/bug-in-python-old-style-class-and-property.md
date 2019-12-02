title: Python2 中 旧式类与property引发的bug
date: 2019-12-01 8:17 PM
categories: 编程
tags: [property, Python]

---

## 缘起
话接上回，说是接手了一个82年的~~拉菲~~Python项目，这次又发现了一个新坑

项目中用了一个上下文类，用于存储本次请求的一些数据，在开发过程中我想把这个上下文类dump成json，详细分析里面的数据，然而发现上下文类的行为不符合预期

## 症状
上下文类大概是这样

```python
class Context():
    def __init__(self):
        self._input_json = None
        self._result_dict = dict()

    @property
    def input_json(self):
        print 'get _input_json'
        return self._input_json

    @input_json.setter
    def input_json(self, input_json):
        print 'set _input_json %s ' % input_json
        self._input_json = input_json

    @property
    def result_dict(self):
        print 'get _result_dict'
        return self._result_dict

    @result_dict.setter
    def result_dict(self, result_dict):
        print 'set _result_dict %s ' % result_dict
        self._result_dict = result_dict
     
    # 我附加的to_dict方法   
    def to_dict(self):
        tmp = {}
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                tmp[k] = v
        return tmp
```

测试之后发现，结果明显不符合预期，两个属性只输出了一个
```python
>>> from test_property import  Context 
>>> c = Context()
... c.input_json = {'a': 1}
... c.result_dict['b'] = 2
... 
get _result_dict
>>> c.to_dict() 
{'_input_json': None, '_result_dict': {'b': 2}}
```

## 分析
看测试代码我们可以发现，在访问`result_dict`属性的时候，property是工作正常的（有对应的print)

但是对应设置`input_json`的时候, 却没有看到对应的print输出

所以可以断定，此处的property工作不正常。 

仔细看代码后，我发现`Context`是旧式类。可以看到，`A`, `B`, `C`三中类的写法，其中`A`和`B`都是旧式类`<type 'classobj'>`, `C`是新式类。（旧式类只在Python2中存在）。
我们这里`Context`的写法和`B`是一样的。

```python
>>> class A:
...     pass
...
... class B():
...     pass
...
... class C(object):
...     pass
...
>>> type(A)
<type 'classobj'>
>>> type(B)
<type 'classobj'>
>>> type(C)
<type 'type'>
```

然后自然就怀疑旧式类对property装饰器的支持存在问题。
一通google之后，确定旧式类是不支持property。

![](http://image.runjf.com/mweb/2019-12-02-15752721846597.jpg)

确切地说，是对property的支持不完整，具体来说有以下3点。
- 支持property的getter
- 不支持property的setter
- 不支持property的赋值保护 

## 参考
- https://help.semmle.com/wiki/display/PYTHON/Property+in+old-style+class
- https://stackoverflow.com/questions/9962037/pythons-property-decorator-does-not-work-as-expected

