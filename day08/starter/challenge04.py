# Day 8 挑战四：文件备份工具 (★★★★☆)
# 要求: 实现文件备份、校验、恢复。


import os
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path


class BackupManager:
    """文件备份管理器。
    
    功能:
        - 备份文件/目录
        - 校验完整性 (MD5)
        - 恢复文件
        - 列出备份历史
    """
    
    def __init__(self, backup_dir=".backups"):
        self.backup_dir = Path(backup_dir)
        self._manifest = {}  # {backup_id: {文件信息}}
    
    def backup(self, source, name=None):
        """备份文件或目录。
        
        Args:
            source: 源路径
            name: 备份名称（可选，默认用时间戳）
        
        Returns:
            str: 备份 ID
        """
        # TODO: 生成备份ID
        # TODO: 复制文件到备份目录
        # TODO: 计算校验和
        # TODO: 写入 manifest
        pass
    
    def restore(self, backup_id, target_dir=None):
        """恢复备份。"""
        # TODO: 从备份目录复制回原位置或指定目录
        # TODO: 验证校验和
        pass
    
    def verify(self, backup_id):
        """验证备份完整性。"""
        # TODO: 重新计算校验和并对比 manifest
        pass
    
    def list_backups(self):
        """列出所有备份。"""
        # TODO: 从 manifest 返回备份列表
        pass
    
    def cleanup(self, keep_last=5):
        """清理旧备份，只保留最近 N 个。"""
        pass
    
    def _calc_checksum(self, filepath):
        """计算文件 MD5 校验和。"""
        h = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()


# ===== 测试 =====
if __name__ == "__main__":
    # 创建测试文件
    test_dir = "_test_backup_src"
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "data.txt"), "w") as f:
        f.write("测试数据")
    
    bm = BackupManager("_test_backups")
    bid = bm.backup(test_dir, name="test_backup")
    print(f"备份ID: {bid}")
    print(f"校验: {bm.verify(bid)}")
    print(f"列表: {bm.list_backups()}")
    
    # 清理
    shutil.rmtree(test_dir, ignore_errors=True)
    shutil.rmtree("_test_backups", ignore_errors=True)
