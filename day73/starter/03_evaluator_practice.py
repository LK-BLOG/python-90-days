# -*- coding: utf-8 -*-
"""Day 73：离线评估模型输出。"""
from typing import Callable, Any
class EvaluatorPractice:
    def evaluate(self, model_func: Callable[[str], str], test_cases: list[dict[str, Any]]) -> dict[str, Any]:
        """运行测试集，收集输出、得分和失败案例。"""
        results=[]
        for case in test_cases:
            question=case.get("question",""); expected=case.get("expected","")
            actual=model_func(question)
            results.append({"question":question,"expected":expected,"actual":actual,"exact":actual==expected})
        # TODO：加入相关性、事实性、延迟和成本指标
        return {"total":len(results),"passed":sum(x["exact"] for x in results),"results":results}
    def compare(self, model_a: Callable[[str],str], model_b: Callable[[str],str], test_cases: list[dict[str,Any]]) -> dict[str,Any]:
        """在同一测试集上比较两个模型，避免凭感觉选模型。"""
        # TODO：输出逐题差异和统计显著性
        return {"a":self.evaluate(model_a,test_cases),"b":self.evaluate(model_b,test_cases)}
if __name__ == "__main__": print(EvaluatorPractice().evaluate(lambda q:q,[{"question":"x","expected":"x"}]))
