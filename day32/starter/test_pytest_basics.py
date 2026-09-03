"""Challenge 1: pytest fixture 和 parametrize - 骨架代码"""

import pytest


# TODO: 实现以下函数
def is_palindrome(text: str) -> bool:
    \"\"\"判断是否是回文 - TODO: 实现\"\"\"
    pass


def fizzbuzz(n: int) -> str:
    \"\"\"FizzBuzz - TODO: 实现\"\"\"
    # 3的倍数返回Fizz，5的倍数返回Buzz，15的倍数返回FizzBuzz
    # 其他返回数字字符串
    pass


def flatten(lst: list) -> list:
    \"\"\"扁平化嵌套列表 - TODO: 实现\"\"\"
    # flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
    pass


# === TODO: 编写以下测试 ===

# 1. 用 @pytest.mark.parametrize 测试 is_palindrome
#    至少 5 个用例（包括空字符串、单字符、正常回文、非回文、大小写混合）

# 2. 用 @pytest.mark.parametrize 测试 fizzbuzz
#    至少 5 个用例

# 3. 用 fixture 提供测试数据测试 flatten

# 4. 用 @pytest.mark.slow 标记一个性能测试

# 5. 用 @pytest.mark.skipif 跳过不支持的平台测试


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
