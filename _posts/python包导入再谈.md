title: python包导入再谈
date: June 22, 2016 7:26 PM
categories: 编程
tags: [Python, ]

----

## python包导入机制
包是指含有`__init__.py`的文件夹，模块就是一个.py文件。

**python的包和模块是先查找`buil-in moudle`然后是`sys.path`这个list里的所有路径。**
- sys.path[0]是启动Python解释器的脚本所在路径
    - 比如运行`python task/admin.py`，sys.path[0]是`'/home/code/taskman/task'`
    - 启动脚本是符号链接时，`sys.path[0]`是实际文件所在路径，[详见](#符号链接的情况)
    - 如果启动的是python解释器，如idle,ipython等，sys.path[0]是`''`。
- 如果sys.path[0]是`''`，这个值等于当前工作目录也就是`os.getcwd()`的值，也就是linux的pwd的值，你可以用`os.chdir`来改变工作路径。
- sys.path里余下的元素是python环境变量里的一些路径


还是分析之前的那个例子

<!--more-->
```
taskman
    ├── db.sqlite3
    ├── manage.py
    ├── requirement.txt
    ├── task
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    └── man
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```


```python
# task/admin.py 文件
from man.setting import some_setting

some_setting()

if __name__ == '__main__':
    print 'something'
```

## 工作路径的影响
### 当前路径是 `taskman`
假如我们要直接运行`task/admin.py`这个文件，直接`python task/admin.py`，会抛出`ImportError`。

直接`python task/admin.py`，此时的sys.path[0]应该是`'/home/code/taskman/task'`，此时task/admin.py所需的man.setting显然不在`task`目录下，自然就是`ImportError`。
这时如果往admin.py加入`sys.path.append('/home/code/taskman')`语句，就可以把`man`这个包所在目录加入到sys.path，这样就解决了。

也可以使用`python -m task.admin` 将admin.py当作一个模块来执行，此时sys.path[0]是当前工作目录`/home/code/taskman`，所以一切正常。

### 当前路径不是 `taskman`
运行`python -m task.admin`会提示`No module named task`，因为在那个目录下找不到`task`这个包。

此时只能在脚本前部添加一下语句
```python
import os, sys
os.chdir('/home/code/taskman/task')`
sys.path.append('/home/code/taskman')
```

这样在这个脚本的包导入正常，同时还可以通过`os.system('python -m task.models')`运行项目内其他模块，而不用管当前工作目录在那里。

还有一个霸道的解决方法是，通过`export PYTHONPATH="/home/code/taskman"`将项目路径，添加到python环境变量里，这样当解释器启动时项目路径就会直接添加到sys.path中。不过这样会影响整个python环境，可能出现包重名。

当然还可以在Python的site-packages目录下新建一个`some.pth`文件，把需要的路径往里面写，这样每一个Python解释器进程的sys.path都会包含这个目录。可能会影响其他用户的程序，不推荐使用。

## 符号链接的情况
当Python程序的入口文件是符号链接时`sys.path[0]`是实际文件所在路径，所以可能会出现找不到模块的情况。
```bash
➜ tree
.
├── aa.py -> abc/aa.py
├── abc
│   └── aa.py
└── b.py

1 directory, 3 files

➜ cat abc/aa.py
import sys

print(sys.path)
abc=1
from b import *

➜ cat b.py
b=2

➜ python aa.py
['/private/tmp/tmp1/abc', 
'/Users/ruan/.pyenv/versions/3.8.7/lib/python38.zip', 
'/Users/ruan/.pyenv/versions/3.8.7/lib/python3.8', 
'/Users/ruan/.pyenv/versions/3.8.7/lib/python3.8/lib-dynload', 
'/Users/ruan/.pyenv/versions/3.8.7/lib/python3.8/site-packages']
Traceback (most recent call last):
  File "aa.py", line 5, in <module>
    from b import *
ModuleNotFoundError: No module named 'b'
```

## 总结
1. Python模块和包的搜索路径由`sys.path`列表决定
2. Python会将启动脚本所在路径加入到`sys.path[0]`, 也就是`python /home/a/b/c.py`的`sys.path[0]`是`/home/a/b/`
3. Python执行加`-m`参数，会将工作路径加入到`sys.path[0]`, 也就是 `python -m a.b.c`的`sys.path[0]`是`/home`
4. 环境变量`PYTHONPATH`，`some.pth`文件会影响`sys.path`列表
5. sys.path中，空路径`''`总是等效于当前工作路径, 也就是`os.chdir`改变而改变。