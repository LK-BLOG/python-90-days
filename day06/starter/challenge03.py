# Day 6 挑战三：上下文管理器 (★★★☆☆)
# 要求: 用 class 和 @contextmanager 实现上下文管理器。


from contextlib import contextmanager
import time
import os


class ManagedFile:
    """文件上下文管理器 —— 自动打开和关闭文件。
    
    用法:
        with ManagedFile("data.txt", "w") as f:
            f.write("hello")
    """
    def __init__(self, path, mode="r", encoding="utf-8"):
        # TODO: 保存参数，初始化文件句柄为 None
        pass
    
    def __enter__(self):
        # TODO: 打开文件并返回
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: 关闭文件，返回 False 让异常继续传播
        pass


class Timer:
    """计时上下文管理器 —— 测量代码块执行时间。"""
    def __init__(self, label="代码块"):
        # TODO: 保存标签
        pass
    
    def __enter__(self):
        # TODO: 记录开始时间
        pass
    
    def __exit__(self, *args):
        # TODO: 计算并打印耗时
        pass


class DatabaseTransaction:
    """模拟数据库事务上下文管理器。
    
    成功时提交，异常时回滚。
    """
    def __init__(self, db_name):
        # TODO: 初始化事务状态
        pass
    
    def __enter__(self):
        print(f"  BEGIN TRANSACTION on {self.db_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: 根据是否有异常决定 commit 还是 rollback
        pass
    
    def execute(self, sql):
        """执行 SQL（模拟）。"""
        # TODO: 记录操作
        pass


@contextmanager
def temporary_directory(prefix="tmp_"):
    """临时目录上下文管理器（用 @contextmanager 实现）。"""
    # TODO: 创建临时目录
    # TODO: yield 目录路径
    # TODO: 在 finally 中删除目录
    pass


@contextmanager
def suppress_errors(*exceptions):
    """异常抑制上下文管理器 —— 忽略指定异常。"""
    # TODO: try/except 捕获 exceptions，静默忽略
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # Timer 测试
    with Timer("求和"):
        total = sum(range(1_000_000))
    print(f"  结果: {total}")
    
    # 事务测试
    with DatabaseTransaction("users") as tx:
        tx.execute("INSERT INTO users VALUES (1, 'Alice')")
        tx.execute("UPDATE users SET name='Bob' WHERE id=1")
    
    # 临时目录测试
    with temporary_directory() as tmpdir:
        print(f"  临时目录: {tmpdir}")
        print(f"  目录存在: {os.path.exists(tmpdir)}")
    print(f"  目录已清理: {not os.path.exists(tmpdir)}")
