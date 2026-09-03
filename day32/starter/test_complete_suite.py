\"\"\"Challenge 3-5: 完整测试套件骨架\"\"\"


class TaskManager:
    \"\"\"任务管理器 - 被测对象\"\"\"

    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def add(self, title: str, priority: int = 0) -> dict:
        \"\"\"添加任务 - TODO: 实现\"\"\"
        pass

    def get(self, task_id: int) -> dict | None:
        \"\"\"获取任务 - TODO: 实现\"\"\"
        pass

    def complete(self, task_id: int) -> bool:
        \"\"\"完成任务 - TODO: 实现\"\"\"
        pass

    def delete(self, task_id: int) -> bool:
        \"\"\"删除任务 - TODO: 实现\"\"\"
        pass

    def list_all(self, status: str = None) -> list:
        \"\"\"列出任务 - TODO: 实现\"\"\"
        pass

    def search(self, keyword: str) -> list:
        \"\"\"搜索任务 - TODO: 实现\"\"\"
        pass


# === TODO: 编写完整测试 ===
# 要求:
# 1. 每个方法至少 3 个测试（正常/异常/边界）
# 2. 使用 fixture 创建 TaskManager
# 3. parametrize 测试优先级
# 4. 测试覆盖率 > 80%
# 5. 测试独立，无执行顺序依赖


if __name__ == "__main__":
    print("Run with: pytest test_complete_suite.py -v --cov")
