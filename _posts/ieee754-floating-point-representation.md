title: IEEE 754 与浮点数的二进制表示
date: 2020-08-03 8:17 PM
categories: 编程
tags: [浮点数, ]
mathjax: true

---

在计算机科学中，浮点（英语：floating point，缩写为FP）是一种对于实数的近似值数值表现法, 类似于十进制的[科学计数法](https://zh.wikipedia.org/wiki/%E7%A7%91%E5%AD%A6%E8%AE%B0%E6%95%B0%E6%B3%95).
<!--more-->
## 科学记数法
在科学记数法中，一个数被写成一个"实数"与一个10的`n`次幂的积
$$\pm a \times 10 ^ n$$
其中：
* $n$ 必须是一个整数, 可称之为指数。
* $a$ 必须是`[1, 10)`区间内的实数，可称为有效数或尾数。

类似的，二进制的科学计数法则是 $\pm a \times 2 ^ n$ ，不同的是 $a$ 必须是`[1, 2)`区间内的实数。

所以浮点数的二进制表示，就是用二进制位表示出 $\pm a \times 2 ^ n$ 。

我们可以将一定长度的二进制位分成三个部分，用来分别表示 $\pm$、$n$、$a$ 。

## IEEE 754浮点数表示
IEEE二进制浮点数算术标准（IEEE 754）是20世纪80年代以来最广泛使用的浮点数运算标准，为许多CPU与浮点运算器所采用。

IEEE 754规定，对于32位的浮点数，最高的1位表示符号 $\pm$ 记为`s`(sign)，接着的8位有符号整数表示指数 $n$ 记为`E`(exponent)，剩下的23位为有效数 $a$ 记为`M`(fraction)。

由于M的整数部分永远是1，我们可以只表示其小数部分，记为`N`，也就是最终可表示为 $s \times 2 ^ E \times (1+N)$ 。

具体各部分拆解如下，其中 $a_0$ 到 $a_{31}$ 对应32个二进制位的值，为`0`或者`1`。

$$s = (-1)^{a_{0}}$$
$$E = -127 + a_{1}\times 2^{7} + a_{2}\times 2^{6} + \dots + a_{8}\times2^0$$
$$N = a_{9}\times 2^{-1} + a_{10}\times 2^{-2} + \dots + a_{31}\times2^{-23}$$

以十进制的 $-5.0$ 为例，可表示为 $-1.25 \times 2 ^ 2$。那么，s=1，N=0.25，E=2。
具体来说
$$s=(-1)^0=1$$
$$E=-127 + 2^7 + 2^0 = 2$$
$$N=2^{-2}=0.25$$

![-w714](http://image.runjf.com/mweb/2020-08-04-15965370742818.jpg)

## 浮点数与二进制字符串转换
```python
def binary_to_float(data):
    assert len(data) == 32
    sign = (-1) ** int(data[0])
    exponent = 2 ** (-127 + sum(int(a) * 2 ** b for a, b in zip(data[1:9], range(7, -1, -1))))
    fraction = 1 + sum(int(a) * 2 ** b for a, b in zip(data[9:], range(-1, -24, -1)))
    return sign * exponent * fraction
    
def float_to_binary(data):
    import struct
    bins = struct.pack('>f', data)
    return ''.join('{:0>8}'.format(bin(i)[2:]) for i in bins)
```

## 参考
1. https://zh.wikipedia.org/wiki/IEEE_754
2. https://www.ruanyifeng.com/blog/2010/06/ieee_floating-point_representation.html
3. https://zh.wikipedia.org/wiki/%E7%A7%91%E5%AD%A6%E8%AE%B0%E6%95%B0%E6%B3%95
4. 《深入理解计算机系统》
