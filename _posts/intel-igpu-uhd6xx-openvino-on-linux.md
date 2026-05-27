---
title: Linux 平台 intel UHD 6xx 核显 openvino 探索
date: 2026-05-27 21:20:31
updated: 2026-05-27 21:20:31
categories: 编程
tags: [Linux]
---

日常生活中有碰到轻量模型的推理需求，比如验证码识别、tts生成等。
想要这个服务24h可用，就不能在日常电脑上部署。正好有个 J4125 的迷你主机作为家庭服务器，就先把模型部署到上面，验证下是否满足需求。

<!--more-->

核显思路就是使用 openvino + onnx，当最终还是失败，下面记录下探索过程。

## 核显驱动
openvino 是 intel 推出的一款开源 AI 推理工具套件，旨在帮助开发者在 intel 显卡上部署深度学习模型。
openvino 依赖 opencl, 所以需要正确驱动显卡；不过使用 docker 的话，应该不需要宿主机正确驱动，能识别到设备就行了。

所有简单起见，直接使用 docker 部署，由于 ubuntu 新系统移除了老 intel 核显的驱动支持，只能使用 ubuntu 20 lts 镜像。
> Intel Beignet 项目终止：Ubuntu 20.04 为旧款 Intel 核显提供 OpenCL 支持的 beignet-opencl-icd 包，在 Ubuntu 22.04 中已被移除

同时，老核显的 opencl 要能正常工作，内核版本也有要求，所以这里使用 5.15 内核 + openvino/ubuntu20_runtime:latest 镜像。

## onnx 尝试
执行  `./benchmark_app -m ./model_68_64_65.onnx -d GPU -hint latency -shape '[1,1]' -t 30`
> model_68_64_65.onnx 是一个小型决策树模型，用于测试 openvino 功能

然而，出现以下错误，`'work_group_reduce_max' is invalid in OpenCL`
说明，我们这个核显不支持这个 opencl api，模型加载失败。

```

Traceback (most recent call last):
  File "/opt/intel/openvino/python/openvino/tools/benchmark/main.py", line 449, in main
    compiled_model = benchmark.core.compile_model(model, benchmark.device, device_config)
  File "/opt/intel/openvino/python/openvino/_ov_api.py", line 599, in compile_model
    super().compile_model(model, device_name, {} if config is None else config),
RuntimeError: Exception from src/inference/src/cpp/core.cpp:109:
Exception from src/inference/src/dev/plugin.cpp:53:
Check 'false' failed at src/plugins/intel_gpu/src/plugin/program_builder.cpp:163:
[GPU] ProgramBuilder build failed!
Program build failed(0_part_22):
25:8772:15: error: implicit declaration of function 'work_group_reduce_max' is invalid in OpenCL
 my_maximum = work_group_reduce_max(my_maximum);
              ^
25:8772:15: note: did you mean 'sub_group_reduce_max'?
....
25:8801:11: error: implicit declaration of function 'work_group_reduce_add' is invalid in OpenCL
 my_sum = work_group_reduce_add(my_sum);
          ^
25:8801:11: note: did you mean 'work_group_reduce_max'?
....
```

核心问题的 uhd600 的 opencl 版本太低了。要 2.0 以上才比较好支持 openvino, 而 uhd600 只有 1.2。
```
(workdir) root@N4100:~/workdir# clinfo | grep -i "OpenCL C"
  Device OpenCL C Version                         OpenCL C 1.2 
```

相对的 uhd770 的 opencl 版本
```
Device OpenCL C Version        OpenCL C 1.2 
Device OpenCL C all versions   OpenCL C      0x400000 (1.0.0)
                               OpenCL C      0x401000 (1.1.0)
                               OpenCL C      0x402000 (1.2.0)
                               OpenCL C      0xc00000 (3.0.0)
```

intel GPU 典型 OpenCL C 版本
- Intel Gen8 / Gen9（UHD 500/600 / Iris 540/550）	1.2（仅部分 2.0 功能）
- Intel Gen11（UHD620 / Whiskey Lake 之后）	1.2 / 部分 2.0（仍不完整）
- Intel Gen12（Iris Xe / ARC）	OpenCL C 3.0 完整支持

## 结论
uhd600 支持不了 onnx 跑模型，需要换成 12代以上的 cpu。
最终， nuc13 的设备已经在路上了