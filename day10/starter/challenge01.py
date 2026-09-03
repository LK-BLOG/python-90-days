# Day 10 挑战一：路径操作工具 (★★★☆☆)
# 要求: 掌握 pathlib 的路径操作。


from pathlib import Path, PureWindowsPath, PurePosixPath
import os


class PathHelper:
    """路径操作工具类。"""
    
    @staticmethod
    def join_safe(*parts):
        """安全拼接路径（处理空部分和特殊字符）。"""
        # TODO: 过滤空 parts，用 Path / 拼接
        pass
    
    @staticmethod
    def make_relative(filepath, base_dir):
        """计算相对路径。"""
        # TODO: 使用 Path.relative_to() 或 os.path.relpath
        pass
    
    @staticmethod
    def normalize(filepath):
        """规范化路径（解析 .. 和 .）。"""
        # TODO: 返回 resolve() 的结果
        pass
    
    @staticmethod
    def ensure_dir(filepath):
        """确保文件所在目录存在。"""
        # TODO: filepath.parent.mkdir(parents=True, exist_ok=True)
        pass
    
    @staticmethod
    def get_extension(filepath, lower=True):
        """获取文件扩展名（不含点号）。"""
        # TODO: 返回 Path.suffix 去掉点号
        pass
    
    @staticmethod
    def rename_safe(filepath, new_name):
        """安全重名（处理重名冲突）。"""
        # TODO: 如果目标已存在，自动加序号
        pass
    
    @staticmethod
    def walk_up(filepath):
        """从 filepath 向上遍历所有父目录。"""
        # TODO: yield 每个 parent 直到根目录
        pass
    
    @staticmethod
    def find_file(filename, start_dir="."):
        """从 start_dir 向上查找文件。"""
        # TODO: 逐层向上查找
        pass


# ===== 测试 =====
if __name__ == "__main__":
    p = Path("documents/reports/../data/./file.txt")
    print(f"原始: {p}")
    print(f"规范化: {PathHelper.normalize(p)}")
    print(f"扩展名: {PathHelper.get_extension('archive.tar.gz')}")
    print(f"父目录: {PathHelper.ensure_dir('a/b/c/test.txt')}")
    
    print("\n向上遍历:")
    for parent in PathHelper.walk_up(Path("a/b/c/d")):
        print(f"  {parent}")
