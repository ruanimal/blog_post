---
title: Bitmap 原理及实现
date: 2021-05-31 21:48:00
updated: 2021-06-01 11:42:00
categories: 编程
tags: [Python, 数据结构]
---

所谓的 Bitmap 其实就是二进制位数组，由于元素是二进制位，每一个元素只占用1个bit，十分节省内存空间。

每一个bit有0、1两种状态，所以 Bitmap 适合应用于判断是否存在、桶排序（不含重复元素），具体来说可以用bitmap记录ip信息，实现布隆过滤器等等。
<!--more-->

## Bitmap 原理
Bitmap 可以看成是个二维数组，第一维取出的元素是byte，然后用第二维的index去访问该byte对应的位。

由于正常访问内存最小的单位的字节，操作具体的位需要位运算。

![](https://image.ponder.work/mweb/2021-05-31-16224684372402.jpg)

### 位运算
**注意**：这里的位移操作都是逻辑位移

一个byte有8bit， 设置某个位为1，需要用到`按位或 |`
```
第0个bit： byte |= 0b10000000
第1个bit： byte |= 0b01000000
...
第7个bit： byte |= 0b00000001

所以：设置byte的第n个bit(n取0到7)： byte |= (0b10000000 >> n)
```

判断某个位是否为1，需要用到`按位与 &`
过程和上面类似, 满足`byte & (0b10000000 >> n) == (0b10000000 >> n)`，则该位为1

将某个位置为0，需要用到`按位与 &`
```
第0个bit： byte &= 0b01111111
第1个bit： byte &= 0b10111111
...
第7个bit： byte &= 0b01111110

所以：第n个bit(n取0到7)： byte &= ((0b10000000 >> n) ^ 0b11111111)
Python中由于没有无符号数，所以算掩码（0b01111111）时不能用按位取反。
```

### Python实现
将使用到的掩码设置为常量，性能会更好，这里的实现主要是为了体现思路，便于理解

```Python
BYTE_WIDTH = 8

class BitMap:
    def __init__(self, size, fill=0):
        self._array = bytearray((fill for _ in range(size//BYTE_WIDTH+1)))

    def set(self, index):
        major, minor = divmod(index, BYTE_WIDTH)
        self._array[major] |= (0b10000000 >> minor)

    def get(self, index):
        major, minor = divmod(index, BYTE_WIDTH)
        mask = 0b10000000 >> minor
        return int(self._array[major] & mask == mask)

    def clear(self, index):
        major, minor = divmod(index, BYTE_WIDTH)
        self._array[major] &= ((0b10000000 >> minor) ^ 0b11111111)

    def get_bin(self):
        return ' '.join(('{:0>8}'.format(bin(i)[2:]) for i in self._array))
```

