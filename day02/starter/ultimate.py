# Day 2 Boss 挑战：数据管道处理系统 (★★★★★)
# 难度: ★★★★★
# 要求: 用函数组合实现数据流式处理。


class Pipeline:
    """数据管道 —— 支持函数组合的流式数据处理。
    
    功能说明:
        将多个处理步骤（函数）串联起来，数据从入口流入，
        依次经过每个步骤处理后从出口流出。
    
    用法:
        >>> pipe = Pipeline()
        >>> pipe.add_step("过滤", lambda data: [x for x in data if x > 0])
        >>> pipe.add_step("翻倍", lambda data: [x * 2 for x in data])
        >>> pipe.execute([-2, -1, 0, 1, 2, 3])
        [2, 4, 6]
    
    支持特性:
        - add_step(name, func): 添加处理步骤
        - execute(data): 执行管道
        - add_steps(*steps): 批量添加步骤
        - insert_step(index, name, func): 在指定位置插入步骤
        - remove_step(name): 按名称移除步骤
        - get_steps(): 获取所有步骤信息
        - 链式调用
    """
    
    def __init__(self):
        """初始化空管道。"""
        # TODO: 初始化步骤列表
        # 提示: self._steps = []  # [(name, func)]
        self._steps = []
    
    def add_step(self, name, func):
        """添加一个处理步骤。
        
        Args:
            name: 步骤名称（唯一标识）
            func: 处理函数，接收数据并返回处理后的数据
        
        Returns:
            self: 返回自身，支持链式调用
        
        Raises:
            ValueError: 当步骤名称已存在时
        """
        # TODO: 检查名称唯一性
        # TODO: 添加到步骤列表
        pass
    
    def insert_step(self, index, name, func):
        """在指定位置插入一个处理步骤。
        
        Args:
            index: 插入位置（0-based）
            name: 步骤名称
            func: 处理函数
        """
        # TODO: 在指定位置插入步骤
        pass
    
    def remove_step(self, name):
        """按名称移除一个处理步骤。
        
        Args:
            name: 要移除的步骤名称
        
        Raises:
            KeyError: 当步骤不存在时
        """
        # TODO: 按名称查找并移除
        pass
    
    def execute(self, data):
        """执行管道，数据依次经过所有步骤。
        
        Args:
            data: 输入数据
        
        Returns:
            处理后的数据（类型取决于管道中的函数）
        """
        # TODO: 遍历所有步骤，将上一步的输出作为下一步的输入
        pass
    
    def get_steps(self):
        """获取管道中所有步骤的信息。
        
        Returns:
            list of dict: 每个步骤的名称和描述
        """
        # TODO: 返回步骤信息列表
        pass
    
    def __repr__(self):
        """返回管道的可读表示。"""
        step_names = [s[0] for s in self._steps]
        return f"Pipeline({' -> '.join(step_names)})"


# ===== 流式数据处理工具函数 =====

def chunk(data, size):
    """将数据按指定大小分块。
    
    Args:
        data: 可迭代对象
        size: 每块的大小
    
    Returns:
        list of list: 分块后的数据
    """
    # TODO: 实现分块逻辑
    pass


def flatten(data):
    """展平嵌套列表。
    
    Args:
        data: 嵌套列表
    
    Returns:
        list: 展平后的一维列表
    """
    # TODO: 递归展平
    pass


def deduplicate(data, key=None):
    """数据去重（保持顺序）。
    
    Args:
        data: 可迭代对象
        key: 去重键函数（可选）
    
    Returns:
        list: 去重后的列表
    """
    # TODO: 使用 dict（或 set）保持顺序去重
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 构建数据处理管道
    pipe = (Pipeline()
        .add_step("筛选正数", lambda data: [x for x in data if x > 0])
        .add_step("平方", lambda data: [x ** 2 for x in data])
        .add_step("求和", lambda data: sum(data))
    )
    
    result = pipe.execute([-5, -3, 1, 2, 3, 4, 5])
    print(f"管道结果: {result}")  # 期望: 1+4+9+16+25 = 55
    print(f"管道: {pipe}")
    
    # 测试分块
    print(f"分块: {chunk([1,2,3,4,5,6,7], 3)}")  # [[1,2,3],[4,5,6],[7]]
    
    # 测试展平
    print(f"展平: {flatten([[1,2],[3,[4,5]],6]))}")  # [1,2,3,4,5,6]
