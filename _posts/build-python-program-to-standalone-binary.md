---
title: 用exxo将Python程序编译成单一可执行文件
date: 2020-02-29 09:48:00
updated: 2020-03-01 11:34:31
categories: 编程
tags: [Python,] 

---
## 缘起
golang将程序编译成一个可执行文件，部署起来特别方便。

那么Python是否也有类似解决方案呢？单一可执行文件，免去安装Python环境的麻烦，也避免了直接暴露源码程序。

经过多次搜索之后找到解决方案 [exxo](https://github.com/mbachry/exxo)

*注意：exxo只支持linux64平台*

<!--more-->

## 指路

### 安装
首先下载安装exxo
```bash
wget https://bintray.com/artifact/download/mbachry/exxo/exxo-0.0.7.tar.xz  # 下载 

tar xf exxo-0.0.7.tar.xz  # 解压

mv exxo /usr/local/bin   # 移动到可执行文件目录（可选）
```

### 创建环境
通过 exxo 创建一个python虚拟环境，用于编译我们的程序

```bash
exxo venv /tmp/myenv    # 创建环境
source /tmp/myenv/bin/activate   # 激活环境
```

### 编译程序
先写一个简单的程序: aa.py
```Python
import os

def main():
    os.system('ls -al')

if __name__ == '__main__':
    main()
```

再根据这个程序编写setup.py, 这一步是关键，不熟悉的同学可以去学习一下setuptools的语法。

```Python
#condig=utf8
from setuptools import setup, find_packages

requirements = [
    # 这里可以写上需要的依赖
    # 'setuptools',
]

setup(
    name='pyaa',   # 编译出的文件的名称
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=True,
    py_modules=[
        "aa",
    ],
    entry_points={  # python 生成可执行文件的入口
        'console_scripts': [
            'pyaa = aa:main',
        ]
    }
)
```

执行`exxo build`编译，生成文件`dist/pyaa`

最后，测试该文件，功能正常。
```
$ ./dist/pyaa
总用量 19348
drwxrwxr-x 4 ruan ruan     4096 3月   1 11:25 .
drwxrwxr-x 6 ruan ruan     4096 2月  29 11:48 ..
-rw-rw-r-- 1 ruan ruan       87 3月   1 11:14 aa.py
drwxrwxr-x 2 ruan ruan     4096 3月   1 11:26 dist
-rw-r--r-- 1 ruan ruan 19784872 8月  29 2016 exxo-0.0.7.tar.xz
drwxrwxr-x 2 ruan ruan     4096 3月   1 11:24 __pycache__
-rw-rw-r-- 1 ruan ruan      505 3月   1 11:25 setup.py
```

