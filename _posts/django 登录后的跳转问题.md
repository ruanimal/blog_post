title: django 登录后的跳转到之前的页面
date: November 25, 2015 8:57 PM 
categories: 编程
tags: [Python, Django]

---


## 概述
在开发django网站时发现，用户登录后不能跳转到之前的页面，google了很多答案，讲得也不清楚。

其实就是渲染登陆表单时，将原链接带到action参数里，view函数接收到参数后进行重定向。

## 实现
### 登录链接
```xml
<a href="/account/login/?next={{request.path}}">登录</a>
```

### view
```Python
def login(request):
    next_url = request.REQUEST.get('next', '/')
    
    if request.method == 'GET':
        return render_to_response('account/login.html', {'next_url': next_url}, context_instance=RequestContext(request))

    django_login(request, user)
    return redirect(next_url)
```

### 登录表单
```xml
<form action="/account/login/?next={{next_url}}" method="post" >
{% csrf_token %}
    用户名<input id="username" type="text" name="username"  required/>
	</br>
    密码<input type="password" name="password" required/>
    <input type="submit" value="登  录"/>
</form>
```





