title: Lightgbm多线程卡死问题定位
date: 2020-01-25 5:03 PM
categories: 编程
tags: [Lightgbm, Python]

---

## 症状
最近在开发的lightgbm树模型，发现服务在处理了一定量请求后会卡死，请求无响应。

`pstack`之后发现, 进程卡在libgomp.so这个动态库的函数中. 证实确实是卡死

```
Thread 8 (Thread 0x7f8eb7900700 (LWP 1859)):
#0  0x00007f8e9def4af1 in ?? () from /usr/lib64/libgomp.so.1
#1  0x00007f8e9def23a0 in ?? () from /usr/lib64/libgomp.so.1
```

## 尝试
首先尝试google `lightgbm hang`, 看了前几条记录.

发现,github上的一个[issue](https://github.com/microsoft/LightGBM/issues/2217#issuecomment-501233873), 顺着发现官网文档上早就记录里这个问题, 并且提供了解决办法.

<!--more-->

![](http://image.runjf.com/mweb/2020-01-25-15799334551032.jpg)

意思是说,OpenMP这个库在多线程fork的时候, 存在bug, 对于C/C++程序必须在fork完成之后再使用OpenMP的功能.

所以解决方法有两个
1. 不使用多线程
2. 使用intel工具链编译lightgbm

### 不使用多线程
上面说了可以设置`nthreads=1`, 但是在python库中, 我并没有找到如何设置.

查看文档之后发现, 可以通过pip参数编译安装单线程版本.

```
pip install lightgbm --install-option=--nomp
```

安装完成后可以将site-packages中库文件复制备份, 方便部署. 参考路径

```
~/.pyenv/versions/3.6.9/lib/python3.6/site-packages/lightgbm
```

### intel工具链
配置intel工具链, 并从零开始编译, 整体流程比较复杂, 也不建议.

这里推荐使用conda来配置环境, 免去很多编译配置烦恼.

1. 安装[miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. conda添加intel channel: `conda config --add channels intel`

3. 安装相关库

	```bash
	conda create -n idp intelpython3_core python=3
	source activate idp
	conda install lightgbm
	```

## 参考
1. https://github.com/microsoft/LightGBM/issues/2217
2. https://lightgbm.readthedocs.io/en/latest/FAQ.html#lightgbm-hangs-when-multithreading-openmp-and-using-forking-in-linux-at-the-same-time
3. https://github.com/microsoft/LightGBM/blob/master/python-package/README.rst#build-threadless-version
4. https://software.intel.com/en-us/articles/using-intel-distribution-for-python-with-anaconda
