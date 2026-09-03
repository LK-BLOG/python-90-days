# Day 79 测试
def test_task_creation():
    from day79_starter import Task, TaskStatus
    t = Task('t1', 'test')
    assert t.status == TaskStatus.PENDING
    print('✅ Task 创建通过')

def test_plan_ready():
    # TODO: 测试 get_ready 逻辑
    pass

def test_planner_decompose():
    # TODO: 测试目标分解
    pass

if __name__ == '__main__':
    test_task_creation()
    print('请完成其他测试')
