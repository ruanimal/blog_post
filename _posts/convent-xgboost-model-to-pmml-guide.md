title: 在Java环境中使用PMML执行xgboost模型 
date: 2020-04-10 9:48 PM
categories: 编程
tags: [Python, 机器学习, Java]

----

## 缘起
最近有个需求, 在Java环境环境运行xbgboost模型, 查询资料后发现PMML可以解决这个问题.

PMML是数据挖掘的一种通用的规范，它用统一的XML格式来描述我们生成的机器学习模型。这样无论你的模型是sklearn,R还是Spark MLlib生成的，我们都可以将其转化为标准的XML格式来存储。当我们需要将这个PMML的模型用于部署的时候，可以使用目标环境的解析PMML模型的库来加载模型，并做预测。

可以看出，要使用PMML，需要两步的工作:
* 第一块是将离线训练得到的模型转化为PMML模型文件
* 第二块是将PMML模型文件载入在线预测环境，进行预测

<!--more-->

## 模型转PMML
### sklearn2pmml
常见的方法是用`sklearn2pmml`, 主要思路是将Booster模式转为`Scikit-Learn Wrapper interface`的`XGBModel`, 然后再使用`PMMLPipeline`保存为PMML模型文件

```python
import xgboost as xgb
from sklearn_pandas import DataFrameMapper
from sklearn2pmml import PMMLPipeline, sklearn2pmml

FILE = 'demo.model'

def convert(file):
    mod = xgb.XGBModel()
    mod.load_model(file)
    pipe = PMMLPipeline([
        ("classifier", mod),
    ])
    # pipe.configure(ntree_limit=999)
    sklearn2pmml(pipe, file + '.pmml', with_repr=True)
    
convert(FILE)
```

使用这种方法, 可能会出现因为模型包含中文信息导致转换失败
```
Standard output is empty
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
  File "/Users/ruan/.pyenv/versions/2.7.16/lib/python2.7/site-packages/sklearn2pmml/__init__.py", line 262, in sklearn2pmml
    print("Standard error:\n{0}".format(_decode(error, java_encoding)))
UnicodeEncodeError: 'ascii' codec can't encode character u'\u6708' in position 1: ordinal not in range(128)
'ascii' codec can't encode character u'\u6708' in position 1: ordinal not in range(128)
```

### jpmml-xgboost
也可以[jpmml-xgboost](https://github.com/jpmml/jpmml-xgboost)工具, 将xgboost模型直接转换为PMML

注意这里的模型文件, 需要是通过`xgboost.Booster.save_model`方法保存的.

#### 下载 
```shell
wget https://github.com/jpmml/jpmml-xgboost/releases/download/1.3.15/jpmml-xgboost-executable-1.3.15.jar
```

#### 生成fmap特征映射文件
fmap文件的每行的格式是: `特征索引\t特征名称\tq`
特征名称可以随意命名, 在调用PMML预测时会用到

例如: fmap.txt
```
0	fea0	q
1	fea1	q
2	fea2	q
3	fea3	q
4	fea4	q
...
```


#### 执行
```shell
java -jar jpmml-xgboost-executable-1.3.15.jar \
	--model-input demo.model \  # 输入
	--pmml-output demo.model.pmml \  # 输出
	--fmap-input fmap.txt \  # 特征映射文件
	--missing-value -1 \   # 指定模型缺失值
```

## 模型预测
### python环境比较模型结果
python可以使用`pypmml`库, 测试我们转换好的PMML, 并和原始模型进行分数比较

```python
from pypmml import Model
import xgboost as xgb
import numpy as np

xgb_mod = xgb.Booster(model_file='demo.model')
pmml_mod = Model.load('demo.model.pmml')

# float分数比较
def eq(a, b):
    return abs(a - b) < 0.00001

# xgboost预测
def predict(mod, data):
    fea = np.asarray(data, dtype=np.float64).reshape([1, -1])
    dtest = xgb.DMatrix(fea, missing=np.float64(-1.0))
    return mod.predict(dtest)[0]

# pmml预测
def pmml_predict(mod, data):
    fea = {"fea{}".format(idx): elem for (idx, elem) in  enumerate(data)}
    return mod.predict(fea)['probability(1)']

data = [1, 2, 3, 4]
a, b = predict(xgb_mod, data), pmml_predict(pmml_mod, data)
assert eq(a, b)
```

### Java环境执行
java环境执行, 需要用到`pmml-evaluator`和`pmml-evaluator-extension`库

具体代码参考 https://www.cnblogs.com/pinard/p/9220199.html

## 参考
1. https://www.cnblogs.com/pinard/p/9220199.html
2. https://blog.csdn.net/yueguanghaidao/article/details/91892549
3. https://github.com/jpmml/jpmml-xgboost
4. https://yao544303.github.io/2018/07/11/sklearn-PMML/