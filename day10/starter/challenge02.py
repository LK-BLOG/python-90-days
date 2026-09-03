# Day 10 挑战二：目录分析器 (★★★☆☆)
# 要求: 统计和分析目录结构。


from pathlib import Path
from collections import Counter, defaultdict
import os


class DirectoryAnalyzer:
    """目录分析器 —— 统计文件数量、大小、类型分布。"""
    
    def __init__(self, path="."):
        self.path = Path(path)
        self._stats = {}
    
    def get_stats(self):
        """获取目录统计信息。
        
        Returns:
            dict: {
                "total_files": 文件总数,
                "total_dirs": 目录总数,
                "total_size": 总大小(字节),
                "by_extension": {".py": 10, ".txt": 5, ...},
                "by_size_range": {"<1KB": 50, "1KB-10KB": 20, ...},
                "largest_file": (路径, 大小),
                "newest_file": (路径, 修改时间),
                "oldest_file": (路径, 修改时间)
            }
        """
        # TODO: 递归遍历目录
        # TODO: 统计各项指标
        pass
    
    def _walk(self):
        """递归遍历目录。"""
        # TODO: 使用 Path.rglob("*") 遍历
        pass
    
    def generate_tree(self, max_depth=3, show_size=True):
        """生成目录树文本。
        
        示例:
            project/
            ├── src/
            │   ├── main.py  (2.3KB)
            │   └── utils.py (1.1KB)
            └── README.md  (0.5KB)
        """
        # TODO: 递归生成树形文本
        pass
    
    def find_large_files(self, min_size=1_000_000):
        """查找大文件。"""
        pass
    
    def find_empty_dirs(self):
        """查找空目录。"""
        pass
    
    def get_type_summary(self):
        """文件类型分布摘要。"""
        pass
    
    def format_size(self, size_bytes):
        """格式化文件大小。"""
        # TODO: 自动选择 B/KB/MB/GB 单位
        pass


# ===== 测试 =====
if __name__ == "__main__":
    analyzer = DirectoryAnalyzer("D:/Python-Learn-30-days/day10")
    print(f"统计: {analyzer.get_stats()}")
    print(f"\n目录树:\n{analyzer.generate_tree(max_depth=2)}")
