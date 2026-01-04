---
title: 使用PlantUML做软件设计
date: 2019-09-21 09:48:00
updated: 2022-04-02 18:57:00
categories: 编程
tags: [UML, 软件架构]
---

## Plantuml 是什么？
首先得说一下UML，**统一建模语言**（英语：Unified Modeling Language，缩写 UML）是非专利的第三代和规约语言。

UML涵盖了很多类型的图，主要都是应用于软件开发行业。

在UML系统开发中有三个主要的模型：
- **功能模型**：从用户的角度展示系统的功能，包括用例图。

- **对象模型**：采用对象，属性，操作，关联等概念展示系统的结构和基础，包括类别图、对象图。

- **动态模型**：展现系统的内部行为。包括序列图，活动图，状态图。

而PlantUML是一个开源项目，除了支持快速绘制上面这些类型的图表之外，还支持很多图表，具体查看[官方网站](http://plantuml.com/zh/index)。

PlantUML通过编写文本的方式来定义UML图表，有点类似markdown，然后生成图表

<!--more-->

示例：
```
@startuml
' Split into 4 pages
page 2x2
skinparam pageMargin 10
skinparam pageExternalColor gray
skinparam pageBorderColor black

class BaseClass

namespace net.dummy #DDDDDD {
	.BaseClass <|-- Person
	Meeting o-- Person

	.BaseClass <|- Meeting

}

namespace net.foo {
  net.dummy.Person  <|- Person
  .BaseClass <|-- Person

  net.dummy.Meeting o-- Person
}

BaseClass <|-- net.unused.Person
@enduml
```

输出效果
![](https://image.ponder.work/mweb/15690347198367.jpg)

## 环境搭建
我们需要一个编辑器/IDE来编辑和预览UML图表，这里使用[vscode](https://code.visualstudio.com/)

### 安装PlantUML插件
![-w1151](https://image.ponder.work/mweb/15690363185298.jpg)

### 配置插件渲染方式
渲染方式有两种
- local 本地的Java渲染服务，需要Java运行环境及Graphviz
- PlantUMLServer 远程渲染服务器

方便起见，我们直接用官方的服务器
![-w1151](https://image.ponder.work/mweb/15690367077023.jpg)

### 验证
1. 新建 test.puml
    ```
    @startuml
    ' Split into 4 pages
    class BaseClass

    @enduml
    ```

2. 预览图表
![-w1151](https://image.ponder.work/mweb/15690369832230.jpg)

## PlantUML基础语法
由于PlantUML支持的图表类型比较多，每种图表的语法还不太一致，这里只简单介绍通用的语法，具体的图表还是建议查看官方文档。

也建议大家，在使用过程中记录适合自己的每种图表的模板，作图效率大大提高。

**注意**：语句类型是和图关联的，也就是说某些语句只能在某个图表用，而且PlantUML会根据你用到的语句猜测你是什么图表，然后进行渲染。

### 图表块
以`@startuml`和`@enduml`标记一个图表，还可以在开始处记录图表的名称（这里是hello-world）

```
@startuml hello-world
You -> World: Hello
@enduml
```

![-w315](https://image.ponder.work/mweb/15690376853589.jpg)

### 注释和标记
- 单行注释：单引号 `'` 在行首
- 多行注释：以`/'` 开始， 以 `/'` 结束
- 图表标记：`note left|right|top|bottom of XXX`

```
@startuml hello-world
' You -> World: Hello 单行注释

/'
you can not 多行注释
see me
'/

You <-> World: Hello
note left of You: yoyoyo
' 标记
@enduml
```

![-w254](https://image.ponder.work/mweb/15690390104495.jpg)


### 对象和关系
**对象**： 图表中的方块，一般出现才关系的两端，有些需要额外定义（如接口，类）
**关系**：一般用形如箭头的字符来表示对象之间的关系，字符不同样式不同

```
@startuml hello-world1
You -> World: Hello
You <- World: also Hello
You <-> World: Hololo
You <--> World: Hololo
@enduml
```
![-w260](https://image.ponder.work/mweb/15690396911033.jpg)

## 一些例子
### 时序图
```
@startuml
participant 用户
用户 -> 店长: 询问：iphone11 有吗？
activate 店长

note left of 用户: 我很暴躁
note left of 店长: 巧了，我也是

店长 -> 服务员: 命令：去查下库存
activate 服务员
服务员 -> 库存系统: 查询库存
activate 库存系统
return 库存量
deactivate 库存系统
alt "库存量 > 0"
	服务员 -> 店长: 通知：货多得很
else
	服务员 -> 店长: 通知：没货了
end
deactivate 服务员

alt "库存量 <= 0"
	店长 -> 用户: 不凑巧，买完了
    用户 -> 店长: 没货还挂着商品，耍人吗???
    用户 -> 店长: 愉快地打了一架
end
店长 -> 用户: Done
@enduml
```

![-w765](https://image.ponder.work/mweb/15690411434468.jpg)

### 类图
```
@startuml
class Head
class Body

class Animal {
    head
    body
    eye_num = 2
    hand_num = 0
    leg_num = 4
    tail_num = 1

    run()
    shout()
}

class Cat

class Fish {
    hand_num = 0
    leg_num = 0
    tail_num = 1

    swim()
}


class FishShoal {
    shoal_size
    fish_type
    fish_array

    migrate()
}
note left of FishShoal: 鱼群

class Human {
    hand_num = 2
    leg_num = 2
    tail_num = 0

    speak()
    work()
}

class Sutdent {
    study()
}

class School {
    location
    level
    student_num
    student_array
}

' 组合
Animal *-- Head
Animal *-- Body

' 继承、扩展
Animal <|-- Cat
Animal <|-- Fish
Animal <|-- Human
Human <|-- Sutdent

' 聚合
School o-- Sutdent: contains >
FishShoal o-- Fish: contains >
@enduml
```

![-w1253](https://image.ponder.work/mweb/15690445125047.jpg)

## 参考资源
- https://real-world-plantuml.com/ PlantUML示例网站
