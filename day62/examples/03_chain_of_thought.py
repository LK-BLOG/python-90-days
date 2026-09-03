# -*- coding: utf-8 -*-
# Chain-of-Thought
def cot_prompt(question):
    result = "请一步一步思考。

"
    result += "问题: " + question + "

"
    result += "让我一步步分析：
"
    result += "1. 理解题意
2. 列出条件
3. 推理计算
4. 验证答案

答案:"
    return result

def compare_approaches():
    print("=== Zero-shot ===")
    print("净速度: 3-1=2吨/时, 时间: 20/2=10小时")
    print()
    print("=== CoT ===")
    print("1. 进水: 3吨/时")
    print("2. 出水: 1吨/时")
    print("3. 净: 3-1=2吨/时")
    print("4. 20/2=10小时")
    print("5. 验证: 10h进30出10剩20 OK")

if __name__ == "__main__":
    print(cot_prompt("一个水池问题..."))
    print()
    compare_approaches()
