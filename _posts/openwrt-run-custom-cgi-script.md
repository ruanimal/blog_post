title: OpenWrt执行自定义CGI脚本
date: 2020-11-26 8:17 PM
categories: 编程
tags: [CGI, OpenWrt]

---

## 缘起
我家里的路由器是矿渣newifi3, 刷了OpenWrt系统，可玩性还是非常强的。
而且路由器作为24小时在线的设备，很适合作为网络设备的控制中心，比如使用[WOL](https://zh.wikipedia.org/wiki/%E7%B6%B2%E8%B7%AF%E5%96%9A%E9%86%92)唤醒其他设备。
之前就写过一个Python服务，用来控制其他设备的唤醒和睡眠。但是由于newifi3的rom空间十分有限，usb又十分不稳定，Python环境在路由器上还是太重了。
所以就想到了利用路由器默认的uhttpd网页服务器，自己编写CGI脚本来实现相应功能。
<!--more-->

## 实现
以下操作均需要ssh登陆到路由器后台

### uhttpd添加lua执行功能
编辑`/etc/config/uhttpd`文件
在`config uhttpd main`部分添加`list interpreter ".lua=/usr/bin/lua"`， 使uhttpd能够执行lua文件

重启uhttp服务：`/etc/init.d/uhttpd restart`

修改后的配置大致如下
```
# Server configuration
config uhttpd main

	# HTTP listen addresses, multiple allowed
	list listen_http	0.0.0.0:80
	list listen_http	[::]:80

	# HTTPS listen addresses, multiple allowed
	list listen_https	0.0.0.0:443
	list listen_https	[::]:443

	# Redirect HTTP requests to HTTPS if possible
	option redirect_https	1

	# Server document root
	option home		/www
	
	# 此处省略其他配置
	
	# List of extension->interpreter mappings.
	# Files with an associated interpreter can
	# be called outside of the CGI prefix and do
	# not need to be executable.
#	list interpreter	".php=/usr/bin/php-cgi"
#	list interpreter	".cgi=/usr/bin/perl"
	list interpreter ".lua=/usr/bin/lua"  # 我们添加的内容

# 此处省略其他配置
```

### 添加CGI脚本
从上面的配置可以看到，web的默认路径在`/www`
我们就在这里新建一个文件夹`ctl`，来存放我们的CGI脚本, 用于实现NAS的睡眠和唤醒。

目录信息如下
```
/www/
├── cgi-bin
│   └── luci
├── ctl
│   ├── sleep.lua
│   └── wakeup.lua
├── index.html
```

下面开始编写CGI脚本，需要复习以下CGI协议，可以参考[本人的文章](http://ponder.work/2019/09/28/python-web-development/#CGI)
再花几分钟熟悉一下[lua语法](https://www.runoob.com/lua/lua-tutorial.html)

#### NAS睡眠脚本 
睡眠的实现是在NAS上写了个简单的Web服务，基于`systemctl suspend`来实现睡眠
然后访问Web服务，触发NAS的睡眠。这里为了和下面的唤醒统一处理，所以通过CGI转发了一道。
```lua
#!/usr/bin/lua
-- /www/ctl/sleep.lua

io.stdout:write("Content-Type: text/plain\r\n\r\n")
local status = os.execute("wget -q -O - --timeout 1 -t 1  http://192.168.123.100:8888/ctl/sleep > /dev/null")
if status == 0 then
	io.stdout:write("sleep succ\n")
else
	io.stdout:write("sleep fail, already sleep?\n")
end
```

使用：`curl http://192.168.123.1/ctl/sleep.lua`

#### NAS唤醒脚本
唤醒是基于WOL，原理是在网络上广播特定格式的网络包，目标机器的网卡接受到以后唤醒机器。

```lua
#!/usr/bin/lua

io.stdout:write("Content-Type: text/plain\r\n\r\n")
-- /usr/bin/etherwake -i <网口> <MAC>
-- 网口需要是和目标机器同网段的接口，在OpenWrt中通常是br-lan
local status = os.execute("/usr/bin/etherwake -i br-lan 00:12:34:56:78:90")
if status == 0 then
	io.stdout:write("wakeup succ\n")
else
	io.stdout:write("wakeup fail\n")
end
```
使用：`curl http://192.168.123.1/ctl/wakeup.lua`

## 参考
1. https://zh.wikipedia.org/wiki/%E7%B6%B2%E8%B7%AF%E5%96%9A%E9%86%92
2. https://www.zhihu.com/question/31579325/answer/283425839
3. https://www.runoob.com/lua/lua-tutorial.html
4. https://openwrt.org/docs/guide-user/services/webserver/uhttpd
