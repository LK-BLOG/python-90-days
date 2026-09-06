# Day 3 挑战五：日志分析

def analyze_logs(text):
    """统计多行日志中 INFO、WARNING、ERROR 的数量。"""
    result = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    # TODO：按行遍历；取每行第一个单词作为级别
    # TODO：遇到未知级别时跳过
    return result

if __name__ == '__main__':
    logs = 'INFO start\nERROR timeout\nINFO retry'
    print(analyze_logs(logs))
