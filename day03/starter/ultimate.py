# Day 3 终极挑战：日志摘要工具

def clean_line(line):
    """清理一行日志。"""
    # TODO
    pass


def analyze_logs(text):
    """返回日志级别统计和错误内容。"""
    # TODO：遍历 splitlines() 的结果
    # 返回 {'总行数': 0, '级别统计': {}, '错误内容': []}
    pass


def build_summary(text):
    """把日志分析结果格式化成可读摘要。"""
    # TODO：调用 analyze_logs，不要重复统计逻辑
    pass


if __name__ == '__main__':
    logs = 'INFO user login\nERROR database timeout\nINFO retry success'
    print(build_summary(logs))
