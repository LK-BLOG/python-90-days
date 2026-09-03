# file_handler.py - 文件处理器骨架
# 请根据挑战要求完善这个文件

import os
from pathlib import Path

class FileHandler:
    """文件处理器，提供各种文件操作功能"""
    
    def __init__(self, base_dir="."):
        """
        初始化文件处理器
        
        参数:
            base_dir (str): 基础目录
        """
        # TODO: 设置基础目录
        # TODO: 创建目录（如果不存在）
        pass
    
    def read_file(self, filename, encoding='utf-8'):
        """
        读取文件内容
        
        参数:
            filename (str): 文件名
            encoding (str): 编码
        
        返回:
            str: 文件内容
        """
        # TODO: 检查文件是否存在
        # TODO: 读取文件内容
        # TODO: 处理异常
        pass
    
    def write_file(self, filename, content, encoding='utf-8', mode='w'):
        """
        写入文件内容
        
        参数:
            filename (str): 文件名
            content (str): 内容
            encoding (str): 编码
            mode (str): 写入模式
        
        返回:
            bool: 是否成功
        """
        # TODO: 确保目录存在
        # TODO: 写入文件
        # TODO: 处理异常
        pass
    
    def append_file(self, filename, content, encoding='utf-8'):
        """
        追加内容到文件
        
        参数:
            filename (str): 文件名
            content (str): 要追加的内容
            encoding (str): 编码
        
        返回:
            bool: 是否成功
        """
        # TODO: 追加写入
        pass
    
    def copy_file(self, src, dst, encoding='utf-8'):
        """
        复制文件
        
        参数:
            src (str): 源文件
            dst (str): 目标文件
            encoding (str): 编码
        
        返回:
            bool: 是否成功
        """
        # TODO: 读取源文件
        # TODO: 写入目标文件
        pass
    
    def backup_file(self, filename):
        """
        备份文件
        
        参数:
            filename (str): 要备份的文件
        
        返回:
            str: 备份文件名
        """
        # TODO: 生成备份文件名
        # TODO: 复制文件
        pass
    
    def get_file_info(self, filename):
        """
        获取文件信息
        
        参数:
            filename (str): 文件名
        
        返回:
            dict: 文件信息
        """
        # TODO: 获取文件大小
        # TODO: 获取修改时间
        # TODO: 返回信息字典
        pass

# 测试代码
if __name__ == "__main__":
    # 创建处理器
    handler = FileHandler("test_files")
    
    # 测试写入
    success = handler.write_file("test.txt", "Hello, World!")
    print(f"写入文件: {'成功' if success else '失败'}")
    
    # 测试读取
    content = handler.read_file("test.txt")
    print(f"读取内容: {content}")
    
    # 测试备份
    backup_name = handler.backup_file("test.txt")
    print(f"备份文件: {backup_name}")
    
    # 获取文件信息
    info = handler.get_file_info("test.txt")
    print(f"文件信息: {info}")
    
    # 清理
    import shutil
    if os.path.exists("test_files"):
        shutil.rmtree("test_files")
