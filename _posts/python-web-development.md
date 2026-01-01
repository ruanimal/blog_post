---

title: Python Web开发总结
date: 2019-09-28 09:48:00
updated: 2024-07-09 22:02:56
categories: 编程
tags: [Web, Python, Django]

---
## HTTP协议
### HTTP简介
HTTP协议是Hyper Text Transfer Protocol（超文本传输协议）的缩写。
用于从万维网（WWW:World Wide Web ）服务器传输超文本到本地浏览器的传送协议。

HTTP协议工作于客户端-服务端架构为上。
浏览器作为HTTP客户端通过URL向HTTP服务端即WEB服务器发送所有请求。
Web服务器根据接收到的请求后，向客户端发送响应信息。

![](https://image.ponder.work/mweb/2019-09-28-15299338545214.jpg)

#### 主要特点
- **无连接**：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。采用这种方式可以节省传输时间。

- **无状态**：HTTP协议是无状态协议。无状态是指协议对于事务处理没有记忆能力。缺少状态意味着如果后续处理需要前面的信息，则它必须重传，这样可能导致每次连接传送的数据量增大。另一方面，在服务器不需要先前信息时它的应答就较快。

<!--more-->

#### URL
- URI: 统一资源标识符（Uniform Resource Identifiers, URI）
- URL是一种特殊类型的URI

HTTP使用统一资源标识符（Uniform Resource Identifiers, URI）来传输数据和建立连接。URL是一种特殊类型的URI，包含了用于查找某个资源的足够的信息


### HTTP报文
#### 请求报文

HTTP 协议是以 ASCII 码传输，建立在 TCP/IP 协议之上的应用层规范。

规范把 HTTP 请求分为三个部分：状态行、请求头、消息主体。类似于下面这样：

```
<method> <request-URL> <version>
<headers>

<entity-body>
```
![](https://image.ponder.work/mweb/2019-09-28-15299956241673.jpg)

**GET请求**

`curl -XGET -H 'Content-type:application/json' 'http://127.0.0.1:5001/api/_echo?a=1&b=2' -d '{"test": 1, "USER": "qqhc_clac_user"}' `


请求报文
```
GET /api/_echo?a=1&b=2 HTTP/1.1
User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.7 libidn/1.18 libssh2/1.2.2
Host: 127.0.0.1:5001
Accept: */*
Content-type:application/json
Content-Length: 37

{"test": 1, "USER": "qqhc_clac_user"}
```

- 第1行, 请求行
- 第2到6行, 请求头部(headers), key: value 格式
- 第7行, 空行, 分割headers 和 body
- 第8行, 请求数据, 也叫主体(body)

注意: 这里的行与行之间的分隔符为 `\r\n`

**POST请求**


`curl -XPOST 'http://127.0.0.1:5001/api/_echo?a=1&b=2' -d 'c=3&d=4'  `

```
POST /api/_echo?a=1&b=2 HTTP/1.1
User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.7 libidn/1.18 libssh2/1.2.2
Host: 127.0.0.1:5001
Accept: */*
Content-Length: 7
Content-Type: application/x-www-form-urlencoded

c=3&d=4
```


#### 响应报文

```
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Tue, 26 Jun 2018 07:00:38 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 45

{
  "USER": "qqhc_clac_user",
  "test": 1
}
```

- 第1行, 状态行
- 第2到6行, 响应头部(headers), key: value 格式
- 第7行, 空行, 分割headers 和 body
- 剩下的其他行, 响应数据, 也叫主体(body)

### 响应状态码
HTTP之状态码

状态代码有三位数字组成，第一个数字定义了响应的类别，共分五种类别:

```
1xx：指示信息--表示请求已接收，继续处理
2xx：成功--表示请求已被成功接收、理解、接受
3xx：重定向--要完成请求必须进行更进一步的操作
4xx：客户端错误--请求有语法错误或请求无法实现
5xx：服务器端错误--服务器未能实现合法的请求
```

常见的状态码

* 200 OK 客户端**请求成功**
* 301 Moved Permanently 请求**永久重定向**
* 302 Moved Temporarily 请求**临时重定向**
* 304 Not Modified 文件未修改，可以直接使用缓存的文件。
* 400 Bad Request 由于客户端**请求有语法错误**，不能被服务器所理解。
* 401 Unauthorized **请求未经授权**。这个状态代码必须和WWW-Authenticate报头域一起使用
* 403 Forbidden 服务器收到请求，但是**拒绝提供服务**。服务器通常会在响应正文中给出不提供服务的原因
* 404 Not Found 请求的资源**不存在**，例如，输入了错误的URL
* 500 Internal Server Error 服务器发生不可预期的错误，导致无法完成客户端的请求。
* 503 Service Unavailable 服务器当前不能够处理客户端的请求，在一段时间之后，服务器可能会恢复正常。

### HTTP请求方法
HTTP1.1 版本

```
GET  请求指定的页面信息，并返回实体主体。
HEAD     类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头
POST     向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。
PUT  从客户端向服务器传送的数据取代指定的文档的内容。
DELETE   请求服务器删除指定的页面。
CONNECT  HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。
OPTIONS  允许客户端查看服务器的性能。
TRACE    回显服务器收到的请求，主要用于测试或诊断。
```

## Web的发展史
### 静态页面
在很久很久以前, 那时Web开发还比较简单，开发者经常会去操作web服务器，并且他会写一些HTML页面放到服务器指定的文件夹(/www)下。

这些HTML页面，就在浏览器请求页面时使用。
![](https://image.ponder.work/mweb/2019-09-28-15300002589684.jpg)

**常见Web服务器**
最常见的Web服务器有Apache和Nginx, 也是静态资源服务器.

问题就出现了，你只能获取到静态内容。
倘若你想让访问者看到有多少其他访问者访问了这个网站呢，或者倘若你想让访问者去填写这样一个表单，包含有姓名和邮件地址呢？

所以出现动态技术. 静态资源服务器可以直接处理静态页面, 并且将动态请求转发给CGI程序处理。

### 动态页面
![](https://image.ponder.work/mweb/2019-09-28-15300005473401.jpg)

## CGI
### 什么是CGI
`通用网关接口`（Common Gateway Interface/CGI）
CGI是动态网页的第一种解决方案. CGI协议描述了服务器和请求处理程序之间传输数据的一种标准。
遵循CGI协议的请求处理程序称为`CGI程序\脚本`

### CGI协议数据流

![](https://image.ponder.work/mweb/2019-09-28-15300044921863.jpg)


![企业微信截图_15300035568763](https://image.ponder.work/mweb/2019-09-28-%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_15300035568763.png)



### 一个简单的CGI脚本

```python
#!C:\\Python27\\python.exe
# coding=utf-8

import cgi
form = cgi.FieldStorage()
text = form.getvalue('text', open('simple_edit.dat').read())
f = open('simple_edit.dat', 'w')
f.write(text)
f.close()

print 'Content-type: text/html\r\n'

print '''<html>
  <head>
    <title>A Simple Editor</title>
  </head>
  <body>
    <form action='simple_edit.cgi' method='POST'>
    <textarea rows='10' cols='20' name='text'>%s</textarea><br />
    <input type='submit' />
    </form>
  </body>
</html>
''' % text
```

### CGI的发展
#### CGI局限性
- 伸缩性不是太好(经常是为每个请求分配一个新的进程)，
- 不太安全(直接使用文件系统或者环境变量)
- 功能十分有限：很难在CGI体系去对Web请求的控制，例如：用户认证等。

每当客户请求CGI的时候，WEB服务器就请求操作系统生成一个新的CGI解释器进程(如php-cgi.exe)，CGI 的一个进程则处理完一个请求后退出，下一个请求来时再创建新进程。

当然，这样在访问量很少没有并发的情况也行。可是当访问量增大，并发存在，这种方式就不适合了。于是就有了fastcgi。

#### FastCGI
FastCGI（快速通用网关接口），是CGI的增强版本。其目的在于，减少Web服务器与CGI程序之间交互的开销，使得服务器可以同时处理更多的请求。

FastCGI像是一个常驻(long-live)型的CGI，它可以一直执行着，只要激活后，不会每次都要花费时间去fork一次（这是CGI最为人诟病的fork-and-execute 模式）。

一般情况下，FastCGI的整个工作流程是这样的：

1. Web Server启动时载入FastCGI进程管理器（IIS ISAPI或Apache Module)
2. FastCGI进程管理器自身初始化，启动多个CGI解释器进程(可见多个php-cgi)并等待来自Web Server的连接。
3. 当客户端请求到达Web服务器时，Web服务器将请求通过socket方式转发到FastCGI主进程，主进程选择并连接到一个CGI解释器。Web服务器将CGI环境变量和标准输入发送到FastCGI子进程
4. FastCGI 子进程完成处理后将标准输出和错误信息从同一socket连接返回Web Server。当FastCGI子进程关闭连接时， 请求便告处理完成。
5. FastCGI子进程接着等待并处理来自FastCGI进程管理器(运行在Web Server中)的下一个连接。

**FastCGI的PHP实现**
- PHP-FPM

![](https://image.ponder.work/mweb/2019-09-28-15300123292497.jpg)


## WSGI
WSGI：全称是`Web Server Gateway Interface`，WSGI不是服务器，python模块，框架，API或者任何软件，只是一种**规范**，描述`web server`如何与`web application`通信的规范。

要实现WSGI协议，必须同时实现web server和web application，当前运行在WSGI协议之上的web框架有Torando, Flask, Django

WSGI server负责从客户端接收请求，将request转发给application，将application返回的response返回给客户端；

WSGI application接收由server转发的request，处理请求，并将处理结果返回给server。application中可以包括多个栈式的中间件(middlewares)，这些中间件需要同时实现server与application，因此可以在WSGI服务器与WSGI应用之间起调节作用：对服务器来说，中间件扮演应用程序，对应用程序来说，中间件扮演服务器。

WSGI协议其实是定义了一种server与application解耦的规范，即可以有多个实现WSGI server的服务器，也可以有多个实现WSGI application的框架，那么就可以选择任意的server和application组合实现自己的web应用。

例如uWSGI和Gunicorn都是实现了WSGI server协议的服务器，Django，Flask是实现了WSGI application协议的web框架，可以根据项目实际情况搭配使用。

WSGI将 web 组件分为三类： web服务器，web中间件,web应用程序， wsgi基本处理模式为

```
WSGI Server -> (WSGI Middleware)* -> WSGI Application
```

### WSGI Server
wsgi server可以理解为一个符合wsgi规范的web server，接收request请求，封装一系列环境变量，按照wsgi规范调用注册的wsgi app，最后将response返回给客户端。

![](https://image.ponder.work/mweb/2019-09-28-15300098402454.png)

### WSGI Application
wsgi application就是一个普通的callable对象，当有请求到来时，wsgi server会调用这个wsgi app。

```python
def application (environ, start_response):

    response_body = 'Request method: %s' % environ['REQUEST_METHOD']

    # HTTP响应状态
    status = '200 OK'

    # HTTP响应头，注意格式
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    # 将响应状态和响应头交给WSGI server
    start_response(status, response_headers)

    # 返回响应正文
    return [response_body]
```

### WSGI MiddleWare
有些功能可能介于服务器程序和应用程序之间，例如，服务器拿到了客户端请求的URL, 不同的URL需要交由不同的函数处理，这个功能叫做 URL Routing，这个功能就可以放在二者中间实现，这个中间层就是 middleware。

middleware对服务器程序和应用是透明的，也就是说，服务器程序以为它就是应用程序，而应用程序以为它就是服务器。

## Django简介
Django是一个开放源代码的Web应用框架，由Python写成。采用了MVT的软件设计模式，即模型Model，视图View和模板Template。

### Django的MVT模型

![](https://image.ponder.work/mweb/2019-09-28-15300114452163.png)


### 架构图

![](https://image.ponder.work/mweb/2019-09-28-15300116078473.jpg)

### 请求和响应

![](https://image.ponder.work/mweb/2019-09-28-15300116231124.jpg)


### 典型的目录结构

```
microapp
├── manage.py    # 程序启动入口
├── microapp    # 项目配置目录
│   ├── __init__.py
│   ├── dev_settings.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── translator   # web app, 可以有多个app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── interfaces.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

### 中间件
中间件的执行流程 (Django1.9 以后的版本)

1、执行完所有的request方法 到达视图函数。

2、执行中间件的其他方法

3、经过所有response方法 返回客户端。

注意：如果在其中1个中间件里 request方法里 return了值，就会执行当前中间件的response方法，返回给用户 然后 报错。。不会再执行下一个中间件。

![](https://image.ponder.work/mweb/2019-09-28-15308821801095.jpg)



一个简单的中间件

```python
# -*- coding:utf-8 -*-
"""获取真实用户ip"""

from django.utils.deprecation import MiddlewareMixin


class RemoteHostMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        m = request.META
        if m.get("HTTP_X_REAL_IP"):
            ip = m.get("HTTP_X_REAL_IP")
        elif m.get('HTTP_X_FORWARDED_FOR'):
            x_forwarded_for = m.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = m.get('REMOTE_ADDR')
        request.remote_host = ip

```

## 参考资料
1. https://hit-alibaba.github.io/interview/basic/network/HTTP.html
2. https://code.ziqiangxuetang.com/django/django-middleware.html
3. http://blog.jobbole.com/45170/
4. https://www.cnblogs.com/wanghetao/p/3934350.html



