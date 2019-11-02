title: Python排序算法总结
date: January 20, 2016 5:03 PM
categories: 编程
tags: [Python]

----

## 一、冒泡排序 BubbleSort
### 介绍
遍历序列，比较两个元素，如果前面的大于后面的就交换两者的位置。其实称之为冒泡排序不如加沉底排序，因为每一轮比较，这一轮轮最大都会被排到序列末尾，其实沉底更为贴切。

### 步骤
1. 遍历序列，比较序列的相邻元素，比较n-1次，如果前面的大于后面的就交换两者的位置。
2. 比较次数减一，重复步骤1
3. 共遍历n-1次

### 代码
1. 原始版本
```python
def bubble_sort(arry):
    n = len(arry)
    while n > 1:
        n -= 1
        for x in range(n):
            if arry[x] > arry[x+1]:
                arry[x], arry[x+1] = arry[x+1], arry[x]
    return arry
```
2. 改进版本
```python
def bubble_sort(arry):
    n = len(arry)
    while n > 1:
        n -= 1
        swap_flag = False  # 增加一个标记，当排好序后直接退出
        for x in range(n):
            if arry[x] > arry[x+1]:
                arry[x], arry[x+1] = arry[x+1], arry[x]
                swap_flag = True
        if not swap_flag:
            break
    return arry
```

<!--more-->

## 二、选择排序 SelectionSort
### 介绍
还是先来看看选择排序的思想。选择排序的思想非常直接，不是要排序么？那好，我就从所有序列中先找到最小的，然后放到第一个位置。之后再看剩余元素中最小的，放到第二个位置……以此类推，就可以完成整个的排序工作了。

### 步骤
1. 在未排序序列中找到最小元素，存放到序列的起始位置。
2. 在未排序序列中找到最小元素，存放到序列的第二位置。
3. 以此类推，共遍历序列n次

### 代码
```python
def selection_sort(arry):
    n = len(arry)
    for i in range(0, n):
        min = i
        for j in range(i+1, n):
            if arry[j] < arry[min]:
                min = j
        arry[i], arry[min] = arry[min], arry[i]
    return arry
```

## 三、插入排序 InsertionSort
### 介绍
插入排序（Insertion Sort）是一种简单直观的排序算法。它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。

### 步骤
1. 从第一个元素开始，该元素可以认为已经被排序
2. 取出下一个元素，在已经排序的元素序列中从后向前扫描
3. 如果该元素（已排序）大于新元素，将该元素移到下一位置
4. 重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
5. 将新元素插入到该位置后
6. 重复步骤2~5

### 代码
```python
def Insertion_sort(arry):
    n = len(arry)
    for i in range(1, n):
        temp = arry[i]
        index = i
        for j in range(i-1, -1, -1):
            if temp < arry[j]:
                arry[j+1] = arry[j]
                index = j
            else:
                break
        arry[index] = temp
    return arry
```
## 四、希尔排序 ShellSort
### 介绍
希尔排序，也称递减增量排序算法，是插入排序的一种更高效的改进版本，我称之为`分组插入排序`。希尔排序是非稳定排序算法。
希尔排序是基于插入排序的以下两点性质而提出改进方法的
- 插入排序在对几乎已经排好序的数据操作时，效率高，即可以达到线性排序的效率
- 但插入排序一般来说是低效的，因为插入排序每次只能将数据移动一位

### 实现
希尔排序通过将比较的全部元素分为几个区域来提升插入排序的性能。这样可以让一个元素可以一次性地朝最终位置前进一大步。然后算法再取越来越小的步长进行排序，算法的最后一步就是普通的插入排序，但是到了这步，需排序的数据几乎是已排好的了（此时插入排序较快）。

假设有一个很小的数据在一个已按升序排好序的数组的末端。如果用复杂度为O(n2)的排序（冒泡排序或插入排序），可能会进行n次的比较和交换才能将该数据移至正确位置。而希尔排序会用较大的步长移动数据，所以小数据只需进行少数比较和交换即可到正确位置。

### 代码
```python
def shell_sort(arry):
    n = len(arry)
    step = int(round(n/2.0))
    while step > 0:
        for i in range(step, n):
            temp = arry[i]
            index = i 
            for j in range(i-step, -1, -step):
                if temp < arry[j]:
                    arry[j+step] = arry[j]
                    index = j
                else:
                    break
            arry[index] = temp
        step = int(round(step/2))
    return arry
```
## 五、归并排序 MergeSort
### 介绍
归并排序是建立在归并操作上的一种有效的排序算法。该算法是采用分治法（Divide and Conquer）的一个非常典型的应用。

首先考虑下如何将将二个有序数列合并。这个非常简单，只要从比较二个数列的第一个数，谁小就先取谁，取了后就在对应数列中删除这个数。然后再进行比较，如果有数列为空，那直接将另一个数列的数据依次取出即可。

### 实现
1. 先将序列递归分组，直到每组只有一个元素。
2. 将序列两两合并：只要从比较二个数列的第一个数，谁小就先取谁，取了后就在对应数列中删除这个数。然后再进行比较，如果有数列为空，那直接将另一个数列的数据依次取出即可。
3. 重复步骤2，直到所有序列都合并。

### 代码
```python
def merge_sort(arry):
    if len(arry) <= 1:
        return arry
    num = int(len(arry)/2)
    left = merge_sort(arry[:num])
    right = merge_sort(arry[num:])
    return merge(left, right)

def merge(left, right):
    l, r = 0, 0  #左右两个序列的指针
    result = []
    while l<len(left) and r<len(right):
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result
```
## 六、快速排序 QuickSort
### 介绍
快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为两个子序列（sub-lists）。一个序列大于基准，一个小于基准。再对这两个序列进行同样的操作，以此类推直到所有元素都排列好。

### 步骤
1. 从数列中挑出一个元素，称为"基准"（pivot），
2. 重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分割结束之后，该基准就处于数列的中间位置。这个称为分割（partition）操作。
3. 递归地（recursive）把小于基淮值元素的子数列和大于基淮值元素的子数列排序。递归的最底部情形，是数列的大小是零或一，也就是永远都已经被排序好了。虽然一直递迴下去，但是这个演算法总会结束，因为在每次的迭代（iteration）中，它至少会把一个元素摆到它最后的位置去。

### 代码
```python
def quick_sort(arry):
    return qsort(arry, 0, len(arry)-1)

def qsort(arry, left, right):
    if left >= right:
        return arry
    key = arry[right]  # 以未排序序列最后一个元素为基准
    l = left
    r = right
    while l < r:
        while arry[l] <= key and l < r:   # A.直到从左边找到一个比基准大的元素
            l += 1
        while arry[r] >= key and l < r:   # B.直到从右边找到一个比基准小的元素; 
            r -= 1	# A与B对调会出错，因为r可能会多移动一步，而arry[r]是要与arry[right]交换的
        arry[l], arry[r] = arry[r], arry[l]
    arry[r], arry[right] = arry[right], arry[r]
    qsort(arry, left, l-1)
    qsort(arry, r+1, right)
    return arry
```

## 七、桶排序 BucketSort
### 介绍
桶排序（Bucket sort）或所谓的箱排序，是一个排序算法，工作的原理是将数组分到有限数量的桶里。每个桶再个别排序（有可能再使用别的排序算法或是以递归方式继续使用桶排序进行排序）。桶排序是鸽巢排序的一种归纳结果。当要被排序的数组内的数值是均匀分配的时候，桶排序使用线性时间（Θ(n)）。但桶排序并不是比较排序，他不受到O(n log n)下限的影响。

### 步骤
1. 根据数据的分布范围建桶，比如年龄，就可以建1-100号的桶。
2. 根据每个数据的值，将它放到对应的桶中
3. 从1号到100号桶中，依次将数据倒出

### 代码
```python
def bucket_sort(array):
    buckets = {i:0 for i in range(1, 101)}  # 100 bucket
    for i in array:
        buckets[i] += 1
    result = []
    for i in xrange(1,101):
        result.extend([i] * buckets[i])
    return result
```

## 八、堆排序
### 介绍
堆排序在 top K 问题中使用比较频繁。堆排序是采用二叉堆的数据结构来实现的，虽然实质上还是一维数组。二叉堆是一个近似完全二叉树 。

二叉堆具有以下性质：

父节点的键值总是大于或等于（小于或等于）任何一个子节点的键值。
每个节点的左右子树都是一个二叉堆（都是最大堆或最小堆）。

### 步骤
1. 构造最大堆：若数组下标范围为1~n，考虑到单独一个元素是大根堆，则从下标n/2+1开始的元素均为大根堆。于是只要从n/2开始，向前依次构造大根堆，这样就能保证，构造到某个节点时，它的左右子树都已经是大根堆。

2. 堆排序（HeapSort）：由于堆是用数组模拟的。得到一个大根堆后，数组内部并不是有序的。因此需要将堆化数组有序化。思想是移除根节点，并做最大堆调整的递归运算。第一次将heap[1]与heap[n]交换，再对heap[1...n-1]做最大堆调整。第二次将heap[1]与heap[n-1]交换，再对heap[1...n-2]做最大堆调整。重复该操作直至heap[1]和heap[2]交换。由于每次都是将最大的数并入到后面的有序区间，故操作完后整个数组就是有序的了。

3. 最大堆调整（sink）：该方法是提供给上述两个过程调用的。目的是将堆的末端子节点作调整，使得子节点永远小于父节点 。

### 代码
```python
def heap_sort(array):
    # 此处用最大堆
    n = len(array)
    pq = [None] + array
    def sink(k):  # 下沉
        while 2*k <= n:
            j = 2*k 
            if j < n and pq[j] < pq[j+1]:
                j += 1
            if pq[k] >= pq[j]:
                break
            pq[k], pq[j] = pq[j], pq[k]
            k = j
    
    for k in xrange(n/2, 0, -1):
        sink(k)
    while n > 1:
        pq[1], pq[n] = pq[n], pq[1]
        n -= 1
        sink(1)
    return pq[1:]
```

## 总结
下面为以上八种排序算法指标对比情况：

| 排序方法 | 平均情况            | 最好情况    | 最坏情况    | 辅助空间         | 稳定性 |
|----------|---------------------|-------------|-------------|------------------|--------|
| 冒泡排序 | 〇(n^2)             | 〇(n)       | 〇(n^2)     | 〇(1)            | 稳定   |
| 选择排序 | 〇(n^2)             | 〇(n^2)     | 〇(n^2)     | 〇(1)            | 不稳定 |
| 插入排序 | 〇(n^2)             | 〇(n)       | 〇(n^2)     | 〇(1)            | 稳定   |
| 希尔排序 | 〇(nlog(n))~〇(n^2) | 〇(n^1.3)   | 〇(n^2)     | 〇(1)            | 不稳定 |
| 堆排序   | 〇(nlog(n))         | 〇(nlog(n)) | 〇(nlog(n)) | 〇(1)            | 不稳定 |
| 归并排序 | 〇(nlog(n))         | 〇(nlog(n)) | 〇(nlog(n)) | 〇(n)            | 稳定   |
| 快速排序 | 〇(nlog(n))         | 〇(nlog(n)) | 〇(n^2)     | 〇(log(n))~〇(n) | 不稳定 |
| 桶排序   | 〇(n+k)             | 〇(n+k)     | 〇(n^2)     | 〇(n)            | 稳定   |