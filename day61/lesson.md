# Day 61: LLM 基础

## 1. LLM 本质
下一个 token 预测器，基于 Transformer 架构。

## 2. API 调用
```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"你好"}]
)
```

## 3. 参数
- temperature: 0确定, 0.7平衡, 1+创意
- max_tokens: 输出长度限制
- top_p: 核采样

## 4. Token
中文1-2 token/字, 英文4字符≈1 token

## 5. 流式输出
```python
stream = client.chat.completions.create(..., stream=True)
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
```
