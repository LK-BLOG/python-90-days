"""Day 25 测试：Debug + 测试基础"""
import pytest
import time
import logging


# 导入练习模块
# from exercises import Stack, Queue, SimpleLogger, timer_decorator


class TestStack:
    """栈测试"""
    
    def test_push(self):
        """测试压栈"""
        # stack = Stack()
        # stack.push(1)
        # assert stack.size() == 1
        # assert stack.peek() == 1
        pass
    
    def test_pop(self):
        """测试弹栈"""
        # stack = Stack()
        # stack.push(1)
        # stack.push(2)
        # assert stack.pop() == 2
        # assert stack.pop() == 1
        pass
    
    def test_peek(self):
        """测试查看栈顶"""
        # stack = Stack()
        # stack.push(1)
        # stack.push(2)
        # assert stack.peek() == 2
        # assert stack.size() == 2  # peek 不改变栈
        pass
    
    def test_empty_stack(self):
        """测试空栈操作"""
        # stack = Stack()
        # assert stack.is_empty()
        # assert stack.size() == 0
        pass
    
    def test_pop_empty_raises(self):
        """测试空栈弹栈抛出异常"""
        # stack = Stack()
        # with pytest.raises(IndexError):
        #     stack.pop()
        pass
    
    def test_peek_empty_raises(self):
        """测试空栈查看抛出异常"""
        # stack = Stack()
        # with pytest.raises(IndexError):
        #     stack.peek()
        pass


class TestQueue:
    """队列测试"""
    
    def test_enqueue(self):
        """测试入队"""
        # queue = Queue()
        # queue.enqueue("a")
        # queue.enqueue("b")
        # assert queue.size() == 2
        pass
    
    def test_dequeue(self):
        """测试出队"""
        # queue = Queue()
        # queue.enqueue("a")
        # queue.enqueue("b")
        # assert queue.dequeue() == "a"  # FIFO
        # assert queue.dequeue() == "b"
        pass
    
    def test_peek(self):
        """测试查看队首"""
        # queue = Queue()
        # queue.enqueue(1)
        # queue.enqueue(2)
        # assert queue.peek() == 1
        pass
    
    def test_empty_queue(self):
        """测试空队列"""
        # queue = Queue()
        # assert queue.is_empty()
        pass
    
    def test_dequeue_empty_raises(self):
        """测试空队列出队抛出异常"""
        # queue = Queue()
        # with pytest.raises(IndexError):
        #     queue.dequeue()
        pass


class TestSimpleLogger:
    """日志系统测试"""
    
    def test_log_levels(self):
        """测试日志级别"""
        # logger = SimpleLogger("test", level=SimpleLogger.DEBUG)
        # logger.debug("debug message")
        # logger.info("info message")
        # logger.warning("warning message")
        # logger.error("error message")
        # assert len(logger.entries) == 4
        pass
    
    def test_log_format(self):
        """测试日志格式"""
        # logger = SimpleLogger("test")
        # logger.info("test message")
        # entry = logger.entries[0]
        # assert "test" in entry
        # assert "INFO" in entry
        # assert "test message" in entry
        pass
    
    def test_log_level_filter(self):
        """测试日志级别过滤"""
        # logger = SimpleLogger("test", level=SimpleLogger.WARNING)
        # logger.debug("debug")  # 不应记录
        # logger.info("info")    # 不应记录
        # logger.warning("warning")
        # logger.error("error")
        # assert len(logger.entries) == 2
        pass


class TestTimerDecorator:
    """计时装饰器测试"""
    
    def test_timer_measures_time(self):
        """测试计时功能"""
        # @timer_decorator
        # def slow_function():
        #     time.sleep(0.1)
        #     return "done"
        # 
        # result = slow_function()
        # assert result == "done"
        pass
    
    def test_timer_preserves_function_name(self):
        """测试保留函数名"""
        # @timer_decorator
        # def my_function():
        #     pass
        # 
        # assert my_function.__name__ == "my_function"
        pass


class TestBinarySearchBug:
    """二分查找测试"""
    
    def test_find_first_problem(self):
        """测试找到第一个问题"""
        # data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # # 假设从 index 6 开始有问题
        # index = binary_search_bug(data, lambda x: x > 5)
        # assert index == 6
        pass
    
    def test_no_problem(self):
        """测试没有问题"""
        # data = [1, 2, 3, 4, 5]
        # index = binary_search_bug(data, lambda x: x > 10)
        # assert index == -1  # 或 None
        pass
    
    def test_all_problems(self):
        """测试全部有问题"""
        # data = [1, 2, 3, 4, 5]
        # index = binary_search_bug(data, lambda x: True)
        # assert index == 0
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
