---
title: mitmproxy 使用
date: 2026-03-20 08:56:27
updated: 2026-03-20 08:56:27
categories:
  - 编程
tags: [抓包, 网络]
---

做 LLM Agent 开发时，经常要查看模型的请求与响应，需要一个便捷的工具。
mitmproxy 是一个功能强大的开源中间人代理，通常用于网络调试、分析 HTTP 和 HTTPS 流量。
<!--more-->

## 安装

1. 访问 https://www.mitmproxy.org/ ，根据指引安装，不同系统有区别
    - 也可以使用 `pip install mitmproxy` 安装 
2. 配置证书，用于解析 https，参考 https://docs.mitmproxy.org/stable/concepts/certificates/

## 使用
包含以下命令
- mitmdump：支持将捕获的数据导出到文件，类似tcpdump   
- mitmproxy：TUI 实时查看、修改和调试流量
- mitmweb：webui 实时查看、修改和调试流量（一般推荐用这个）

使用步骤
1. 启动 mitmweb
2. 设置代理环境变量：ALL_PROXY, 

```
~ ❯ mitmweb -p 8082 -s ~/projects/scripts/mitmproxy_fix_unicode.py
[15:26:42.046] Loading script /Users/ruan/projects/scripts/mitmproxy_fix_unicode.py
[15:26:42.047] HTTP(S) proxy listening at *:8082.
[15:26:42.047] Web server listening at http://127.0.0.1:8081/?token=4987293fea3331a4f3de2b0ba836a85d
load: 11.06  cmd: mitmweb 3541 waiting 0.55u 0.19s
[15:42:34.333][[::1]:62868] client connect
```

### python 证书相关问题
python 的 http 客户端有自己的证书处理逻辑，仅安装证书到系统还不能生效
需要额外设置环境变量

```
# 合并证书
cat $(python -c "import certifi; print(certifi.where())") \
~/.mitmproxy/mitmproxy-ca-cert.pem > ~/.mitmproxy/py-certifi-combined-ca.pem

# 设置环境变量
SSL_CERT_FILE=/Users/ruan/.mitmproxy/py-certifi-combined-ca.pem   # httpx 库
REQUESTS_CA_BUNDLE=/Users/ruan/.mitmproxy/py-certifi-combined-ca.pem  # requests 库
HTTPS_PROXY=https://localhost:8082
```


### webui 的 json 中文显示问题
需要附加脚本：`mitmweb -s ~/projects/scripts/mitmproxy_fix_unicode.py`

```python
# mitmproxy_fix_unicode.py

import json
from mitmproxy import contentviews


class PrettyJsonChinese(contentviews.Contentview):
    name = "JSON (中文)"
    syntax_highlight = "yaml"  # YAML is a superset of JSON, so this highlights JSON too

    def prettify(self, data: bytes, metadata: contentviews.Metadata) -> str:
        decoded = json.loads(data)
        return json.dumps(decoded, indent=4, ensure_ascii=False, sort_keys=False)

    def render_priority(self, data: bytes, metadata: contentviews.Metadata) -> float:
        # Match the same content types as the built-in JSON view, but with higher priority
        if metadata.content_type and "json" in metadata.content_type:
            return 2
        return 0

contentviews.add(PrettyJsonChinese)

```

### 让 json request 和 response 能够自动换行
使用 [tampermokey 脚本](https://github.com/ruanimal/browser-scripts/blob/master/mitmweb_wordwrap.user.js) 修改 webui