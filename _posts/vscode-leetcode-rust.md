title: 在 VSCode 中用 Rust 刷LeetCode
date: 2025-03-08 8:17 PM
categories: 编程
tags: [Rust, ]

---

本文介绍在 VSCode 中配置和使用插件来高效地解决 LeetCode 问题，并使用 Rust 语言编写和测试代码。
<!--more-->

## vscode 插件
- LeetCode.vscode-leetcode
- pucelle.run-on-save
- rust-lang.rust-analyzer

## 项目结构
cargo new vscode-leetcode-rust

```
// tree -I target --dirsfirst
.
├── Cargo.lock
├── Cargo.toml
└── src
    ├── lib.rs
    ├── main.rs
    └── solutions
        ├── 1_two_sum.rs
        ...
```

## vscode 全局设置
```json
    "leetcode.useEndpointTranslation": false,  // for english filename
    "leetcode.workspaceFolder": "/Users/<your_name>/projects/vscode-leetcode-cn-rust",   
    "leetcode.filePath": {
        "default": {
            "folder": "src/solutions",
            "filename": "${id}_${snake_case_name}.${ext}"
        }
    },
```

## 用 automod 宏添加新回答到模块
cargo add automod

```rust
// src/lib.rs 

const CURRENT: &str = "sdfsdfsd.rs";  // trigger rust-analyser recheck

pub mod solutions {
    automod::dir!("src/solutions");
}
```

## 触发 rust-analyzer
用 run-on-save 插件，保存回答时更新 lib.rs，触发 rust-analyzer 重新分析项目，开启新回答的代码补全。

vscode 项目配置
```
    "runOnSave.commands": [
        {
             // use gnu sed update lib.rs when add solutions (macOS)
            "command": "sh onsave.sh ${fileBasename}",  
            "runIn": "backend",
            "finishStatusMessage": "touched ${workspaceFolderBasename}"
        },
    ]
```


`onsave.sh`脚本，macOS使用 gnused，linux 使用默认 sed 就好。
通过切换模块是否为pub来触发 rust-analyzer 识别新回答

```bash
#!/bin/bash

FILE=$1
if [[ `grep "$FILE" src/lib.rs | wc -l` -eq 0 ]]; then
    gsed -i -E "/CURRENT/c\const CURRENT: &str = \"$FILE\";" src/lib.rs
    if [[ `grep '::dir!(pub' src/lib.rs | wc -l` -eq 1 ]]; then
        gsed -i "s|::dir!(pub |::dir!(|" src/lib.rs
    else
        gsed -i "s|::dir!(|::dir!(pub |" src/lib.rs
    fi
fi

```

## 编写本地测试用例
把测试代码写在 `"// @lc code=end"` 后面，需要定义 Solution 结构体，可能还需要定义参数的结构体。

```
// @lc code=end
struct Solution;

#[test]
fn test_a() {
    // let res = Solution::is_valid(String::from("()[]{}"));
    // println!("RESUTL\t{:?}", res);
}
```

![-w340](https://image.ponder.work/mweb/2025-03-16---17420958075794.jpg)
