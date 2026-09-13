# 工具调用智能体（学生版，student-agent）

教学实验项目：**实验5 —— 工具调用智能体（学生版）**。实现一个带多个内置工具的智能体，能够批量读取题目文件并生成作答结果，供教师评测。

## 项目简介

该智能体支持通过 `run_agent(question, api_key, model)` 接口调用，内置安全数学计算、文本统计等工具。主入口读取 `student_questions.jsonl` 中的题目，逐个作答后输出 `lab5_result.jsonl`。

## 技术栈

- Python 标准库为主
- 大模型 API（通义千问，需传入 `api_key`）

## 目录结构

```
student-agent/
├── student_agent.py          # 智能体主程序（工具定义 + 批量作答入口）
├── student_questions.jsonl   # 题目文件（输入）
├── lab5_result.jsonl         # 作答结果（输出，每行 {"case_id": ..., "answer": ...}）
└── lab5_result.zip           # 结果压缩包
```

## 运行方式

```bash
python student_agent.py
```

或按评测要求调用：

```python
from student_agent import run_agent
answer = run_agent(question, api_key, model)
```

## 内置工具

| 工具 | 说明 |
| --- | --- |
| `calculate_math_expression` | 安全数学表达式计算（`eval` 受限环境，支持四则运算、幂、取模及常用数学函数） |
| `count_text_statistics` | 文本统计（字数、字符数等） |

## 输出格式

`lab5_result.jsonl` 每行一条 JSON：`{"case_id": "...", "answer": ...}`
