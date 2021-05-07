title: Redis原理 —— SDS 数据结构
date: 2021-05-07 7:48 PM
categories: 编程
tags: [Redis, C]

----

Redis没有直接使用C语言传统的字符串表示，而是自己构建了一种名为简单动态字符串SD S(simple dynamic string)的数据结构 ，并将SDS用作Redis的默认字符串表示。

Redis内部所有字符串都由SDS来表示，其本质就是动态字节数组，和python的`bytearray`类似。
<!--more-->

## SDS 实现
```c
/*
 * 类型别名，用于指向 sdshdr 的 buf 属性, 用以和C字符串兼容
 */
typedef char *sds;

// 保存字符串对象的结构
struct sdshdr {
    // buf 中已占用空间的长度，不包含末尾的\0
    int len;
    // buf 中剩余可用空间的长度
    int free;
    // 数据空间, 柔性数组, 存储C字符串
    char buf[];
};
```

![](http://image.runjf.com/mweb/2021-05-07-16203880544303.jpg)

使用SDS时，一般是通过指向buf数组的指针而不是sdshdr，这样相关接口就和C字符串兼容。同时需要使用到len和free相关属性时，通过计算指针偏移来得到sdshdr指针，整体设计比较高效。
```c
static inline size_t sdslen(const sds s) {
    struct sdshdr *sh = (void*)(s-(sizeof(struct sdshdr)));
    return sh->len;
}
```

## 创建新SDS
创建比较简单，注意buf末尾的`\0`，以及最后返回的buf指针
```c
sds sdsnewlen(const void *init, size_t initlen) {
    struct sdshdr *sh;
    // 根据是否有初始化内容，选择适当的内存分配方式
    if (init) {
        // zmalloc 不初始化所分配的内存
        sh = zmalloc(sizeof(struct sdshdr)+initlen+1);
    } else {
        // zcalloc 将分配的内存全部初始化为 0
        sh = zcalloc(sizeof(struct sdshdr)+initlen+1);
    }
    if (sh == NULL) return NULL;
    // 设置初始化长度
    sh->len = initlen;
    // 新 sds 不预留任何空间
    sh->free = 0;
    // 如果有指定初始化内容，将它们复制到 sdshdr 的 buf 中
    if (initlen && init)
        memcpy(sh->buf, init, initlen);
    // 以 \0 结尾
    sh->buf[initlen] = '\0';
    // 返回 buf 部分，而不是整个 sdshdr
    return (char*)sh->buf;
}
```

## 容量调整
既然是动态数组，就会涉及到容量调整。
Redis的调整策略，当所需空间小于SDS_MAX_PREALLOC(当前版本是1MB)时是指数增长, 否则线性增长。

```c
sds sdsMakeRoomFor(sds s, size_t addlen) {
    struct sdshdr *sh, *newsh;
    // 获取 s 目前的空余空间长度
    size_t free = sdsavail(s);
    size_t len, newlen;
    // s 目前的空余空间已经足够，无须再进行扩展，直接返回
    if (free >= addlen) return s;
    // 获取 s 目前已占用空间的长度
    len = sdslen(s);
    sh = (void*) (s-(sizeof(struct sdshdr)));
    // s 最少需要的长度
    newlen = (len+addlen);
    // 根据新长度，为 s 分配新空间所需的大小
    // 小于SDS_MAX_PREALLOC(当前版本是1MB)时是指数增长, 否则线性增长
    if (newlen < SDS_MAX_PREALLOC)
        newlen *= 2;
    else
        newlen += SDS_MAX_PREALLOC;
    // 重新调整空间大小
    newsh = zrealloc(sh, sizeof(struct sdshdr)+newlen+1);
    if (newsh == NULL) return NULL;
    // 更新 sds 的空余长度
    newsh->free = newlen - len;
    return newsh->buf;
}
```

## 参考
- redis 3.0 源码
- redis 设计与实现