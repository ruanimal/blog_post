---
title: Python 循环变量泄露与延迟绑定
date: 2022-03-04 20:17:00
updated: 2022-03-05 13:15:04
categories: 编程
tags: [Python]

---
循环变量泄露与延迟绑定叠加在一起，会产生一些让人迷惑的结果。
<!--more-->

## 梦开始的地方

先看看一开始的问题，可以看到这里lambda函数的返回值一直在变。

```Python
xx = []
for i in [1,2,3]:
    xx.append(lambda: i)

print('a:', xx[0]())

for j in xx:
    print(j())

print('b:', xx[0]())

for i in xx:
    print(i, i())

print('c:', xx[0], xx[0]())

for i in [4, 5, 6]:
    print(i)

print('d:', xx[0], xx[0]())
```

输出如下

```
a: 3
3
3
3
b: 3
<function main2.<locals>.<lambda> at 0x10ca30310> <function main2.<locals>.<lambda> at 0x10ca30310>
<function main2.<locals>.<lambda> at 0x10ca303a0> <function main2.<locals>.<lambda> at 0x10ca303a0>
<function main2.<locals>.<lambda> at 0x10ca30430> <function main2.<locals>.<lambda> at 0x10ca30430>
c: <function main2.<locals>.<lambda> at 0x10ca30310> <function main2.<locals>.<lambda> at 0x10ca30430>
4
5
6
d: <function main2.<locals>.<lambda> at 0x10ca30310> 6
```

## 循环变量泄露
由于Python没有块级作用域，所以循环会改变当前作用域变量的值，也就是循环变量泄露。
**注意**：Python3中列表推导式循环变量不会泄露，Python2中和常规循环一样泄露。

```Python
x = -1
for x in range(7):
    if x == 6:
        print(x, ': for x inside loop')
print(x, ': x in global')
```

输出如下

```
6 : for x inside loop
6 : x in global
```

## 闭包与延迟绑定
再讲一下**闭包**，在一个内部函数中，对外部作用域的变量进行引用，(并且一般外部函数的返回值为内部函数)，那么内部函数就被认为是闭包。
这里所谓的引用可以也就是内部函数记住了**变量的名称**（而不是值，这个从ast语法树可以看出），而变量对应的值是会变化的。
如果在循环中定义闭包，引用的变量的值在循环结束才统一确定为最后一次循环时的值，也就是**延迟绑定**（lazy binding）。

所以下面的例子，`xx`的所有匿名函数的返回值均为`3`
```
xx = []
for i in [1,2,3]:
    xx.append(lambda: i)
```

## 最后
再分析一开始的问题，这里的匿名函数引用了变量`i`，而`i`是全局变量，所以再次使用`i`作为循环变量时，列表中的匿名函数引用的值就被覆盖了。

正确做法：
- 在独立的函数中定义闭包
- 闭包引用的变量应该是其他函数不可修改的
- 优先使用列表推导式

## 参考
- https://stackoverflow.com/questions/3611760/scoping-in-python-for-loops
- https://www.educative.io/courses/python-ftw-under-the-hood/N8RW8508RkL
- https://mail.python.org/pipermail/python-ideas/2008-October/002109.html