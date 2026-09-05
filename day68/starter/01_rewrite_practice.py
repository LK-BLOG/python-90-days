# -*- coding: utf-8 -*-
"""Day 68：查询改写与问题分解。"""
class RewritePractice:
    def rewrite(self, query: str) -> list[str]:
        """生成多个等价查询，提升召回率。"""
        if not query.strip(): raise ValueError("问题不能为空")
        # TODO：实现同义改写、关键词提取和去重
        return [query.strip()]
    def decompose(self, query: str) -> list[str]:
        """将复杂问题拆成可独立检索的子问题。"""
        # TODO：识别并列条件、时间条件和因果关系
        return [part.strip() for part in query.split("；") if part.strip()]
if __name__ == "__main__": print(RewritePractice().decompose("A是什么；B有什么区别"))
