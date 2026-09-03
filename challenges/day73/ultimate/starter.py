# -*- coding: utf-8 -*-
class RAGEvalScheme:
    def __init__(self, rag_system):
        self.rag = rag_system
        self.test_cases = []
    def add_test(self, question, expected_answer, relevant_docs):
        # TODO
        pass
    def evaluate_retrieval(self):
        # TODO: 评估检索质量
        pass
    def evaluate_generation(self):
        # TODO: 评估生成质量
        pass
    def full_report(self):
        # TODO: 完整评估报告
        pass
