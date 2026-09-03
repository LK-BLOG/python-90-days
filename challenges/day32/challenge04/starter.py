# Challenge 04: TDD 实战
# 遵循 TDD 流程：先写测试，再写代码

# Step 1: 先写这个测试
# def test_queue():
#     q = Queue()
#     q.enqueue(1)
#     q.enqueue(2)
#     assert q.dequeue() == 1
#     assert q.dequeue() == 2
#     assert q.is_empty()

# Step 2: 写最少代码让测试通过
class Queue:
    def __init__(self):
        pass
    def enqueue(self, item):
        pass
    def dequeue(self):
        pass
    def is_empty(self):
        pass
    def size(self):
        pass
    def peek(self):
        pass

# Step 3: 重构
