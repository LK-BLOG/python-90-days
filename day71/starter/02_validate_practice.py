# -*- coding: utf-8 -*-
"""Day 71：训练数据集验证与质量评分。"""
from typing import Any
class ValidatePractice:
    def validate(self, data: list[dict[str, Any]]) -> list[str]:
        """返回所有格式错误，不在遇到第一条错误时停止。"""
        errors=[]
        for i,item in enumerate(data):
            if not isinstance(item, dict): errors.append(f"第{i}条不是对象"); continue
            if "messages" not in item: errors.append(f"第{i}条缺少messages")
            elif not isinstance(item["messages"], list): errors.append(f"第{i}条messages不是列表")
        # TODO：检查角色顺序、长度、重复样本和敏感信息
        return errors
    def check_quality(self, data: list[dict[str, Any]]) -> dict[str, float]:
        """返回完整率、重复率等质量指标。"""
        errors=self.validate(data)
        # TODO：增加长度分布、平衡性和可学习性指标
        return {"count": float(len(data)), "valid_rate": (len(data)-len(errors))/len(data) if data else 0.0}
if __name__ == "__main__": print(ValidatePractice().check_quality([]))
