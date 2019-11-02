title: SublimeText3 快捷键列表
date: 2016-07-16 3:00 PM
categories: 编程
tags: 

----

主力使用SublimeText3编辑器，将一些常用的快捷键总结一下。

### 通用（General）
- `Esc` 退出功能，比如退出输出面板
- `↑↓←→`	上下左右移动光标，注意不是不是KJHL！
- `Alt`	显示菜单栏
- `Ctrl + Shift + P`	调出命令板（Command Palette）
- ``Ctrl + ` ``	调出控制台
- `Ctrl + K, Ctrl + 数字`	代码折叠，数字代表折叠的层次
- `Ctrl + Shift + [ / ]`	收起/展开选中的代码。

<!--more-->

### 窗口（Window）
- `Ctrl + Shift + N`	创建一个新窗口
- `Ctrl + N`	在当前窗口创建一个新标签
- `Ctrl + W`	关闭当前标签
- `Ctrl + Shift + T`	恢复刚刚关闭的标签

### 屏幕（Screen）
- `F11`	切换普通全屏
- `Shift + F11`	切换无干扰全屏
- `Alt + Shift + 2/3/4`	左右分组,分2到4组
- `Alt + Shift + 8/9`	上下分组,分2到3组
- `Alt + Shift + 5`	上下左右分组
- `Ctrl + 数字键`	跳转到指定组
- `Ctrl + Shift + 数字键`	将当前标签移动到指定组

### 跳转（Jumping）
- `Ctrl + P`	跳转到指定文件，输入文件名后可以打开对应文件
- `@ 符号跳转`	输入@symbol跳转到symbol符号所在的位置，比如函数或类
- `# 关键字跳转`	输入#keyword跳转到keyword所在的位置
- `: 行号跳转`	输入:12跳转到文件的第12行。
- `Ctrl + R`	跳转到指定符号 @
- `Ctrl + G`	跳转到指定行号 :
- `Ctrl + ;`	跳转到指定关键字

### 编辑（Editing）
- `Ctrl + /`	注释当前行，取消注释
- `Ctrl + Enter`	在当前行下面新增一行然后跳至该行
- `Ctrl + Shift + Enter`	在当前行上面增加一行并跳至该行
- `Ctrl + ←/→`	进行逐词左右移动
- `Ctrl + Shift + ←/→ `	进行左右逐词选择
- `Ctrl + ↑/↓ `	上下移动当前显示区域
- `Ctrl + Shift + ↑/↓ ` 上下移动当前行，或者选中行
- `Ctrl + KU/KL `	转换当前单词为大写/小写

### 选择（Selecting）
- `Ctrl + D`	选择当前词，进入多重编辑
- `Ctrl + K`	多重编辑时跳过当前选中的
- `Ctrl + U`	多重编辑，回退选中
- `Ctrl + Shift + L`	将当前选中区域打散
- `Ctrl + J`	把当前选中区域合并为一行
- `Ctrl + M`	在起始括号和结尾括号间切换
- `Ctrl + Shift + M`	快速选择括号间的内容
- `Ctrl + Shift + J`	快速选择同缩进的内容
- `Ctrl + Shift + Space`	快速选择当前作用域（Scope）的内容

### 查找&替换（Finding&Replacing）
- `F3`	跳至当前关键字下一个位置
- `Shift + F3`	跳到当前关键字上一个位置
- `Alt + F3`	选中当前关键字出现的所有位置
- `Ctrl + F/H`	进行标准查找/替换，之后
- `Alt + C`	切换大小写敏感（Case-sensitive）模式
- `Alt + W`	切换整字匹配（Whole matching）模式
- `Alt + R`	切换正则匹配（Regex matching）模式
- `Ctrl + Shift + H`	替换当前关键字
- `Ctrl + Alt + Enter`	替换所有关键字匹配
- `Ctrl + Shift + F`	多文件搜索&替换
