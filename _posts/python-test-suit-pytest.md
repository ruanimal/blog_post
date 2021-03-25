title: 用Pytest测试Python代码
date: 2020-03-12 9:48 AM
categories: 编程
tags: [Python, Pytest]

--------

## 简介
pytest是一个非常成熟的全功能的Python测试框架, 简单灵活, 容易上手, 具有很多第三方插件，并且可以自定义扩展.

## 安装
```
pip install pytest
```

## 使用
### 简单例子
先写个测试代码`tmp.py`
```python
def add(a, b):
    return a + b

def test_add():
    assert add(1, 1) == 2

def test_add_fail():
    assert add(1, 2) == 2
```

使用方法
```
usage: py.test [options] [file_or_dir] [file_or_dir] [...]
```

<!--more-->

所以我们执行 `pytest tmp.py`

输出结果, 两个测试用例一个通过一个失败, 通过用绿色 <font color="green">.</font> 表示, 失败红色 <font color="red">F</font> 表示.
```
=============================== test session starts ===============================
platform darwin -- Python 3.6.9, pytest-5.2.0, py-1.8.0, pluggy-0.13.0
rootdir: /Users/ruan/projects
plugins: pylint-0.15.1, mypy-0.5.0, celery-4.3.0
collected 2 items

tmp.py .F                                                                   [100%]

==================================== FAILURES =====================================
__________________________________ test_add_fail __________________________________

    def test_add_fail():
>       assert add(1, 2) == 2
E       assert 3 == 2
E        +  where 3 = add(1, 2)

tmp.py:92: AssertionError
=========================== 1 failed, 1 passed in 0.10s ===========================
```

### 用例查找规则
测试用例目录优先级: `命令行参数目录 > 配置文件中的testpaths配置项 > 当前目录`

支持的配置文件: pytest.ini，tox.ini，setup.cfg

测试用例查找规则:
* 如果当前目录在包中, 则以该包的顶级目录作为工作目录(向上查找, 第一个不包含`__init__.py`的目录)
* 递归遍历目录，除非目录指定了不递归参数`norecursedirs`
* 在目录中查找匹配`test_*.py` 或者 `*_test.py` 的文件, 并以包名的全路径导入
* 查找以 `Test` 开头的类(该类不能有 init 方法), 的以`test`为前缀的方法.
* 查找以`test`为前缀的函数.

### 常用参数
```
pytest --fixtures, --funcargs  查看可用的 fixtures
pytest --markers                查看可用的 markers

# 失败后停止
pytest -x           首次失败后停止执行
pytest --maxfail=2  两次失败之后停止执行

# 调试输出
pytest -l, --showlocals  在 traceback 中显示本地变量
pytest -q, --quiet       静默模式输出
pytest -v, --verbose     输出更详细的信息
pytest -s                捕获输出, 例如显示 print 函数的输出
pytest --tb=style        错误信息输出格式
    - long    默认的traceback信息格式化形式
    - native  标准库格式化形式
    - short   更短的格式
    - line    每个错误一行

# 运行指定 marker 的测试
pytest -m MARKEXPR

# 运行匹配的测试(函数名称)
pytest -k stringexpr

# 只收集并显示可用的测试用例，但不运行测试用例
pytest --collect-only

# 失败时调用 PDB
pytest --pdb
```

**使用示例**
* 执行单个模块中的全部用例: `py.test test_mod.py`

* 执行指定路径下的全部用例: `py.test somepath`

* 执行匹配`stringexpr`表达式的用例: `py.test -k stringexpr`

* 运行指定模块中的某个用例: `pytest test_mod.py::test_func`

* 运行某个类下的某个用例: `pytest test_mod.py::TestClass::test_method`

* 执行测试用例时输出print内容: `pytest -s test_mod.py`


### 编写测试用例
#### 断言
```
import pytest

# 简单断言
assert 1 + 1 == 2

# 断言发生异常
with pytest.raises(ZeroDivisionError):
    1 / 0
```

#### Fixtures
`fixture` 是 pytest 特有的功能，它用 pytest.fixture 标识，定义在函数前面, 起到依赖注入的作用.

在编写测试函数的时候，可以将此函数名称做为传入参数，pytest 将会以依赖注入方式，将该函数的返回值作为测试函数的传入参数。

```python
import pytest

# fixtures documentation order example
order = []

@pytest.fixture(scope="session")
def s1():
    order.append("s1")

@pytest.fixture(scope="module")
def m1():
    order.append("m1")

@pytest.fixture
def f1(f3):
    order.append("f1")

@pytest.fixture
def f3():
    order.append("f3")

@pytest.fixture(autouse=True)
def a1():
    order.append("a1")

@pytest.fixture
def f2():
    order.append("f2")

def test_order(f1, m1, f2, s1):
    assert order == ["s1", "m1", "a1", "f3", "f1", "f2"]
```

fixture接收`scope`和`autouse`参数
不同的scope表明了fixture的作用访问和执行先后顺序, 以下fixture执行顺序从上到下依次执行. 同级别是fixture按照依赖关系决定先后次序.
autouse参数决定了fixture是自动执行, 还是在被用做参数传入时才执行

- `scope='session'`: 会话级别, 测试开始时执行一次, 在整个测试的过程不变
- `scope='module'`: 模块级别, 每个模块测试开始时执行一次, 在整个模块测试的过程不变
- `scope='function', autouse=True`: 函数级别, 在每个函数开始前自动执行.
- `scope='function'`: 函数级别(默认是这个级别).

#### setUp & tearDown
`setup\teardown` 是指在模块、函数、类开始运行以及结束运行时执行一些动作。

例如: 数据库连接管理, 临时文件清理.

pytest支持的`setup\teardown`钩子

```python
# 模块级别
def setup_module(module):
    pass

def teardown_module(module):
    pass

# 类级别
class TestA:
	@classmethod
	def setup_class(cls):
	    pass

	@classmethod
	def teardown_class(cls):
	    pass

	# 方法级别
	def setup_method(self, method):
	    pass

	def teardown_method(self, method):
	    pass

# 函数级别
def setup_function(function):
    pass

def teardown_function(function):
    pass

# 会话级别
def pytest_sessionstart(session):
    # setup_stuff

def pytest_sessionfinish(session, exitstatus):
    # teardown_stuff
```

以上这些钩子, 也都可以用 fixture 的方式等效实现, 例如：

```python
@fixture(scope='session', autouse=True)
def my_fixture():
    # setup_stuff
    yield
    # teardown_stuff
```

#### conftest.py
从广义理解，`conftest.py` 是一个本地的 `per-directory` 插件，在该文件中可以定义目录特定的 hooks 和 fixtures。

`pytest` 框架会在它测试的项目中寻找 conftest.py 文件，然后在这个文件中寻找针对整个目录的测试选项.

总结起来，`conftest.py` 文件大致有如下几种功能：

* **Fixtures:** 用于给测试用例提供静态的测试数据，其可以被所有的测试用于访问，除非指定了范围

* **加载插件:** 用于导入外部插件或模块:
```
pytest_plugins ="myapp.testsupport.myplugin"
```

* **测试根路径:** 如果将 conftest.py 文件放在项目根路径中，则 pytest 会自己搜索项目根目录下的子模块，并加入到 sys.path 中，这样便可以对项目中的所有模块进行测试，而不用设置 PYTHONPATH 来指定项目模块的位置。

#### Markers

`marker` 的作用是，用来标记测试，以便于选择性的执行测试用例。

Pytest 提供了一些内建的 marker, 这里列了几个个人觉得有用的, 详细的请看[文档](https://docs.pytest.org/en/latest/mark.html)
```
# 跳过测试
@pytest.mark.skip(reason=None)

# 满足某个条件时跳过该测试
@pytest.mark.skipif(condition)

# 让测试尽早地被执行
@pytest.mark.tryfirst

# 让测试尽量晚执行
@pytest.mark.trylast
```

例子:
```python
# 如果是window平台, 跳过该测试用例
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

也可以自定义markers, 这些markers只是具有名称, 只起了标记作用, 通过`-m`参数执行指定的marker的测试用例.

例如`pytest -m hello`, 只执行test_one测试用例
```python
@pytest.mark.hello
def test_one():
    assert False

@pytest.mark.world
def test_two():
    assert False
```

### 插件
通过pip安装, 例如pylint插件
```
pip install pytest-pylint
```

通过添加参数来使用插件
```
pytest --pylint tmp.py
```

常用插件
* pytest-randomly: 测试顺序随机
* pytest-xdist: 分布式测试
* pytest-cov: 生成测试覆盖率报告
* pytest-pep8: 检测代码是否符合 PEP8 规范
* pytest-pylint: 检测代码风格和错误
* pytest-html: 生成 html 报告
* pytest-rerunfailures: 失败重试
* pytest-timeout: 超时测试
* pytest-mypy: type hints 检查

### 配置文件
可以在项目根目录放置`pytest.ini`来控制pytest的行为

例如:
```
[pytest]
addopts = --pylint --mypy ; 指定默认追加的参数
; testpaths = /home/test/ ; 测试用例路径
; minversion = 1.1 ; 依赖的pytest的最低版本
; norecursedirs = xx ; 不搜索测试用例的路径
; console_output_style ; 控制台测试报告格式
; 记录测试用例中用到的markers, 通过--markers参数可以显示出来
; markers =
;   webtest:  Run the webtest case
;   hello: Run the hello case
```

## 参考
1. https://docs.pytest.org/en/latest/
2. http://blog.konghy.cn/2018/05/08/pytest/
3. https://www.jianshu.com/p/a613a3a4d030

