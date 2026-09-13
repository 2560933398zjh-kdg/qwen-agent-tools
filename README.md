# Qwen — 项目集合总览

`D:\pycharm\Qwen` 是一个项目集合目录，包含 3 个独立子项目，主要围绕通义千问（Qwen）大模型与教学实验等方向：

| 子目录 | 项目 | 一句话说明 |
| --- | --- | --- |
| `appinventor/` | App Inventor 项目工具集 | 分析、生成、修复 MIT App Inventor（.aia）项目的脚本集合 |
| `HMuserproject/` | 验证码登录演示（Flask） | 图形验证码 + 短信验证码登录流程演示，鸿蒙课程对接版 |
| `student-agent/` | 工具调用智能体（学生版） | 教学实验：带数学计算/文本统计等工具的智能体，批量作答并输出结果 |

> 原集合中的 `finalwork`（家庭理财 AI 问答）、`search-RAG`（保险条款 RAG）、`Speechsignal`（语音去噪）已拆分为独立仓库，分别位于 `D:\pycharm\finance-qa`、`D:\pycharm\insurance-rag`、`D:\pycharm\speech-signal`。

各子项目均有独立的 `README.md`，详见对应目录。

## 公共说明

- 多数子项目依赖 `qwen_agent`、`dashscope` 等包，调用通义千问模型需配置 DashScope API Key。
- 各子项目相互独立，均位于 `.venv` 虚拟环境之外可独立运行（部分项目自含 `.venv`）。
