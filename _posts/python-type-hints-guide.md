title: Python 类型标记(Type Hints) 初探
date: 2020-03-11 9:48 AM
categories: 编程
tags: [Python, ]

-------

## 缘起
Python是一门动态强类型语言, 动态性是它鲜明的特点. 

但是动态性在给程序员充分的自由的同时, 也带来了一些不好的负面效应. 特别是在团队协作的时候, 不好的队友会引发许多难以定位的问题.

同时动态性也大大削弱了ide的作用, 代码提示, 重构等一些功能远不如静态语言来得可靠.

```Python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def introduce_someone(person):
    print('{} is {} years old'.format(person.name, person.age))
```

比如这个代码片段, ide很难准确识别`introduce_someone`的参数应该是`Person`类的实例, 它只能单纯地从文本上分析, 并把所有可能的单词都提示出来. 

而且当调用`introduce_someone`, 传入了不合适的对象, 也很难通过静态检查发现.

类型标记的出现就解决了这些问题.

<!--more-->

## 性空
**类型标记**就是, 给变量, 参数, 函数附加上类型信息. 类似Java等静态语言的变量声明信息.

Python 从3.5开始, 引入了类型标记系统, 并在后面的版本有所增强.

类型标记的基本语法 `变量名: 标记`, 标记可以是字符串, 对象或者`Type aliases`(类型别名)

### 变量类型标记
```Python
name: str = 'tom'
age: 'int' = 42
```

### 函数类型标记
```Python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

def introduce_someone(person: 'Person') -> None:
    print('{} is {} years old'.format(person.name, person.age))

introduce_someone('fuck')
```

函数的类型标记比变量多了一项: **返回值**, 通过`->`与函数名连接在一起.

如果调用`introduce_someone`, 参数不是`Person`类的实例. 静态检查会发现以下错误.
```
error: Argument 1 to "introduce_someone" has incompatible type "str"; expected "Person"
Found 1 error in 1 file (checked 1 source file)
```

### mypy
[mypy](http://mypy-lang.org/) 实用工具是一款针对 Python 的静态类型检查程序, 也可以和pytest一起配合使用.

#### 安装
```
pip install mypy
```

#### 执行检查
```bash
mypy my_program.py my_src_folder
```

### typing库
Python内置typing库提供了许多有用的工具来辅助类型标记

#### 类型别名 Type aliases
类型别名(运行时的标识函数), 帮助更好地进行类型标记, 这些别名可以进行组合.

```python
from typing import List, Dict, Tuple, Sequence

Vector = List[float]   # [float, float, ...]
ConnectionOptions = Dict[str, str]  # {str: str, ...}
Address = Tuple[str, int]  # (str, int)
Server = Tuple[Address, ConnectionOptions]  # ((str, int), {str: str, ...})

def print_vector(v: Vector):
    for i in v:
        print(i)

def print_connectionoptions(c: ConnectionOptions):
    for k, v in c.items():
        print(k, v)

def print_address(a: Address):
    print('{}:{}'.format(a[0], a[1]))

print_vector(['1', 1])
print_connectionoptions({'a': 1})
print_address(['127.0.0.1', 22])
```

静态检查结果, 三个调用错误都发现了
```
error: List item 0 has incompatible type "str"; expected "float"
error: Dict entry 0 has incompatible type "str": "int"; expected "str": "str"
error: Argument 1 to "print_address" has incompatible type "List[object]"; expected "Tuple[str, int]"

Found 3 errors in 1 file (checked 1 source file)
```

#### NewType
使用 NewType() 辅助函数创建派生的类型标记.
静态类型检查器会将新类型视为它是原始类型的子类, 可用于发现逻辑错误(比如: 虽然都是数字, 其实含义不同)

```python
from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)

def get_user_name(user_id: UserId) -> str:
    ...

# pass typechecks
user_a = get_user_name(some_id)

# does not pass typecheck; an int is not a UserId
user_b = get_user_name(-1)
```

#### Callable
标记为可调用对象, 期望特定签名的回调函数的框架可以将类型标注为 Callable[[Arg1Type, Arg2Type], ReturnType]。

例如:
```python
from typing import Callable

def feeder(get_next_item: Callable[[], str]) -> None:
    # Body

def async_query(on_success: Callable[[int], None],
                on_error: Callable[[int, Exception], None]) -> None:
    # Body
```

#### TypeVar
通过TypeVar来定义一个泛型类型标记, 限制对象的可选类型

```
from typing import TypeVar

T = TypeVar('T')  # Can be anything
A = TypeVar('A', str, bytes)  # Must be str or bytes
```

#### Any 类型
Any 是一种特殊的类型。

静态类型检查器将所有类型视为与 Any 兼容，反之亦然， Any 也与所有类型相兼容。

所有返回值无类型或形参无类型的函数将隐式地默认使用 Any 类型(没有类型标记的代码, 模式标记就是Any)

```python
from typing import Any

a = None    # type: Any
a = []      # OK
a = 2       # OK

s = ''      # type: str
s = a       # OK

def foo(item: Any) -> int:
    # Typechecks; 'item' could be any type,
    # and that type might have a 'bar' method
    item.bar()
    ...
```

