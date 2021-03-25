title: xgboost C++线程安全问题定位与修复
date: 2021-03-25 9:48 PM
categories: 编程
tags: [Python, 机器学习, C++]

----

公司的线上模型服务是基于`brpc + xgboost`实现的，而xgboost官方是不支持在多线程环境下使用的（1.2.0版本之前）

这个模型服务已经有两年多了，显然当时用的版本是不支持多线程的，有位同事当时修改了xgboost的源码，解决了多线程的问题，在线上也稳定运行到现在。

那么，问题来了。最近有个新需求，用到了xgboost的`pred_leaf`功能，然后就发现并发请求时`0.1%`的模型结果不对。

<!--more-->

## 分析问题
调试过程中，首先删除其他模型，排除干扰。然后开关`pred_leaf`功能批量对比测试，确认当该功能关闭时，模型结果是正常的。

所以，很有可能`pred_leaf`参数导致程序走到和之前不同的分支，而这个分支的多线程问题并未修复。

那么，解决问题的思路就是：确定之前同事修改了什么，找到与pred_leaf相关的函数，尝试做相同修复。

## 尝试解决
首先得确定同事都修改了什么，由于代码历史比较就远了了，而且xgboost的改动并没有加入到git，也没有明显的版本号等标识，这个地方也就比较头疼了。

唯一能确定的是，xgboost版本的是0.6左右，修改源码时参考了[文章](https://blog.csdn.net/zc02051126/article/details/79427605)。

所以只能从git下载最新的代码，然后`git --no-pager log  --stat`查看每个commit的改动情况，使用`beyond compared对比 + 人肉二分查找`，最终定位到对应的commit。

找到了对应的commit之后，通过对比改动和结合上文参考文章，其实就是两类改动。
1. 存在竞争条件的变量 -> 加锁
2. 不存在竞争条件的变量 -> threadLocal，栈上自动变量


具体来说，以`PredLoopSpecalize`为例， 修改前
```c++
inline void PredLoopSpecalize() {
    const int nthread = omp_get_max_threads();
    InitThreadTemp(nthread, model.param.num_feature);
    for (bst_omp_uint i = 0; i < nsize - rest; i += K) {
        const int tid = omp_get_thread_num();
        RegTree::FVec& feats = thread_temp[tid];
        // thread_temp 为成员变量
        // 省略其他逻辑
    }
}

inline void InitThreadTemp(int nthread, int num_feature) {
    int prev_thread_temp_size = thread_temp.size();
    if (prev_thread_temp_size < nthread) {
      thread_temp.resize(nthread, RegTree::FVec());
      for (int i = prev_thread_temp_size; i < nthread; ++i) {
        thread_temp[i].Init(num_feature);
      }
    }
}
```

修改后
```c++
inline void PredLoopSpecalize() {
    const int nthread = omp_get_max_threads();
    std::vector<RegTree::FVec> local_thread_temp;  // 改动点
    int prev_thread_temp_size = local_thread_temp.size();
    if (prev_thread_temp_size < nthread) {
      local_thread_temp.resize(nthread, RegTree::FVec());
      for (int i = prev_thread_temp_size; i < nthread; ++i) {
        local_thread_temp[i].Init(model.param.num_feature);
      }
    }
    for (bst_omp_uint i = 0; i < nsize - rest; i += K) {
        const int tid = omp_get_thread_num();
        RegTree::FVec& feats = local_thread_temp[tid];  // 改动点
        // thread_temp 为成员变量
        // 省略其他逻辑
    }
}
```

显然问题就在`thread_temp`, 做为类成员，它不是线程安全的，通过替换为栈上的`local_thread_temp`，不同进程访问的地址不同，自然就不存在冲突了。

通过查找`PredLoopSpecalize`函数的调用链，可以发现其修改只会影响正常预测，pred_leaf则是不同的分支，显然线程安全的问题依然存在。
```c++
// 调用链
XGBoosterPredict()
    --> LearnerImpl::Predict()
        --> LearnerImpl::PredictRaw() // if 正常predict
            --> GBTree::PredictBatch()
                --> CPUPredictor::PredictBatch()
                    --> CPUPredictor::PredLoopInternal()
                        --> Dart::PredLoopSpecalize()
        --> GBTree::PredictLeaf()   // if pred_leaf
        --> GBTree::PredictContribution()
        --> ObjFunction::PredTransform()

// LearnerImpl::Predict() 源码
void Predict(DMatrix* data, bool output_margin,
            std::vector<bst_float>* out_preds, unsigned ntree_limit,
            bool pred_leaf, bool pred_contribs) const override {
    if (pred_contribs) {
        gbm_->PredictContribution(data, out_preds, ntree_limit);
    } else if (pred_leaf) {
        gbm_->PredictLeaf(data, out_preds, ntree_limit);
    } else {
        this->PredictRaw(data, out_preds, ntree_limit);
        if (!output_margin) {
        obj_->PredTransform(out_preds);
        }
    }
}
```

所以，最后采用与`PredLoopSpecalize`相同方法对`PredictLeaf`进行修复，问题得以完美解决。

## 总结
1. 源码版本管理非常重要。
2. 软件版本在新建项目时尽量选择较新版本，因为后续迭代更新版本的概率较小。
3. xgboost建议使用1.2.0以上版本，已经线程安全。

## 参考
- https://blog.csdn.net/zc02051126/article/details/79427605
- https://github.com/dmlc/xgboost
