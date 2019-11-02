title: python包导入再谈
date: June 22, 2016 7:26 PM
categories: 编程
tags: [Python, ]

----

### python包、模块导入的顺序
包是指含有`__init__.py`的文件夹，模块就是一个.py文件。
**python的包和模块是先查找`buil-in moudle`然后是`sys.path`这个list里的所有路径。**
- sys.path[0]是启动Python解释器的脚本所在路径，比如运行`python task/admin.py`，sys.path[0]是`'/home/code/taskman/task'`；如果启动的是是idle,ipython等，sys.path[0]是`''`。
- 如果sys.path[0]是`''`，这个值等于当前工作目录也就是`os.getcwd()`的值，也就是linux的pwd的值，你可以用`os.chdir`来改变工作路径。
- sys.path里余下的元素是python环境变量里的一些路径


还是分析之前的那个例子

<!--more-->
```
/home/code/taskman
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

### 当前路径是`/home/code/taskman`
假如我们要直接运行`task/admin.py`这个文件，直接`python task/admin.py`，会抛出`ImportError`。

直接`python task/admin.py`，此时的sys.path[0]应该是`'/home/code/taskman/task'`，此时task/admin.py所需的man.setting显然不在`task`目录下，自然就是`ImportError`。这时如果往admin.py加入`sys.path.append('/home/code/taskman')`语句，就可以把`man`这个包所在目录加入到sys.path，这样就解决了。

也可以使用`python -m task.admin` 将admin.py当作一个模块来执行，此时sys.path[0]是`''`代表当前工作目录，而我们此时工作目录是`/home/code/taskman`，所以一切正常。

### 当前路径不是`/home/code/taskman`
运行`python -m task.admin`会提示`No module named task`，因为在那个目录下找不到`task`这个包。

此时只能在脚本前部同时添加`os.chdir('/home/code/taskman/task')`和`sys.path.append('/home/code/taskman')`，这样在这个脚本包的导入正常，同时可以通过`os.system('python -m task.models')`运行项目内其他模块，而不用管当前工作目录在那里。

总之，**如果`sys.path[0]`是一个具体的脚本路径，`os.chdir()`是不能对脚本内部包模块的导入产生影响，但是如果`sys.path[0]`是`''`，`os.chdir`可以影响包的导入。**

还有一个霸道的解决方法是，通过`export PYTHONPATH="/home/code/taskman"`将项目路径，添加到python环境变量里，这样当解释器启动时项目路径就会直接添加到sys.path中。不过这样会影响整个python环境，可能出现包重名。

当然还可以在Python的site-packages目录下新建一个`some.pth`文件，把需要的路径往里面写，这样每一个Python解释器进程的sys.path都会包含这个目录。可能会影响其他用户的程序，不推荐使用。
