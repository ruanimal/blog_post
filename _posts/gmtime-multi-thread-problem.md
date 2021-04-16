title: gmtime 在多线程环境使用引发的 bug
date: 2021-04-15 9:48 PM
categories: 编程
tags: [C++]

----

话接[上文](/2021/03/25/xgboost-multi-thread-problem-debug-and-fix/)，还是这个 C++ 模型服务，在并发请求的情况下，大概有0.01%的请求部分模型分数不对。定位这种问题，对一个Python程序员来说，真是苦手。还好，经过调整代码不断测试，最终完美解决了问题。

<!--more-->

## 线程安全

对比数据，可以发现和请求中的某个时间字段有关。关键逻辑代码如下，主要是一个时间差的计算。
```cpp
// string date_str = "2019-01-01 00:00:00";
// string date_appl = "2012-01-01 00:00:00";
double test_a(string& date_str, string& date_appl, tm& tm_appl) {
    stringstream ss(date_str.substr(0,10));
    int date_sec;
    ss >> date_sec;  // stringstream to int 
    time_t ts_date_1 = date_sec + 8*3600;
    tm* tm_date = gmtime(&ts_date_1);  // timestemp to tm 
    tm_date->tm_hour = 0;
    tm_date->tm_min = 0;
    tm_date->tm_sec = 0;
    double seconds = difftime(mktime(&tm_appl), mktime(tm_date)); // diff timestemp
    return seconds;
}
```

根据之前的经验，肯定是该函数内部某些操作非线程安全的, 通过google搜索（关键词: gmtime thread safe）和询问朋友，得到以下信息。
- stringstream to int: 这里date_sec变量不存在竞争条件，所以安全
- gmtime: 不安全
- mktime: 时区不变的情况下安全
- difftime: 安全

bug应该是来自`gmtime`，该函数返回的是tm结构体指针，指向的是一个 static 结构体，所以不是线程安全，可以用`gmtime_r`函数替换。

修改之后
```cpp
double test_a(string& date_str, string& date_appl, tm& tm_appl) {
    stringstream ss(date_str.substr(0,10));
    int date_sec;
    ss >> date_sec;  // stringstream to int 
    time_t ts_date_1 = date_sec + 8*3600;
    tm tm_date;
    gmtime_r(&ts_date_1, &tm_date);
    tm_date.tm_hour = 0;
    tm_date.tm_min = 0;
    tm_date.tm_sec = 0;
    double seconds = difftime(mktime(&tm_appl), mktime(&tm_date));
}
```

经过测试，bug得以解决。但是同时发现一个问题，程序的qps下降了1/3。

## QPS下降
编程测试代码测试对比`gmtime_r`和`gmtime`耗时上并没有显著差别。而且如果不调用`gmtime_r`只声明`tm tm_date`，qps也是一样下降。

考虑到这个函数，在服务中调用次数比较多，而且自动变量的栈空间在函数调用时就会分配, tm结构体又比较大，应该对耗时有影响。

尝试修改`tm tm_date`为`static tm tm_date`静态分配内存, qps恢复正常了。
但是由于我们需要在多线程环境中使用，最终修改为`static thread_local tm tm_date`。

## 参考
* https://man7.org/linux/man-pages/man3/gmtime.3p.html#DESCRIPTION
* https://stackoverflow.com/questions/18355101/is-standard-c-mktime-thread-safe-on-linux#answer-18355323
* https://man7.org/linux/man-pages/man3/difftime.3.html#ATTRIBUTES
* https://softwareengineering.stackexchange.com/questions/195385/understanding-stack-frame-of-function-call-in-c-c#answer-195406