title: Redis原理 —— zskiplist 跳跃表
date: 2021-04-20 9:48 PM
categories: 编程
tags: [Redis, C]

----

跳跃表 （skiplist) 是一种有序数据结构，它通过在每个节点中维持多个指向其他节点的 指针，从而达到快速访问节点的目的。

跳跃表优点
- 表支持平均`O(logN)`, 最坏`O(N)`复杂度的节点查找，效率可以和平衡树相当
- 通过顺序性操作来批量处理节点
- 实现比平衡树要来得更为简单

因为`ziplist`内存占用较小，所以Redis使用作为有序集合的初始底层结构。
如果一个有序集合包含的元素数量比较多（大于`zset-max-ziplist-entries`），又或者有序集合中元素的成员是比较长的字符串时（大于`zset-max-ziplist-value`），Redis就会将其底层结构转换为跳跃表。

<!--more-->

## zskiplist 数据结构
跳跃表节点, 其中`zskiplistLevel`成员是[柔性数组](https://gcc.gnu.org/onlinedocs/gcc/Zero-Length.html)
```c
typedef struct zskiplistNode {
    // 成员对象
    robj *obj;
    // 分值
    double score;
    // 后退指针
    struct zskiplistNode *backward;
    // 层
    struct zskiplistLevel {
        // 前进指针
        struct zskiplistNode *forward;
        // 跨度，经过的节点数目
        unsigned int span;
    } level[];  // 柔性数组
} zskiplistNode;
```

跳跃表
```c
typedef struct zskiplist {
    // 表头节点和表尾节点
    struct zskiplistNode *header, *tail;
    // 表中节点的数量
    unsigned long length;
    // 表中层数最大的节点的层数
    int level;
} zskiplist;
```

![](https://image.ponder.work/mweb/2021-04-23-16190066207268.jpg)

所谓跳跃表，就是多层链表（redis中的实现是最多32层）通过额外的链接提高效率，从低层到高层，节点之间的跨度逐渐变大。

跨度越大则查找效率越高，所以查找时是从高层往底层查找。

如果节点的最高层高为x，则可以认为该节点就存储在低x层，则表头到该节点的跨度之和为该节点的rank(排位)，所有节点的最大层高为跳跃表层高。

## 跳跃表插入节点
因为跳跃表是多层链表，所以插入节点的关键是找到每一层插入的位置，以及插入位置的跨度变化，还有新节点的跨度计算。

python 版跳跃表插入实现
```python
# 比较节点大小
def _node_lt(node: zskiplistNode, score: float, obj: robj):
    if node.score < score:
        return True
    if (node.score == score and
        compareStringObjects(node.obj, obj) < 0):
        return True
    return False

def zslInsert(zsl: zskiplist, score: float, obj: robj) -> zskiplistNode:
    # update list记录的是每一层, 新节点需要插入的位置(新节点x的backward节点指针)
    update: List[Opt[zskiplistNode]] = [None for _ in range(ZSKIPLIST_MAXLEVEL)]
    # rank[i]: 从高到低, 到第i层为止经过的所有node的span总和, 也就是节点的排序
    # 用于计算新节点各层的span, 以及新节点的后继节点各层的span
    rank = [0 for _ in range(ZSKIPLIST_MAXLEVEL)]
    x = zsl.header
    # 从高层开始遍历
    for i in range(zsl.level-1, -1, -1):
        rank[i] = 0 if i == zsl.level-1 else rank[i+1]
        # 找到每一层x需要插入的位置, 并更新rank
        while x.level[i].forward and _node_lt(x.level[i].forward, score, obj):
            rank[i] += x.level[i].span
            x = x.level[i].forward
        # 对于每一层i, 新节点会插入到update[i].level[i]之后
        update[i] = x
    level = zslRandomLevel()  # 取一个随机层数, 使zskiplist，每层节点更为均衡
    # 新节点层高增大的情况，更新扩展层的默认跨度
    if level > zsl.level:
        for i in range(zsl.level, level):
            rank[i] = 0
            update[i] = zsl.header
            update[i].level[i].span = zsl.length
        zsl.level = level
    # 更新节点x和前驱节点已有层的跨度
    x = zslCreateNode(level, score, obj)
    for i in range(level):
        x.level[i].forward = update[i].level[i].forward
        update[i].level[i].forward = x
        x.level[i].span = update[i].level[i].span - (rank[0] - rank[i])
        update[i].level[i].span = (rank[0] - rank[i]) + 1
    # 更新前驱节点扩展层的跨度，x节点这些层没有后继节点，所以跨度为0
    for i in range(level, zsl.level):
        update[i].level[i].span += 1  # type: ignore
    # 设置新节点的后退指针, level[0]才有后退指针
    x.backward = None if update[0] == zsl.header else update[0]
    if x.level[0].forward:
        x.level[0].forward.backward = x
    else:
        zsl.tail = x
    zsl.length += 1
    return x
```

## 跳跃表查找
跳跃表的查找则是从高层向低层查找，沿着最高层链表前进；遇到大于目标值的节点，则往下一层，直到找到相等的值为止。

经过的所有节点的跨度相加即是目标节点的rank。

```python
def zslGetRank(zsl: zskiplist, score: float, obj: robj) -> int:
    rank = 0
    x = zsl.header
    for i in range(zsl.level-1, -1, -1):
        while x.level[i].forward and _node_lt(x.level[i].forward, score, obj):
            rank += x.level[i].span
            x = x.level[i].forward
        if x.obj and equalStringObjects(x.obj, obj):
            return rank
    return 0
```

查找score=2.0的o2对象的过程
![](https://image.ponder.work/mweb/2021-04-23-16191635872238.jpg)

## 参考
- redis 3.0 源码
- redis 设计与实现
