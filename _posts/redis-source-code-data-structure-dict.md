title: Redis原理 —— dict 字典
date: 2021-04-17 9:48 AM
categories: 编程
tags: [Redis, C]

----

这是Redis源码阅读系列第一篇文章。

dict 是 redis 最重要的数据结构，db、hash、以及服务器内部需要用到hashmap的场景都是用dict来实现的。学习 dict 的源码，我们可以学到hashmap的原理及实现。
<!--more-->

## dict 数据结构
哈希表元素节点
```c
typedef struct dictEntry {
    // 键，指向SDS(Redis字符串实现)
    void *key;
    // 值, 联合值, 可以是整数或者指针
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
    } v;
    // 指向下个哈希表节点，形成链表
    struct dictEntry *next;
} dictEntry;
```

哈希表
```c
typedef struct dictht {
    // 哈希表元素数组
    dictEntry **table;
    // 哈希表大小，初始值为4
    unsigned long size;
    // 哈希表大小掩码，用于计算索引值，总是等于 size - 1
    unsigned long sizemask;
    // 该哈希表已有节点的数量
    unsigned long used;
} dictht;
```

字典
```c
typedef struct dict {
    // 类型特定操作函数
    dictType *type;
    // 私有数据，保存了需要传给那些类型特定函数的可选参数
    void *privdata;
    // 哈希表，ht[1]在rehash的时候使用
    dictht ht[2];
    // rehash 索引，当 rehash 不在进行时，值为 -1
    int rehashidx;
    // 目前正在运行的安全迭代器的数量
    int iterators;
} dict;
```

结构体，储存不同类型字典的操作函数指针，实现了多态
```c
typedef struct dictType {
    // 计算哈希值的函数
    unsigned int (*hashFunction)(const void *key);
    // 复制键的函数
    void *(*keyDup)(void *privdata, const void *key);
    // 复制值的函数
    void *(*valDup)(void *privdata, const void *obj);
    // 对比键的函数
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);
    // 销毁键的函数
    void (*keyDestructor)(void *privdata, void *key);
    // 销毁值的函数
    void (*valDestructor)(void *privdata, void *obj);
} dictType;
```

![-w789](https://image.ponder.work/mweb/2021-04-18-16187320239054.jpg)

## 哈希算法
redis 的 dict 本质上就是个hashmap，其中的关键是哈希算法。

哈希函数（英语：Hash function）又称散列算法、散列函数，是一种从任何一种数据中创建小的数字“指纹”的方法。散列函数把消息或数据压缩成摘要，使得数据量变小，将数据的格式固定下来。该函数将数据打乱混合，重新创建一个叫做散列值的指纹。

比如取模函数就是一种最简单的对整数的哈希算法。

当字典被用作数据库的底层实现，或者哈希键的底层实现时，Redis使用 [MurmurHash2](https://zh.wikipedia.org/wiki/Murmur%E5%93%88%E5%B8%8C) 算法来计算键的哈希值。

具体求索引的过程

```c
// 求哈希值
hash = dict->type->hashFunction(kO);
// 根据哈希值和掩码计算出元素节点索引
index = hash & dict->ht[0].sizemask
```

## 冲突解决
当有两个或以上数量的键被分配到了哈希表数组的同一个索引上面时，我们称这些键发生了冲突。

常见冲突解决方法

- 链地址法：用链表储存冲突项
- 开放地址法：按照一定顺序寻找下一个可用位置(x为当前位置)
    + 线性探测法：按顺序向后查找，x+1, x+2, x+3
    + 平方探测法：平方向后查找，x+1,x+4,x+9
    + 双散列法

- 再哈希法：依次使用多个哈希函数

Redis的哈希表使用链地址法（separate chaining) 来解决键冲突，每个哈希表节点都有一个next指针，多个哈希表节点可以用 next指针构成一个单向链表，被分配到同一个索 引上的多个节点可以用这个单向链表连接起来，这就解决了键冲突的问题。

![-w722](https://image.ponder.work/mweb/2021-04-18-16187328149108.jpg)

还有一种常用的冲突解决办法是再哈希法，就是同时构造多个不同的哈希函数。
当H1 = hashfunc1(key) 发生冲突时，再用H2 = hashfunc1(key) 进行计算，直到冲突不再产生，这种方法不易产生聚集，但是增加了计算时间。

## rehash
随着操作的不断执行，哈希表保存的键值对会逐渐地增多或者减少，为了让哈希表的负载因子（used/size)维持在一个合理的范围之内，程序需要对哈希表的大小进行相应的扩展或者收缩, 这个过程就是rehash。

这里redis采用的装载系数为1，扩容系数为2

Redis对字典的哈希表执行rehash的步骤如下：
1. 为字典的`ht[1]`哈希表分配空间
2. 将保存在`ht[0]`中的所有键值对rehash到`ht[1]`上面：rehash指的是重新计算键的哈希值和索引值，然后将键值对放置到`ht[1]`哈希表的指定位置上
3. 全部复制完成后，释放`ht[0]`，将`ht[1]`设置为`ht[0]`，重置`ht[1]`

### 渐进式 rehash
所谓渐进式，是指rehash动作并不是一次性、集中式地完成的，而是分多次、渐进式地完成的。

由于redis是单线程的, 哈希表里保存的键值对又可能非常多，一次性将这些键值对全部rehash到ht[1]，会导致服务器在一段时间内停止服务。

所以需要渐进式 rehash，在字典的每个添加、删除 、查找和更新操作的时候，顺便进行部分元素的 rehash（目前实现是rehash一个元素），避免了集中式rehash而带来的庞大计算量。

rehash 示例代码
```python
def dictRehash(d: rDict, n: int) -> int:
    if not dictIsRehashing(d):
        return 0

    while (n):
        n -= 1
        if d.ht[0].used == 0:  # rehash 完成了
            del d.ht[0].table
            d.ht[0] = c_assignment(d.ht[1])
            _dictReset(d.ht[1])
            d.rehashidx = -1
            return 0

        assert d.ht[0].size > d.rehashidx
        # 找到第一个需要移动的元素
        while d.ht[0].table[d.rehashidx] is None:
            d.rehashidx += 1
        de = d.ht[0].table[d.rehashidx]
        while de:  # 移动该元素（包含整个冲突链表）到ht[1]
            nextde = de.next
            h = dictHashKey(d, de.key) & d.ht[1].sizemask
            de.next = d.ht[1].table[h]
            d.ht[1].table[h] = de  # 复制dictEntry元素
            d.ht[0].used -= 1
            d.ht[1].used += 1
            de = nextde
        d.ht[0].table[d.rehashidx] = None
        d.rehashidx += 1
    return 1
```

除了渐进式rehash，对于redis的多个db，也会有定时任务进行主动rehash，防止服务器长期没有执行命令时，数据库字典的 rehash 一直没办法完成。

## 参考
- redis 3.0 源码
- redis 设计与实现
