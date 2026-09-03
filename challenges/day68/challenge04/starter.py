# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple

class RAGEvaluator:
    def __init__(self):
        self.weights = {
            'faithfulness': 0.25,
            'relevancy': 0.25,
            'precision': 0.25,
            'recall': 0.25
        }
    
    def faithfulness(self, answer: str, context: str) -> float:
        # TODO: 评估答案对上下文的忠实度
        pass
    
    def answer_relevancy(self, question: str, answer: str) -> float:
        # TODO: 评估答案与问题的相关性
        pass
    
    def context_precision(self, question: str, context: str) -> float:
        # TODO: 评估上下文的精准度
        pass
    
    def context_recall(self, context: str, reference: str) -> float:
        # TODO: 评估上下文的召回率
        pass
    
    def evaluate(self, test_case: Dict) -> Dict:
        # TODO: 综合评估
        pass
    
    def batch_evaluate(self, test_cases: List[Dict]) -> Dict:
        # TODO: 批量评估
        pass
