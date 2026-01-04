---
title: 给 macOS 词典增加生词本功能
date: 2022-11-12 20:00:00
updated: 2022-11-04 19:40:00
categories: 工作生活
tags: [mac,]
---

macOS 系统的自带词典应用非常强大，与其他应用整合很好，快捷取词很方便（command+control+d）。
但是美中不足的是缺少生词本功能，查了单词又很容易忘记，对语言学习者来说就有些不便了。

经过本强迫症的探索，终于找到基于 Karabiner-Elements + Automator + Logseq 的完美生词本方案。
最后的效果是，快捷键取词的同时记录单词卡片到Logseq对应的笔记。
<!--more-->

## 词典词库扩充
参考[知乎文章](https://zhuanlan.zhihu.com/p/433646737)安装好《朗道英汉字典5.0》
这是为了有个释义简洁的词典，方便后续生成生词本词条

![](https://image.ponder.work/mweb/2022-11-02-16673997943438.jpg)
## 编写workflow
使用 macOS 自带应用 Automator（自动操作）编写workflow，将当前鼠标所在位置的文本提取并保存制卡。

首先打开 Automator.app 新建一个 Quick Aciont(快速操作)
![](https://image.ponder.work/mweb/2022-11-02-16673999123628.jpg)
然后依次拖入“获得词语定义”，“运行Shell脚本”等步骤，并调整如下几个位置的选项。
![](https://image.ponder.work/mweb/2022-11-02-16674004811769.jpg)

修改脚本里的代码为如下内容，生词本路径相应替换，并相应位置新建好生词本文件。
```Python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import sys, os, io, subprocess

FILE=os.path.expanduser("~/weiyun_sync/!sync/logseq-note/pages/生词本.md")
output = []
text = sys.argv[1].decode('utf8') if sys.version_info.major == 2 else sys.argv[1]

lines = [i.strip() for i in text.splitlines() if i.strip()]
if len(lines) < 2:
    exit(0)

word = lines[0]
if lines[1][0] == '*':
    output.append('- {}\t{}  [[card]]'.format(word, lines[1]))
    lines = lines[2:]
else:
    output.append('- {}\t  [[card]]'.format(word))
    lines = lines[1:]
output.append('\t- {}'.format(lines[0]))
for line in lines[1:]:
    output.append('\t  ' + line)

old_words = set()
with io.open(FILE, 'r', encoding='utf8') as fp:
    for line in fp:
        parts = line.split()
        if line.startswith('-') and len(parts) > 1:
            old_words.add(parts[1])

if word not in old_words:
    with io.open(FILE, 'a', encoding='utf8') as fp:
        fp.write('\n')
        fp.write('\n'.join(output))
        fp.write('\n')
    subprocess.check_call(['osascript', '-e', u'display notification "添加 {}" with title "生词本"'.format(word)])
else:
    subprocess.check_call(['osascript', '-e', u'display notification "跳过 {}" with title "生词本"'.format(word)])

```

选择路径保存好 workflow，然后在 `键盘 - 快捷键 - 服务` 中能看到新建的workflow。
为它设置快捷键 `command + shift + alt + 1`
![](https://image.ponder.work/mweb/2022-11-02-16674009451584.jpg)


## Karabiner-Elements
[Karabiner-Elements](https://karabiner-elements.pqrs.org/) 是 macOS 平台的一个重新映射快捷键的软件。
这里我们使用它将“查询单词”和“触发workflow”整合在一起，当然它还支持很多用途，这里就不赘述了。

注意确保Karabiner相关权限，并且设置中下图相关设备是勾选状态

![](https://image.ponder.work/mweb/2022-11-04-16675619005392.jpg)

安装好Karabiner-Elements后，打开它的配置文件
路径在 `/Users/<用户名>/.config/karabiner/karabiner.json`

在 `profiles -> complex_modifications -> rules` 列表中增加一项配置，内容如下。
然后保存，Karabiner会自动加载新的配置。

这里是将鼠标的侧键（靠前的）映射为查单词的快捷键，实现一键查词。
也可以根据需要更改按键，通过[EventViewer](https://karabiner-elements.pqrs.org/docs/manual/operation/eventviewer/)可以查看按键代码，配置文件格式可参考[官方文档](https://karabiner-elements.pqrs.org/docs/json/complex-modifications-manipulator-definition/to/)

```json
{
    "description": "Mouse",
    "manipulators": [
        {
            "from": {
                "pointing_button": "button5"
            },
            "to": [
                {
                    "pointing_button": "button1"
                },
                {
                    "pointing_button": "button1"
                },
                {
                    "key_code": "d",
                    "modifiers": [
                        "left_command",
                        "left_control"
                    ]
                },
                {
                    "key_code": "1",
                    "modifiers": [
                        "left_option",
                        "left_shift",
                        "left_command"
                    ]
                }
            ],
            "type": "basic"
        }
    ]
}
```

![](https://image.ponder.work/mweb/2022-11-02-16674017788245.jpg)

## 效果

可以看到 Logseq 中卡片生成的效果
![](https://image.ponder.work/mweb/2022-11-02-16674007610777.jpg)
![](https://image.ponder.work/mweb/2022-11-02-16674023982597.jpg)

## 参考
- https://karabiner-elements.pqrs.org/docs/
- https://zhuanlan.zhihu.com/p/433646737
- https://hectorguo.com/zh/save-words-in-dictionary/
- https://github.com/jjgod/mac-dictionary-kit
- https://lightcss.com/mac-dictionary/


