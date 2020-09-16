title: 使用line_profiler分析Python程序耗时情况
date: 2020-09-15 9:48 PM
categories: 编程
tags: [Python, ]

-------

## 缘起
最近发生了一个服务故障，在一个同事对日志服务做了改动后，服务的耗时就变大了很多，数据大量积压。
通过观察监控报表，我们发现从他的改动上线后，服务器的CPU使用率大幅增加，基本处于满载状态。
粗略审查代码并没有发现问题，我们只能紧急回滚了服务，日志消费也恢复到正常状态了。
但是根本问题还没有找到，所以我请出了line_profiler来分析程序的具体耗时情况。

[line_profiler](https://github.com/pyutils/line_profiler)是个代码耗时分析器，可以逐行分析代码的耗时情况。
<!--more-->

## 使用
line_profiler包含两个部分
- kernprof：代码执行和耗时记录
- line_profiler：耗时报告解析和展示

首先，安装：`pip install line_profiler -U`

给需要分析的代码加上`@profile`装饰器, `@profile`装饰器不需要被import，kernprof在运行时会注入依赖，kernprof会记录被装饰函数的耗时情况，有多个函数也可以都加上装饰器。
```python
@profile
def main(run_type):
    with open('data.txt','r') as f:
        data=f.readline()
    input_data = json.loads(data)
    source = input_data.get('source', '')
    service = input_data.get('service', 0)
    apply_no = input_data.get('applyNo', 0)
    info = input_data.get('info', '')

    cust_no = input_data.get('cust_no', 0)
    job.run(source, service, apply_no, info, run_type)
```

然后，运行代码：`kernprof -l service.py`, 统计耗时情况, 执行完成后生成耗时报告文件`service.py.lprof`

最后，耗时报告解析：`python -m line_profiler service.py.lprof`，会生成可阅读的耗时报告。

## 分析
耗时报告示例
```
Timer unit: 1e-06 s

Total time: 4.18908 s
File: service.py
Function: main at line 38

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    38                                               @profile
    39                                               def main(run_type):
    40         1         45.0     45.0      0.0          with open('data.txt','r') as f:
    41         1        517.0    517.0      0.0              data=f.readline()
    42         1       6564.0   6564.0      0.2          input_data = json.loads(data)
    43         1         20.0     20.0      0.0          source = input_data.get('source', '')
    44         1          6.0      6.0      0.0          service = input_data.get('service', 0
    45         1          5.0      5.0      0.0          apply_no = input_data.get('applyNo', 
    46         1          5.0      5.0      0.0          info = input_data.get('info', '')
    47
    48         1          1.0      1.0      0.0          cust_no = input_data.get('cust_no', 0)
    49                                                   
    50         1    4181914.0 4181914.0     99.8         job.run(source, service, apply_no, info, run_type)
```

耗时报告会逐行显示代码耗时和调用情况
- Timer unit: 耗时单位，这里是微秒
- Total time：总耗时
- Line #：行号
- Hits：函数被调用次数
- Time：函数总耗时
- Per Hit：函数每次调用耗时
- % Time：耗时占比

可以看到，总耗时4.18908秒，`job.run`占用了`99.8%`的时间。

接下来我们分析下`job.run`的耗时情况
```
Timer unit: 1e-06 s

Total time: 4.16909 s
File: job.py
Function: inout at line 69

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    69                                               @profile
    70                                               def run(self, apply_no, info, req_type, run_type):
    ... 省略部分逻辑
   112         1          2.0      2.0      0.0          if req_type == 'credit':
   113         1    3370673.0 3370673.0     80.8              sql = db_utils.generate_sql(info1, sql, val, columns)
   114                                                   else:
   115                                                       sql = db_utils.generate_sql(info1, sql, val, columns)
   116         1       6948.0   6948.0      0.2          safe3_db.executor(sql)
```

可以看到，113行的生成SQL语句占用了80%的时间，SQL反倒不怎么耗时，显然是不正常的。

再看下`db_utils.generate_sql`函数的具体代码
可以发现遍历字段列表(item_list)的时候，调用了`get_json_value`，该函数每次都会调用`copy.deepcopy`。
众所周知，对象的深拷贝是十分消耗cpu资源的，并且这里深拷贝的次数会随着字段数的增加而线性增长。

把深拷贝行为去除后，服务耗时和cpu占用都回归到了正常水准。

```python
def generate_sql(info, sql, val, item_list):
    index = 0
    length = len(item_list)
    for item in item_list:
        index += 1
        buf = get_json_value(info,item)
        if index < length:
            sql = sql + ', `' + str(item) + '`'
            val = val + ', \'' + MySQLdb.escape_string(str(buf)) + '\''
        else:
            sql = sql + ', `' + str(item) + '`) '
            val = val + ', \'' + MySQLdb.escape_string(str(buf)) + '\')'
    return sql + val

def get_json_value(js,term):
    tsplit=term.split('|')
    result=''
    buf=copy.deepcopy(js)
    # 省略逻辑代码
    return value
```
