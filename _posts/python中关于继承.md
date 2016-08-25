title: 关于Python的继承
date: February 28, 2016 11:26 AM
categories: 编程
tags: 
----

### 引子

童话里经常会看到英雄打败恶人的故事，而且故事里总会有一个类似黑暗森林的场景——要么是一个山洞，要么是一篇森林，要么是另一个星球，反正是英雄不该去的某个地方。当然，一旦反面角色在剧情中出现，你就会发现英雄非得去那片破森林去杀掉坏人。当英雄的总是不得不冒着生命危险进到邪恶森林中去。

在面向对象编程中，“继承”就是那片邪恶森林。有经验的程序员知道如何躲开这个恶魔，因为他们知道，在丛林深处的“继承”，其实是邪恶女皇“多重继承”。她喜欢用自己的巨口尖牙吃掉程序员和软件，咀嚼这些堕落者的血肉。不过这片丛林的吸引力是如此的强大，几乎每一个程序员都会进去探险，梦想着提着邪恶女皇的头颅走出丛林，从而声称自己是真正的程序员。你就是无法阻止丛林的魔力，于是你深入其中，而等你冒险结束，九死一生之后，你唯一学到的，就是远远躲开这片破森林，而如果你不得不再进去一次，你会带一支军队。

有的程序员现在正在丛林里跟邪恶女皇作战，他会对你说你必须进到森林里去。他们这样说其实是因为他们需要你的帮助，因为他们已经无法承受他们自己创建的东西了。

而对于你来说，你只要记住这一条：
大部分使用继承的场合都可以用合成取代，而多级继承则需要不惜一切地避免之。

<!--more-->
### 继承(Inheritance)
继承的用处，就是用来指明一个类的大部分或全部功能，都是从一个父类中获得的。当你写 class Foo(Bar) 时，代码就发生了继承效果，这句代码的意思是“创建一个叫 Foo 的类，并让他继承 Bar”。

继承的时候，父类和子类有三种交互方式：

#### 一. 隐式继承（Implicit Inheritance）
当你在父类里定义了一个函数，但没有在子类中定义的例子，这时候会发生隐式继承。

```python
class Parent(object):
    def implicit(self):
        print "PARENT implicit()"

class Child(Parent):
    pass

dad = Parent()
son = Child()
dad.implicit()
son.implicit()
```

#### 二. 显式覆写（Explicit Override） 
有时候你需要让子类里的函数有一个不同的行为，这种情况下隐式继承是做不到的，而你需要覆写子类中的函数。

```python
class Parent(object):
    def override(self):
        print "PARENT override()"

class Child(Parent):
    def override(self):
        print "CHILD override()"

dad = Parent()
son = Child()
dad.override()
son.override()
```

#### 三. 不完全覆写——super() 
父类中定义的内容运行之前或者之后再修改行为。

```python
class Parent(object):
    def altered(self):
        print "PARENT altered()"
class Child(Parent):
    
    def altered(self):
        print "CHILD, BEFORE PARENT altered()"
        super(Child, self).altered()
        print "CHILD, AFTER PARENT altered()"
dad = Parent()
son = Child()
dad.altered()
son.altered()
```

### 合成(Composition)
<b>合成就是不通过继承直接引用所需要类的方法。</b>继承是一种有用的技术，不过还有一种实现相同功能的方法，就是直接使用别的类和模块，而非依赖于继承。如果你回头看的话，我们有三种继承的方式，但有两种会通过新代码取代或者修改父类的功能。这其实可以很容易地用调用模块里的函数来实现。
```python
class Other(object):
    def override(self):
        print "OTHER override()"
    def implicit(self):
        print "OTHER implicit()"
    def altered(self):
        print "OTHER altered()"

class Child(object):
    def __init__(self):
        self.other = Other()
    def implicit(self):
        self.other.implicit()
    def override(self):
        print "CHILD override()"
    def altered(self):
        print "CHILD, BEFORE OTHER altered()"
        self.other.altered()
        print "CHILD, AFTER OTHER altered()"

son = Child()
son.implicit()
son.override()
son.altered()
```

### 继承和合成的应用场合
“继承 vs 合成”的问题说到底还是关于代码重用的问题。你不想到处都是重复的代码，这样既难看又没效率。继承可以让你在基类里隐含父类的功能，从而解决了这个问题。而合成则是利用模块和别的类中的函数调用实现了相同的目的。
如果两种方案都能解决重用的问题，那什么时候该用哪个呢？这个问题答案其实是非常主观的，不过我可以给你三个大体的指引方案：
1. 不惜一切代价地避免多重继承，它带来的麻烦比能解决的问题都多。如果你非要用，那你得准备好专研类的层次结构，以及花时间去找各种东西的来龙去脉吧。 
2. 如果你有一些代码会在不同位置和场合应用到，那就用合成来把它们做成模块。 
3. 只有在代码之间有清楚的关联，可以通过一个单独的共性联系起来的时候使用继承，或者你受现有代码或者别的不可抗拒因素所限非用不可的话，那也用吧。 
然而，不要成为这些规则的奴隶。面向对象编程中要记住的一点是，程序员创建软件包，共享代码，这些都是一种社交习俗。由于这是一种社交习俗，有时可能因为你的工作同事的原因，你需要打破这些规则。这时候，你就需要去观察别人的工作方式，然后去适应这种场合。
