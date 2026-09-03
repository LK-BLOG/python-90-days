# Day 83 示例 2: 断点续传执行器
import time

class MockTool:
    def __init__(self, name): self.name = name
    def __call__(self, **kw): return f'{self.name} 完成: {kw}'

class ResumableExecutor:
    def __init__(self, tools, cm):
        self.tools = tools; self.cm = cm
    
    def execute(self, cp):
        for i in range(cp.step_idx, len(cp.steps)):
            step = cp.steps[i]
            tool = self.tools.get(step.tool)
            if not tool:
                step.status = 'failed'; step.error = f'无工具: {step.tool}'; continue
            try:
                result = tool(**step.input_data)
                step.output = result; step.status = 'completed'
                cp.step_idx = i + 1
                self.cm.save(cp)
                print(f'  ✅ 步骤{i+1}: {result}')
            except Exception as e:
                step.status = 'failed'; step.error = str(e)
                self.cm.save(cp)
                print(f'  ❌ 步骤{i+1}: {e}')
        return '完成'

if __name__ == '__main__':
    from day83_examples_01 import CheckpointManager, AgentCP, StepCP
    tools = {'calc': MockTool('calc'), 'search': MockTool('search')}
    cm = CheckpointManager('/tmp/test_exec')
    cp = AgentCP('a1', 'executing', '测试', 0, [StepCP('s1','calc',{'expr':'1+1'}), StepCP('s2','search',{'q':'hi'})])
    cm.save(cp)
    executor = ResumableExecutor(tools, cm)
    print(executor.execute(cp))
    import shutil; shutil.rmtree('/tmp/test_exec')
