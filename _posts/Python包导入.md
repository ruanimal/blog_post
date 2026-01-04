---
title: Python项目中包的导入
date: 2016-04-25 21:00:00
updated: 2020-09-28 10:13:00
categories: 编程
tags: [Python]
---

## 例子
```
taskman
├── db.sqlite3
├── manage.py
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

## 说明
上面的例子是一个Django项目，Python包的导入都是相对于`主程序`来说的。

这个项目的主程序就是`manage.py`，跟manage.py同级的文件夹（含有`__init__.py`）如`task`,`man`就称之为包，若同级有文件就称之为顶级模块。

在这个项目里所有Python包的导入，都应该写完整路径, 或者使用相对当前文件的相对路径。

例如在文件`taskman/task/views.py`中，想要导入`taskman/man/setting.py`，就得这样。
```python
## 绝对路径 import
from man.setting import some_setting
# or 
from man import setting
```

再例如, 在文件`taskman/task/views.py`中，想要导入`taskman/task/urls.py`，就得这样。
```python
## 绝对路径 import 
from task.urls import some_setting
# 或者
from task import urls

## 相对路径import
from .urls import some_setting
from . import urls
```

## 总结
1. 所有导入都是根据主程序的路径，然后从完整路径导入包，或者相应的相对路径导入。
2. 主程序应该位于包的最顶层，否则发生`ValueError: Attempted relative import in non-package`


