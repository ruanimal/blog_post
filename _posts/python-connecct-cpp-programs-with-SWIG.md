title: 使用SWIG实现Python调用c++
date: 2020-08-05 8:17 PM
categories: 编程
tags: [SWIG, Python, c++]

---

 **[SWIG](http://www.swig.org)** (Simplified Wrapper and Interface Generator) 是一个开源工具，用于让C/C++的程序和库可以被其他语言调用。
 
支持的非常多语言，有Lua, Perl, PHP, Python, R, Ruby, C#, Java, JavaScript, Go, Scheme 等。
<!--more-->
## 大致流程
1. 定义SWIG接口文件
2. 生成C/C++和目标语言的包装代码
3. 编译位置无关的C/C++包装代码和功能代码，并链接为动态库

![Untitled Diagram](media/Untitled%20Diagram.svg)

## c++示例代码
下面用到的C++代码

头文件
```c++
/* utils.h */
#ifndef _H_UTILS_H_
#define _H_UTILS_H_
#include <sstream>

using namespace std;
class Utils {
  public:
    Utils();
    string Float2String(float Num);
};

#endif
```

实现代码
```c++
/* utils.cpp */
#include "utils.h"

Utils::Utils() {}

string Utils::Float2String(float Num)
{
	ostringstream oss;
	oss<<Num;
	string str(oss.str());
	return str;
}
```

## SWIG 接口文件
```c
 /* example.i */
 %module model_engine
 %include "std_string.i"
 %{
 /* Put header files here or function declarations like below */
#include "utils.h"
 %}

%include "utils.h"
```

其中`%include "std_string.i"`, 实现了c++的string自动转python的str

## 生成动态库
```bash
swig -c++ -python  example.i
g++ -O2 -fPIC -std=c++0x -c utils.cpp
g++ -O2 -fPIC -std=c++0x -c example_wrap.cxx -I/usr/include/python3.8/
g++ -shared utils.o example_wrap.o -o _example.so
```

注意编译`example_wrap.cxx`时引入对应版本的python头文件，不同系统的路径可能有所不同。

## 使用
```
>>> import example
>>> ul = example.Utils()
>>> ul.Float2String(1.111)
'1.111'
```

## 参考
1. https://segmentfault.com/a/1190000013219667
2. http://www.swig.org/Doc4.0/SWIGDocumentation.html#Python