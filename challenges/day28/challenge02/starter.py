"""
Challenge 02: 并发计算器 - AsyncCalculator
"""
import asyncio
import time
from typing import List, Callable, Any
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor


@dataclass
class TaskResult:
    """任务结果"""
    task_id: int
    result: Any = None
    error: str = None
    elapsed: float = 0.0


class AsyncCalculator:
    """并发计算器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[TaskResult] = []
    
    async def compute(self, func: Callable, *args, task_id: int = 0) -> TaskResult:
        """执行单个计算"""
        # TODO: 实现
        # - 记录开始时间
        # - 执行函数
        # - 记录结果和耗时
        pass
    
    async def compute_all(self, func: Callable, args_list: List[tuple]) -> List[TaskResult]:
        """并发执行多个计算"""
        # TODO: 实现
        # - 使用 Semaphore 限制并发
        # - gather 执行所有任务
        pass
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        # TODO: 实现
        # - 总任务数
        # - 成功/失败数
        # - 平均耗时
        pass


if __name__ == "__main__":
    async def main():
        calc = AsyncCalculator(max_workers=3)
        
        # 示例：并发计算
        def slow_square(x):
            time.sleep(0.1)
            return x ** 2
        
        args_list = [(i,) for i in range(10)]
        results = await calc.compute_all(slow_square, args_list)
        
        print(f"完成 {len(results)} 个计算")
        print(f"统计: {calc.get_stats()}")
    
    asyncio.run(main())
