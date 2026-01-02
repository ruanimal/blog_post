---
title: Hexo 版本更新与技术债务
date: 2026-01-02 09:14:19
updated: 2026-01-02 11:43:07
categories: 编程
tags: [Hexo, 随感]
---

昨天花了些时间将 Hexo + next 的博客版本更新了下，发现不少问题。
博客已经很多年了，一直用的是最开始的Hexo版本，nodejs 也是 v12，next 主题也是早年源码安装的，还在上面做了修改。
也是早就明白需要更新了，但是觉得麻烦，就一直没动，最后变得相当麻烦。

<!--more-->

## 依赖更新
首先是版本升级，先将 nodejs 切换到最新 lts（v22）。
再尝试使用npm将 package.json 中的库自动更新，但由于版本差距太大以及很多库不维护了，更新不了。

最后只能使用 hexo init 新建个博客项目，将里面的依赖项复制到老博客里，删除对应的老依赖。
剩下的依赖，大部分是安装的插件，只能一个个搜索用途，看看有没有替代或者还要不要用。
package.json 中的其他参数，参考最新的配置文件，将无用（过时）的设置项删除。

使用 npm 安装 next 主题，将原 themes/next 中的配置文件复制到 _config.next.yml。
对比 hexo 和 next 官方 _config 文件，相应修改 _config.yml 和 _config.next.yml。
删除 themes 中重复的主题目录。

使用 npm install 安装依赖，保证能够正常生成博客。

删除 node_modules，改用 pnpm 管理依赖，更轻量快速。
使用 pnpm 时可能会报错，如某个库的 `index.node` 找不到，是因为 pnpm 默认不执行库的 post install 脚本。
需要将这些库添加到 pnpm.onlyBuiltDependencies 中。
```
  "pnpm": {
    "onlyBuiltDependencies": [
      "hexo-word-counter",
      "hexo-util"
    ]
   }
```

ps: 
- 总体来说 pnpm 还是存在一些兼容性问题，但大部分都不是 pnpm 本身的问题，基本上都是库的影子依赖。
- 大模型在这种疑难杂症上帮助很大

## 额外设置
### hexo
修改 scaffolds 文章模板文件
老版本 hexo 的 scaffolds/page.md 等文件格式与新版不同，会导致一些工具不能识别 front-matter, 需要更新。

老版本 front-matter 前面少了开头的 `---`，导致 vscode 的 hexo-util 插件不能识别 tag 等信息，调试了很久。


```
# 老版本
title: {{ title }}
date: {{ date }}
---

# 新版本
---
title: {{ title }}
date: {{ date }}
---
``` 

### next
自定义样式和脚本，之前是通过之间修改主题源码实现，现在使用 custom_file_path 注入自定义内容。
需要修改 _config.next.yml 文件

```yaml
custom_file_path:
  head: source/_data/head.njk
  bodyEnd: source/_data/body-end.njk
  style: source/_data/styles.styl
```

#### 自定义样式
next 主题的 Muse scheme 整体比较符合我的口味，但部分样式还需要微调。

source/_data/styles.styl

```css

// 自动给文章的 toc 和正文标题编号, 不对首页编号
body {counter-reset: h1}
.post-block .post-body h2 {counter-reset: h2}
.post-block .post-body h3 {counter-reset: h3}
.post-block .post-body h4 {counter-reset: h4}
.post-block .post-body h5 {counter-reset: h5}
.post-block .post-body h6 {counter-reset: h6}

.post-block .post-body h2:before {
  counter-increment: h1;
  content: counter(h1) ". "
}
.post-block .post-body h3:before {
  counter-increment: h2;
  content: counter(h1) "." counter(h2) " "
}
.post-block .post-body h4:before {
  counter-increment: h3;
  content: counter(h1) "." counter(h2) "." counter(h3) " "
}
.post-block .post-body h5:before {
  counter-increment: h4;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) " "
}
.post-block .post-body h6:before {
  counter-increment: h5;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) " "
}
.post-block .post-body h1.nocount:before,
.post-block.post .post-body h2.nocount:before,
.post-block.post .post-body h3.nocount:before,
.post-block.post .post-body h4.nocount:before,
.post-block.post .post-body h5.nocount:before,
.post-block.post .post-body h6.nocount:before {
  content: "";
  counter-increment: none
}

// 隐藏文章 toc 中文章目录 tab 中的友链信息，站点概览中的保留
.sidebar .sidebar-toc-active + .sidebar-blogroll {
    display: none
}

```

#### 只在文章页显示侧边栏
next 主题的侧边栏逻辑有点问题， 就算设置 sidebar.display 为 post，当从文章跳到其他页面时，侧边栏并不会自动关闭，所以只能通过脚本来绕过。


source/_data/body-end.njk 
```js
<script>
  document.addEventListener('pjax:success', () => {
    if (CONFIG.sidebar.display !== 'remove') {
      const hasTOC = document.querySelector('.post-toc:not(.placeholder-toc)');

      // 当没有 TOC 且侧边栏正在显示时，隐藏侧边栏
      if (!hasTOC && document.body.classList.contains('sidebar-active')) {
        window.dispatchEvent(new Event('sidebar:hide'));
      }
    }
  });
</script>

```

#### 自定义重定向
hexo 的文章不支持多个入口，比如我想要分类中英文都可以访问，默认情况是做不到的。

在设置了 category_map 的情况下，hexo 只会生成 programming 等英文链接，无法同时保留中文url作为入口。

```
category_map:
  编程: programming
  随笔: writing
  阅读: reading
  工作生活: life
```

所以最终通过在 404 页面添加自定义的 js 实现重定向逻辑。

source/_data/head.njk
```js
{% if page.title === '404 Page Not Found' or page.type === '404' or page.layout === '404' %}
<script>
(function() {
  // 从 Hexo 配置中获取 category_map
  var categoryMap = {{ config.category_map | dump | safe }};
  var currentPath = decodeURIComponent(window.location.pathname);

  // 检查路径中是否包含分类映射的key
  for (var key in categoryMap) {
    if (currentPath.includes(key)) {
      var targetCategory = categoryMap[key];
      var targetPath = currentPath.replace(key, targetCategory);

      // 执行重定向
      if (currentPath !== targetPath) {
        window.location.replace(targetPath);
        return;
      }
    }
  }
})();
</script>
{% endif %}

```

## 更换编辑器
之前一直是用 mac 平台是 mweb 作为 hexo 的文章编辑器，实话说也非常好用。
但是我把主力操作系统换成 linux 之后，linux 上一直没找到与 mweb 相当的应用。
最终经过一番折腾，最终使用 vscode + Hexo Utils 插件作为平替。
同时对该插件进行来[二开](https://github.com/0x-jerry/vscode-hexo-utils/pulls/ruanimal)，最终体验算是追平了 mweb。

## 感受
所谓技术债务，项目正常迭代的过程中是不断积累的，如果平时不跟进解决，最终在某个阶段就会爆炸，造成巨大影响。

平时迭代时，如果时间安排的过紧，我们就会倾向于采取保守的决策（能跑就不要动），最终不可避免的技术债务堆积。

当然，生活中其实也是这样吧，很多不紧急的问题，一直拖着，最终大概率也会无可挽回。