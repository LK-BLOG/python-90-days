# Day 10 挑战四：系统信息收集器 (★★★★☆)
# 要求: 收集文件系统和环境信息。


import os
import sys
import platform
import hashlib
from pathlib import Path
from datetime import datetime


class SystemInfo:
    """系统信息收集器。"""
    
    @staticmethod
    def get_platform_info():
        """获取平台信息。"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        }
    
    @staticmethod
    def get_disk_usage(path="."):
        """获取磁盘使用情况。
        
        Returns:
            dict: {"total": bytes, "used": bytes, "free": bytes, "percent": float}
        """
        # TODO: 获取磁盘空间信息
        pass
    
    @staticmethod
    def get_env_summary():
        """环境变量摘要。"""
        # TODO: 统计环境变量数量，筛选重要的
        pass
    
    @staticmethod
    def file_info(filepath):
        """获取文件详细信息。
        
        Returns:
            dict: {name, size, created, modified, permissions, md5}
        """
        # TODO: 收集文件元数据
        pass
    
    @staticmethod
    def dir_size(path):
        """递归计算目录大小。"""
        # TODO: 递归统计所有文件大小之和
        pass
    
    @staticmethod
    def permissions_summary(filepath):
        """文件权限摘要。"""
        pass


# ===== 测试 =====
if __name__ == "__main__":
    print("平台信息:", SystemInfo.get_platform_info())
    print("磁盘使用:", SystemInfo.get_disk_usage("."))
    info = SystemInfo.file_info("challenge01.py")
    print(f"文件信息: {info}")
