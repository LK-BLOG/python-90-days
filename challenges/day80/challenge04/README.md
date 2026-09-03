# Day 80 Challenge 4: 智能滑动窗口管理器 ⭐⭐⭐⭐
# 实现一个基于重要性的智能窗口

"""
实现一个SmartWindow类：
- 支持Token预算限制
- 基于重要性评分选择保留哪些消息
- 保护System Prompt不被裁剪
- 支持多种评分策略

重要性评分规则：
- 位置分：越新分数越高 (0.4权重)
- 角色分：user>system>assistant (0.3权重)
- 内容分：包含关键词加分 (0.3权重)
"""

from typing import List, Dict, Callable

class SmartWindow:
    def __init__(self, max_tokens: int, count_fn: Callable = None):
        self.max_tokens = max_tokens
        self.count_fn = count_fn or (lambda t: len(t) // 3)
        self.messages: List[Dict] = []

    def add(self, role: str, content: str):
        """添加消息"""
        pass

    def _score(self, msg: Dict, idx: int, total: int) -> float:
        """计算消息重要性分数"""
        # TODO: 实现评分逻辑
        pass

    def select(self) -> List[Dict]:
        """选择在Token预算内最重要的消息"""
        # TODO: 贪心选择 + 恢复时间顺序
        pass

    def get_messages(self) -> List[Dict]:
        return self.select()

    def stats(self) -> Dict:
        """返回窗口统计"""
        pass


if __name__ == "__main__":
    window = SmartWindow(max_tokens=500)
    # 模拟对话
   对话 = [
        ("system", "你是一个助手"),
        ("user", "你好"),
        ("assistant", "你好！"),
        ("user", "重要：明天有会议"),
        ("assistant", "记住了。"),
        ("user", "天气呢？"),
        ("assistant", "我无法查天气。"),
        ("user", "帮我总结之前的对话"),
    ]
    for role, content in 对话:
        window.add(role, content)

    selected = window.get_messages()
    print(f"选择 {len(selected)}/{len(window.messages)} 条消息")
    for m in selected:
        print(f"  [{m['role']}] {m['content'][:40]}")
