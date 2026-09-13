# App Inventor 项目工具集

针对 **MIT App Inventor（.aia）项目** 的分析、提取、生成与修复脚本集合。App Inventor 项目本质上是 zip 压缩包，其中 `.bky` 为积木逻辑（Blocks）文件、`project.properties` 为工程配置。

## 项目简介

该目录包含若干用于操作 `.aia` 文件的 Python 工具脚本，以及几个 `.aia` 示例项目（登录页、智能 AI 应用、弹球游戏）。主要用途：

- 从 `.aia` 压缩包中提取 `.bky` 积木文件以便分析；
- 按 App Inventor 工程格式自动生成 `.aia` 项目（如登录页 LoginPage.aia）；
- 对生成的工程文件进行清理与修复。

## 目录结构

```
appinventor/
├── extract_bky.py           # 从 .aia 中提取指定 Screen 的 .bky 文件
├── generate_login_v7.py     # 生成 LoginPage.aia（v7 最终版）
├── main.py                  # PyCharm 默认模板（占位）
├── _clean.py / _clean2.py / _clean3.py / _fix.py  # 工程清理/修复脚本
├── 一键分析并修复.bat        # Windows 一键脚本
├── 分析弹球游戏.bat          # Windows 一键脚本
├── LoginPage.aia            # 登录页 App Inventor 项目
├── SmartAI.aia              # 智能 AI 应用项目
├── 弹球游戏.aia             # 弹球游戏示例项目
└── docs/                    # 说明文档（当前为空）
```

## 主要脚本说明

| 脚本 | 功能 |
| --- | --- |
| `extract_bky.py` | 读取 `SmartAI.aia`，解压出 `Screen4.bky` 积木文件 |
| `generate_login_v7.py` | 依据 App Inventor 工程规范（YaVersion 219、XML 格式 BKY 等）生成登录页项目 |
| `_clean.py` 系列 | 对生成/修改后的项目文件做清理处理 |
| `_fix.py` | 修复工程文件中的格式或结构问题 |

## 运行方式

```bash
# 提取 .bky 积木文件
python extract_bky.py

# 生成登录页项目
python generate_login_v7.py
```

## 备注

- `.aia` 文件可通过 MIT App Inventor 或国内镜像（如 广工在线）导入预览。
- 生成脚本基于对示例项目（弹球游戏）的逆向分析结果编写，格式与 App Inventor 标准兼容。
