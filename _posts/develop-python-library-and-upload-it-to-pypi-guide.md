title: 开发Python库并发布到PyPI指南
date: 2020-09-10 8:03 PM
categories: 编程
tags: [PyPI, Python]

---

## PyPI
[PyPI](https://pypi.org/)（英语：Python Package Index，简称PyPI）是一个用于存储Python写成的软件包的软件存储库，我们平时用pip安装的库就是来自于PyPI

而且，通过PyPI我们可以把自己写的库代码分享给别人，这也是开源的乐趣之一。
<!--more-->

## 用到的库代码

```
├── MANIFEST.in
├── README.md
├── dingtalk_log_handler
│   ├── __init__.py
├── setup.py
```
整体代码结构，其中[dingtalk_log_handler](https://github.com/ruanimal/dingtalk-log-handler)是我写的一个用于发日志到钉钉群的库，也是这次要发布的库。

先看下库的主体代码`dingtalk_log_handler/__init__.py`, 由于功能比较简单，逻辑就都写在`__init__.py`里了

```python
import base64
# 其他import略去

__author__ = 'ruan.lj'
__version__ = '0.0.2'
__all__ = (
    'OAPI_DOMAIN',
    'DingTalkHandler',
)

OAPI_DOMAIN = 'oapi.dingtalk.com'   # dingtalk open api domain

class DingdingApiError(RuntimeError):
    pass

class DingTalkHandler(logging.Handler):
    """Handler for logging message to dingtalk"""
    pass
    # 略去逻辑代码
```

## 编写 setup.py
setup.py指引了打包工具如何打包我们的库，功能与类似Makefile

```python
from setuptools import setup, find_packages
from dingtalk_log_handler import __author__, __version__

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dingtalk-log-handler',
    version=__version__,
    author=__author__,
    author_email='xxx@foxmail.com',
    description='log handler for send message to dingtalk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        # 省略一下
    ],
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[],
    project_urls={
        'Source': 'https://github.com/ruanimal/dingtalk-log-handler',
    },
)
```

具体打包的功能由`setuptools.setup`函数实现，我们只需要修改对应的参数即可

这些参数影响打包的行为，以及在PyPI页面上显示的信息

主要的参数说明，详细信息参考[文档](https://packaging.python.org/guides/distributing-packages-using-setuptools)
- name: 库名，也就是`pip install xxx`时的名称
- version: 版本，我们这里是复用了库代码里的版本号
- author: 作者，同上
- author_email: 作者邮箱
- description: 库说明，在`pip search xxx`的时候可以看到
- long_description: 库详细说明，显示在PyPI完整上，我们这里从`README.md`文件中读取具体内容
- long_description: 库详细说明的格式，这里使用markdown
- classifiers: 库的类别信息，[所有可选值参考](https://pypi.org/classifiers/)
- packages: 库包含的python包，通过find_packages自动添加
- py_modules: 库包含的顶级Python模块，我们这里没有
- python_requires: 支持的Python版本
- install_requires: 依赖的其他库，格式与`pip freeze`输出的格式相同
- project_urls: 项目的一些链接信息，[可选值列表](https://packaging.python.org/guides/distributing-packages-using-setuptools/?#project-urls)

## 编写 MANIFEST.in
打包时默认只会包含包代码和一些必要的文件，见[列表](https://packaging.python.org/guides/using-manifest-in/#how-files-are-included-in-an-sdist)
如果要包含其他资源文件，必须编写`MANIFEST.in`来说明说明

MANIFEST.in
```
include README.md
recursive-include dingtalk_log_handler *
global-exclude __pycache__
global-exclude tmp
global-exclude *.py[co]
```

语法和shell的通配符语法类似
- `include <pattern> <pattern2> ...`: 包含项目根目录匹配通配符的文件
- `recursive-include <dir-pattern> <pattern> <pattern2> ...`: 递归地包含指定目录匹配通配符的文件
- `global-exclude <pattern> <pattern2> ...`: 递归地排除匹配通配符的文件


## 打包
执行: `pip3 install wheel && python3 setup.py sdist bdist_wheel`

输出文件
```
dist
├── dingtalk-log-handler-0.0.2.tar.gz
└── dingtalk_log_handler-0.0.2-py3-none-any.whl
```

## 上传
我们可以通过[PyPI的测试站点](https://test.pypi.org) 来练习库文件的上传，并测试效果

1. [注册账户](https://test.pypi.org/account/register/)
2. 安装上传工具：`pip install twine -U`
3. 上传文件：`twine upload --repository testpypi dist/*`

熟悉流程之后，就可以换成[正式站点](https://pypi.org)，指定正式仓库(--repository pypi)上传文件

这样全世界的人都能看到你的库了。

## 效果
可以在[这里](https://pypi.org/project/dingtalk-log-handler/)找到我这次上传的库

可以看到 setup.py 文件里的很多信息会对应体现在PyPI网页上
![](https://image.ponder.work/mweb/2020-09-11-15997969319299.jpg)

## 参考
1. https://packaging.python.org/guides/distributing-packages-using-setuptools
2. https://packaging.python.org/guides/using-manifest-in/
