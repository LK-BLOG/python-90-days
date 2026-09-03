# Day 80 示例 2: 自我纠正循环
class SelfCorrection:
    def __init__(self, max_corrections=3):
        self.max_corrections = max_corrections
    
    def run(self, task: str) -> str:
        output = f'初始输出: {task}'
        for round in range(self.max_corrections):
            issues = self._check(output, task)
            if not issues:
                print(f'✅ 第{round+1}轮检查通过')
                return output
            print(f'⚠️ 发现问题: {issues}')
            output = self._correct(output, issues, task)
        return output
    
    def _check(self, output: str, task: str) -> list:
        issues = []
        if 'TODO' in output: issues.append('包含TODO')
        if len(output) < 20: issues.append('太简短')
        return issues
    
    def _correct(self, output: str, issues: list, task: str) -> str:
        return f'修正后: {task} (已修正{len(issues)}个问题)'

if __name__ == '__main__':
    sc = SelfCorrection()
    print(sc.run('生成报告'))
