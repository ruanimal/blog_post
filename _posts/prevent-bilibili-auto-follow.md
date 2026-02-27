---
title: 阻止 bilibili 网页自动关注
date: 2026-01-02 18:32:09
updated: 2026-01-02 18:32:09
categories: 工作生活
tags: [Web, uBlock]
---

B 站非常逆天，只要你使用网页端看视频，点开首页推荐的视频，观看一定时长，就有概率会触发自动关注该 UP 主。
之前也有怀疑是某个浏览器插件的锅，但更换浏览器依然能够触发这个问题。
> 后来发现疑似是 bilibili 默认绑定了按键 `G` 关注 UP，非常容易误触发。 

网上发现不少类似的问题，但都没有解决方案，迫于无奈只能使用自定义广告过滤规则了，之后没有再出现问题。

这里使用 uBlock origin, 其他去广告插件也类似, 进入插件设置 -> 自定义静态规则，添加如下规则。
在视频页面禁止关注请求，不影响点开 UP 主主页进行关注。
```
www.bilibili.com##+js(no-fetch-if, /api\.bilibili\.com\/x\/relation\/modify/, location.pathname.startsWith('/video/'))
```
