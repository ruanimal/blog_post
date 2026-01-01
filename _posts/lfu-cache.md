---
title: 缓存淘汰算法之LFU
date: 2021-06-23 22:48:00
updated: 2022-04-02 10:07:17
categories: 编程
tags: [缓存, Python,]

---
Least Frequently Used (LFU) 是一种常见的缓存淘汰算法，译为“最近最不经常使用”，也就是将缓存中使用次数最少的数据淘汰掉。

有两种常见的实现方法
- 小顶堆 + hashmap，插入和删除的复杂度为O(logN), 但淘汰相同访问次数的节点是不稳定的，因为堆排序不稳定。
- 数组存储数据项 + hashmap记录数据项index, 淘汰缓存的复杂度为O(N)

<!--more-->
特点
1. 一般情况下，LFU效率要优于LRU，且能够避免周期性或者偶发性的操作导致缓存命中率下降的问题
2. LFU存在历史数据影响将来数据的"缓存污染"问题。

## Python 实现
这里的Python实现是方案1

具体步骤
1. get元素时，如果存在则返回结果并更新访问次数
2. set元素时，如果存在则更新val并更新访问次数，否则检查是否淘汰缓存并插入新key

```python
from math import log, ceil

class MinHeap(object):
    def __init__(self):
        self._items = [None]
        self.need_swap = self.more

    @property
    def length(self):
        return len(self._items) - 1

    @property
    def depth(self):
        return ceil(log(self.length+1, 2))

    def more(self, i, j):
        return self._items[i] > self._items[j]

    def exch(self, i, j):
        self._items[i], self._items[j] = self._items[j], self._items[i]

    def swim(self, k):
        while k > 1 and self.need_swap(k//2, k):
            self.exch(k//2, k)
            k = k//2

    def sink(self, k):
        while 2 * k <= self.length:
            j = 2 * k
            if j < self.length and self.need_swap(j, j+1):
                j += 1
            if not self.need_swap(k, j):
                break
            self.exch(k, j)
            k = j

    def insert(self, val):
        self._items.append(val)
        self.swim(self.length)

    def top(self):
        if self.length > 0:
            return self._items[1]

    def del_top(self):
        if self.length > 0:
            self.exch(1, self.length)
            val = self._items.pop()
            self.sink(1)
            return val

    def __repr__(self):
        tmp = []
        seq = ' '
        for i in range(1, self.depth+1):
            l = seq.join([str(e) for e in self._items[2**(i-1):2**i]])
            tmp.append(l)
        return '\n'.join(tmp)

class Node:
    def __init__(self, key, val=None):
        self.key = key
        self.val = val
        self.count = 1

    def __gt__(self, other):
        return  self.count > other.count

    def __repr__(self):
        # return '<Node key={!r} val={!r} count={!r}>'.format(self.key, self.val, self.count)
        return '{}|{!r}'.format(self.key, self.count)

class LFUCache:
    def __init__(self, size):
        self.cache = {}
        self.heap = MinHeap()
        self.size = size

    def check_expired(self):
        if self.heap.length == self.size:
            node = self.heap.del_top()
            self.cache.pop(node.key)

    def update_count(self, node):
        idx = self.heap._items.index(node)
        node.count += 1
        self.heap.sink(idx)

    def get(self, key):
        node = self.cache.get(key, None)
        if not node:
            return
        self.update_count(node)
        return node.val

    def set(self, key, val):
        node = self.cache.get(key, None)
        if node:
            node.val = val
            self.update_count(node)
            return
        node = Node(key, val)
        self.check_expired()
        self.heap.insert(node)
        self.cache[key] = node

    def __repr__(self):
        return '<LFU {!r}>'.format(self.cache)
```

## 参考
- https://en.wikipedia.org/wiki/Least_frequently_used
- https://melonshell.github.io/2020/02/07/ds_cache_eli/