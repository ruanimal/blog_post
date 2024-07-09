title: IPython学习环境配置
date: 2020-07-18 8:17 PM
categories: 编程
tags: [数据分析, Python]

---

## IPython简介
IPython项目起初是Fernando Pérez在2001年的一个用以加强和Python交互的子项目。在随后的16年中，它成为了Python数据栈最重要的工具之一。

简单来说，我们可以把IPython当成一个学习Python语言、数据分析、机器学习的平台。

<!--more-->

## 环境安装
### Python
这里我们使用[miniconda](https://docs.conda.io/en/latest/miniconda.html)，防止机器学习和图形显示相关的库出问题. 使用pyenv的同学，也可以用pyenv来安装miniconda。

下载：`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh`

安装: `sh Miniconda3-latest-MacOSX-x86_64.sh`

### 创建ipython虚拟环境
1. 创建虚拟环境：`conda create -n ipython`
2. 激活环境：`conda activate ipython`
3. 安装必要的python库：`pip install ipython pandas ipykernel matplotlib`

## 用Visual Studio Code作为编辑器
[VSCode](https://code.visualstudio.com/)在安装Python插件之后，就可以很方便得查看编辑IPython Notebook了

### 安装Python插件
在扩展商店，搜索“Python”， 并安装
![-w549](https://image.ponder.work/mweb/2020-07-19-15951449200011.jpg)

### 创建使用NoteBook
选择IPython环境
![-w1421](https://image.ponder.work/mweb/2020-07-19-15951453546560.jpg)

创建`hello.ipynb`Notebook
![-w1421](https://image.ponder.work/mweb/2020-07-19-15951457001314.jpg)

