title: Redis原理 —— dict 数据结构
date: 2021-04-17 9:48 AM
categories: 编程
tags: [Redis, C]

----

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
    // 类型特定函数
    dictType *type;
    // 私有数据
    void *privdata;
    // 哈希表
    dictht ht[2];
    // rehash 索引
    // 当 rehash 不在进行时，值为 -1
    int rehashidx; /* rehashing not in progress if rehashidx == -1 */

    // 目前正在运行的安全迭代器的数量
    int iterators; /* number of iterators currently running */

} dict;
```
