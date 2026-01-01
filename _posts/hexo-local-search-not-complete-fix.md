---
title: hexo 站内搜索内容不完全问题修复
date: 2021-10-11 20:00:00
updated: 2024-07-09 22:02:56
categories: 编程
tags: [XML,]

---
在使用 Hexo 的站内搜索时，发现搜索的内容不全。单步调试发现xml解析不完整，有部分内容被截断了。

在浏览器中打开[/search.xml](/search.xml)发现以下错误。显然xml中有非法字符，xml解析产生了错误。
<!--more-->
![](https://image.ponder.work/mweb/2021-10-12-16339770374988.jpg)

将search.xml文件保存，并用python打开，找到具体出错的位置。
utf8解码之后可以发现`\x10`非法字符，将其删除，重新生成文章问题解决。

```python
>>> xxx = open('./tmp.xml', 'rb').read()
>>> xxx.index(b'\x10\xE7\x84\xB6')
923278
>>> xxx[923278:923278+31]
b'\x10\xe7\x84\xb6\xe5\x88\x99\xef\xbc\x8c\xe4\xbb\x8a\xe4\xb9\x8b\xe4\xb8\x96\xe4\xba\xba\xef\xbc\x8c\xe7\xb1\xbb\xe6\xad\xa4'
>>> xxx[923278:923278+31].decode()
'\x10然则，今之世人，类此'
```

![](https://image.ponder.work/mweb/2021-10-12-16339793845815.jpg)
