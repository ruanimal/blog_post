title: 除法在 python2 和 python3 中的区别
date: January 10, 2016 5:03 PM
categories: 编程
tags: 

---

### 总结
1. python2 中使用`from __future__ import division`就可以使用python3的除法。
2. python2 中`/`与操作数有关，`x / y`中x、y都为整型的话，为`floor除法`，否则为`true除法`也是日常的除法。
3. python3 中`/`为`true除法`， 与操作数无关。
4. `//`在 python2 与 python3 中并无差别， 都代表`floor除法`

### python3 
```python
>>> -5/3
-1.6666666666666667
>>> -5//3
-2
>>> -5.0/3
-1.6666666666666667
>>> -5.0//3
-2.0
```

### python2
```python
>>> -5/3
-2
>>> -5//3
-2
>>> -5.0/3
-1.6666666666666667
>>> -5.0//3
-2.0
```
