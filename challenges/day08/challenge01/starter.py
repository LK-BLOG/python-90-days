# challenge01/starter.py - 日志分析器骨架
import re
from collections import Counter
from datetime import datetime

class LogAnalyzer:
    """日志文件分析器"""
    
    def __init__(self, log_file):
        """
        初始化分析器
        
        参数:
            log_file (str): 日志文件路径
        """
        # TODO: 设置日志文件路径
        # TODO: 初始化日志列表
        pass
    
    def parse_line(self, line):
        """
        解析单行日志
        
        参数:
            line (str): 日志行
        
        返回:
            dict: 解析后的日志字典
        """
        # TODO: 定义日志格式正则表达式
        # TODO: 匹配日志行
        # TODO: 提取时间、级别、消息
        pass
    
    def parse(self):
        """解析整个日志文件"""
        # TODO: 打开日志文件
        # TODO: 逐行解析
        # TODO: 存储解析结果
        pass
    
    def get_statistics(self):
        """获取统计信息"""
        # TODO: 按级别统计
        # TODO: 按时间统计
        # TODO: 返回统计字典
        pass
    
    def search(self, keyword=None, level=None, start_time=None, end_time=None):
        """搜索日志"""
        # TODO: 实现关键词搜索
        # TODO: 实现级别过滤
        # TODO: 实现时间范围搜索
        pass
    
    def export_report(self, output_file):
        """导出分析报告"""
        # TODO: 生成报告内容
        # TODO: 写入文件
        pass

# 测试代码
if __name__ == "__main__":
    # 创建测试日志
    test_log = "test.log"
    with open(test_log, 'w', encoding='utf-8') as f:
        f.write("2024-01-15 10:30:00 [INFO] Application started\n")
        f.write("2024-01-15 10:30:05 [ERROR] Connection failed\n")
        f.write("2024-01-15 10:31:00 [INFO] Retrying connection\n")
    
    # 分析日志
    analyzer = LogAnalyzer(test_log)
    analyzer.parse()
    
    print("统计信息:", analyzer.get_statistics())
    print("错误日志:", analyzer.search(level="ERROR"))
    
    # 清理
    import os
    os.unlink(test_log)
