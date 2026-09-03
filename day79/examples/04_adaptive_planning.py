# Day 79 示例 4: 自适应规划
class AdaptivePlanner:
    def __init__(self):
        self.plan_history = []
    
    def replan(self, failed_task, error, remaining_tasks):
        print(f'🔄 重新规划: {failed_task.desc} 失败')
        alt_tools = {'search': 'fallback_search', 'api': 'manual'}
        alt = alt_tools.get(failed_task.tool)
        if alt:
            failed_task.tool = alt
            failed_task.status = 'pending'
            print(f'  替换工具: {failed_task.tool} → {alt}')
            return True
        # 跳过
        failed_task.result = f'跳过: {error}'
        return False

if __name__ == '__main__':
    from day79_examples_02 import Task
    p = AdaptivePlanner()
    t = Task('t1', '搜索数据', 'search')
    t.status = 'failed'
    p.replan(t, 'API 超时', [])
    print(f'  重试状态: {t.status}, 工具: {t.tool}')
