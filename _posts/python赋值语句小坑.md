title: python赋值语句小坑
date: January 10, 2016 5:03 PM
categories: 编程
tags:  [Python, ]

---


说到python赋值语句，大家想必一个念头——so easy，不是`lz = 'dashabi'`吗。
确实，easy是easy，里面却有个小坑，虽小，却不易发现。在代码量多的时候，就有点恶心了。

**正常的语句是这样**
```python
>>> aa = u'这是一个坑'
>>> aa 
u'\u8fd9\u662f\u4e00\u4e2a\u5751'
```

**坑在这里**
```python
>>> aa = u'这是一个坑',
>>> aa 
(u'\u8fd9\u662f\u4e00\u4e2a\u5751',)
```
  

看出区别没有，坑的后面有个逗号，平时这逗号没什么卵用，但在赋值语句的末尾会将原来的对象转化为tuple。
和`aa = (u'这是一个坑',)`是一样的效果。