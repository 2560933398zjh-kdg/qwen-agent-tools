"""
实验5：工具调用智能体（学生版）

教师评测时只会调用 run_agent(question, api_key, model)
本文件还包含一个主入口，用于读取 student_questions.jsonl 并生成 lab5_result.jsonl
输出格式：每行 {"case_id": "...", "answer": ...}
"""

from __future__ import annotations

import json
import math
import os
import re
from typing import Dict, Union

# =============================================================================
# 工具区
# =============================================================================

def calculate_math_expression(expression: str) -> Union[int, float]:
    """
    安全计算数学表达式，支持 + - * / // % ** 括号以及常用数学函数。
    """
    safe_dict = {
        "abs": abs,
        "round": round,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "pi": math.pi,
        "e": math.e,
    }
    result = eval(expression, {"__builtins__": {}}, safe_dict)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def count_text_statistics(text: str) -> Dict[str, int]:
    """
    统计文本中的中文字符数、英文词数、总字符数。
    """
    chinese_chars = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    total_chars = len(text)
    return {
        "chinese_chars": chinese_chars,
        "english_words": english_words,
        "total_chars": total_chars,
    }


# =============================================================================
# 智能体主函数
# =============================================================================

def run_agent(
    question: str,
    api_key: str = "",
    model: str = "qwen3-8b",
) -> Union[int, float, Dict[str, int]]:
    """
    根据问题选择工具并返回结果。
    """
    # 判断是否为文本统计任务
    text_keywords = ["中文字符数", "英文词数", "总字符数", "统计下面文本"]
    if any(kw in question for kw in text_keywords):
        # 提取被统计的文本
        match = re.search(r'文本[：:]\s*["\'](.+?)["\']', question)
        if not match:
            match = re.search(r'文本[：:]\s*(.+?)(?:[。！？]|$)', question)
        if not match:
            match = re.search(r'["\'](.+?)["\']', question)
        if match:
            text = match.group(1)
        else:
            text = ""
        return count_text_statistics(text)

    # 否则视为数学计算任务
    expr = None
    match = re.search(r'计算表达式[：:]\s*(.+)', question)
    if match:
        expr = match.group(1).strip()
    else:
        match = re.search(r'调用数学计算工具[，,]\s*计算表达式[：:]\s*(.+)', question)
        if match:
            expr = match.group(1).strip()
        else:
            match = re.search(r'([\d\+\-\*\/\(\)\.\s\*\*\%//]+(?:sqrt|sin|cos|tan|log|abs|round)[\d\+\-\*\/\(\)\.\s]*)', question, re.I)
            if match:
                expr = match.group(1).strip()
            else:
                match = re.search(r'([\d\+\-\*\/\(\)\.\s\%\*\*/]+)', question)
                if match:
                    expr = match.group(1).strip()
    if expr is None:
        raise ValueError(f"无法从问题中提取数学表达式: {question}")

    expr = expr.replace("（", "(").replace("）", ")")
    expr = expr.rstrip("。？！.")
    return calculate_math_expression(expr)


# =============================================================================
# 主程序：读取 student_questions.jsonl，生成 lab5_result.jsonl
# =============================================================================

if __name__ == "__main__":
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "student_questions.jsonl")
    output_file = os.path.join(script_dir, "lab5_result.jsonl")

    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        exit(1)

    results = []  # 每个元素为 (case_id, answer)
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            case_id = data.get("case_id", "")
            question = data["question"]
            try:
                answer = run_agent(question)
            except Exception as e:
                answer = f"ERROR: {e}"
            results.append((case_id, answer))

    with open(output_file, "w", encoding="utf-8") as f:
        for case_id, ans in results:
            record = {"case_id": case_id, "answer": ans}
            # 确保字典中的 answer 如果是 dict 也能正确序列化
            line = json.dumps(record, ensure_ascii=False)
            f.write(line + "\n")

    print(f"已处理 {len(results)} 个问题，结果保存至 {output_file}")