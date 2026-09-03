# Day 10 挑战三：文件整理工具 (★★★★☆)
# 要求: 按规则整理文件（分类、去重、清理）。


from pathlib import Path
import os
import hashlib
import shutil
import time
from collections import defaultdict
from datetime import datetime


class FileOrganizer:
    """文件整理工具 —— 按扩展名/日期分类，查找重复。"""
    
    # 扩展名 -> 分类名 映射
    DEFAULT_CATEGORIES = {
        "文档": [".doc", ".docx", ".pdf", ".txt", ".md", ".rtf"],
        "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
        "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "代码": [".py", ".js", ".java", ".cpp", ".c", ".go", ".rs"],
        "压缩包": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "数据": [".json", ".csv", ".xml", ".yaml", ".yml", ".sql"],
    }
    
    def __init__(self, source_dir, categories=None):
        self.source = Path(source_dir)
        self.categories = categories or self.DEFAULT_CATEGORIES
        self._actions = []  # 记录操作历史
    
    def classify_by_extension(self, dry_run=True):
        """按扩展名分类文件到子目录。
        
        Args:
            dry_run: True 只模拟不实际移动
        """
        # TODO: 遍历文件，按扩展名找分类，移动/记录
        pass
    
    def classify_by_date(self, dry_run=True):
        """按修改日期分类（年/月 子目录）。"""
        pass
    
    def find_duplicates(self, by_content=True):
        """查找重复文件。
        
        Args:
            by_content: True 按内容哈希，False 按文件名+大小
        
        Returns:
            dict: {hash: [filepath1, filepath2, ...]}（只返回有重复的）
        """
        # TODO: 计算哈希，分组
        pass
    
    def remove_duplicates(self, keep="newest", dry_run=True):
        """删除重复文件。
        
        Args:
            keep: "newest"/"oldest"/"largest"/"smallest"
        """
        pass
    
    def clean_empty_dirs(self, dry_run=True):
        """清理空目录。"""
        pass
    
    def archive_old_files(self, days=365, archive_dir="archive", dry_run=True):
        """归档旧文件。"""
        pass
    
    def get_preview(self):
        """返回整理预览（不实际操作）。"""
        pass
    
    def _calc_hash(self, filepath, chunk_size=8192):
        """计算文件内容 MD5。"""
        h = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                h.update(chunk)
        return h.hexdigest()
    
    def _log_action(self, action, src, dst=None):
        """记录操作。"""
        self._actions.append({"action": action, "src": str(src), "dst": str(dst), "time": datetime.now().isoformat()})


# ===== 测试 =====
if __name__ == "__main__":
    organizer = FileOrganizer("D:/Python-Learn-30-days/day10")
    preview = organizer.get_preview()
    print("整理预览:")
    for category, files in preview.items():
        print(f"  {category}: {len(files)} 个文件")
