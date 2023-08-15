title: 跨域的那些事
date: 2023-08-15 15:00
categories: 编程
tags: [Web]

----

- 什么是跨域？
	- 就是当前域访问了非本域的资源。对于http来说，url代表资源，也就是访问了非本域的url。
<!--more-->
- 域的定义是啥？
	- 这里的域，也就是同源策略（Same-origin policy）中的源。
	- 如果两个 URL 的协议、端口和主机都相同的话，则这两个 URL 是同源的。
- 为什么要限制跨域请求？
	- 导致目标域信息泄露
		- 如高仿淘宝站点，诱导登陆，获取用户密码。
		- js直接读取浏览器的目标域的sessionid、cookie
		- CSRF，如img标签的src会被访问
	- 导致当前域信息泄露
		- XSS跨站脚本(Cross-site scripting)注入，导致用户在当前域的信息泄露
			- 一般是接受了用户构造的输入，输入里包含恶意脚本内容，内容未被转义，又输出在页面上，从而被执行
- 怎么限制跨域？浏览器的同源策略
	- 禁止的
		- DOM 同源策略： 不同源的dom之间不能相互操作，多个iframe的情况
		- XMLHttpRequest 同源策略： 禁止请求不同源url
		- Cookie、LocalStorage、IndexedDB 等存储性内容同源策略
	- 允许的
		- 页面中的链接，重定向以及表单提交
		- `<script>、<img>、<link>`这些包含 src 属性的标签可以加载跨域资源。（只能GET）
- 限制跨域导致哪些不便？
	- 前后端分离开发时，localhost不能正常访问后端资源
	- 一些公共的api不能被访问
	- https的页面的http的静态资源，不能加载
- 如何绕过同源策略？
	- 浏览器启动参数（在用户端操作）
	- 反向代理（在当前域操作）
	- JSONP（在目标域操作）
		- 利用`<script>`允许跨域的特点，设置标签的src为目标域，动态生成需要的javascript内容
	- 跨源资源共享（CORS）（目标域操作）
		- 设置相应的reponse header
		  ```
		  Access-Control-Allow-Origin: https://foo.example  // 所允许的来源域
		  Access-Control-Allow-Methods: POST, GET, OPTIONS   // 所允许的请求方法
		  Access-Control-Allow-Headers: X-PINGOTHER, Content-Type  // 所允许的请求header
		  Access-Control-Max-Age: 86400
		  ```
- 参考
	- https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy
	- https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS
	- https://developer.mozilla.org/zh-CN/docs/Glossary/CSRF
	- https://juejin.cn/post/6879360544323665928
	- https://juejin.cn/post/6867096987804794888