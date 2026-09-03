# Day 71: 微调基础

## 1. 何时微调 vs RAG
微调: 改行为/风格/格式 | RAG: 注入新知识

## 2. 数据格式(JSONL)
每行一个JSON: {"messages": [system, user, assistant]}

## 3. 流程
准备数据 -> 验证格式 -> 上传 -> 创建微调 -> 等待 -> 使用

## 4. 超参数
n_epochs, batch_size, learning_rate_multiplier

## 5. 注意事项
- 数据质量 > 数量
- 先小规模测试
- 监控过拟合
