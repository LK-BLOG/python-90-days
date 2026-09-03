# Day 80 Challenge 1: Token计数器 ⭐
# 实现一个精确的Token计数器

class TokenCounter:
    """
    支持多种分词方式的Token计数器
    """

    def __init__(self, method: str = "approximate"):
        """
        初始化计数器
        method: "approximate" | "tiktoken"
        """
        self.method = method
        # TODO: 如果method是tiktoken，初始化编码器

    def count(self, text: str) -> int:
        """计算Token数"""
        # TODO: 根据method选择计数方式
        pass

    def remaining(self, used: int, budget: int = 4096) -> int:
        """计算剩余可用Token"""
        # TODO
        pass

    def fits_budget(self, text: str, budget: int = 4096) -> bool:
        """检查文本是否在预算内"""
        # TODO
        pass


# 测试
if __name__ == "__main__":
    counter = TokenCounter("approximate")
    test = "Hello, world! 你好世界！"
    print(f"Token数: {counter.count(test)}")
    print(f"4096预算内: {counter.fits_budget(test)}")
    print(f"剩余: {counter.remaining(counter.count(test))}")
