# 挑战四：RAG评估器

## 难度
★★★★☆

## 项目名
RAGEvaluator - RAG系统评估器

## 目标
实现RAG系统的自动评估工具，评估答案质量和检索效果。

## 背景
RAG系统需要客观评估指标。本挑战让你实现类似Ragas的评估功能。

## 功能要求
1. **Faithfulness评估**：答案是否忠于检索到的上下文
2. **Answer Relevancy评估**：答案是否回答了问题
3. **Context Precision评估**：检索到的上下文是否精准
4. **Context Recall评估**：是否检索到了所有相关信息

## 输入
- 测试用例列表（问题、答案、上下文、参考答案）
- 评估指标配置

## 输出
- 各指标的得分
- 综合评估报告

## 限制条件
- 纯Python实现
- 不依赖外部评估库
- 支持中文评估

## 示例
`python
evaluator = RAGEvaluator()
test_case = {
    "question": "Python是什么？",
    "answer": "Python是解释型编程语言",
    "context": "Python是解释型语言，由Guido创建",
    "reference": "Python是高级编程语言"
}
scores = evaluator.evaluate(test_case)
# 返回 {'faithfulness': 0.9, 'relevancy': 0.85, ...}
`

## 验收标准
- [ ] Faithfulness评估逻辑正确
- [ ] Answer Relevancy评估准确
- [ ] Context Precision计算正确
- [ ] Context Recall评估完整
- [ ] 代码有中文注释

## 可选扩展
- 支持批量评估
- 添加评估可视化
- 实现评估基准
