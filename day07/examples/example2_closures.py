# 示例2：闭包与数据结构操作
# 展示闭包、列表推导式、字典操作

def create_todo_counter():
    """创建Todo计数器闭包"""
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    def get_count():
        return count
    
    def reset():
        nonlocal count
        count = 0
    
    return increment, get_count, reset

def create_operation_logger():
    """创建操作日志闭包"""
    operations = []
    
    def log_operation(operation_type, todo_title):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        operations.append({
            "time": timestamp,
            "type": operation_type,
            "todo": todo_title
        })
        return f"[{timestamp}] {operation_type}: {todo_title}"
    
    def get_operations():
        return operations.copy()
    
    def clear_operations():
        operations.clear()
    
    def search_operations(keyword):
        """搜索操作记录"""
        keyword = keyword.lower()
        return [op for op in operations if keyword in op["todo"].lower()]
    
    return log_operation, get_operations, clear_operations, search_operations

class TodoAnalyzer:
    """Todo分析器，展示数据结构操作"""
    
    def __init__(self):
        self.todos = []
    
    def add_todo(self, todo):
        """添加Todo"""
        self.todos.append(todo)
    
    def get_completed_count(self):
        """获取已完成Todo数量"""
        return len([t for t in self.todos if t["completed"]])
    
    def get_by_priority(self, priority):
        """按优先级筛选"""
        return [t for t in self.todos if t["priority"] == priority]
    
    def search_todos(self, keyword):
        """搜索Todo"""
        keyword = keyword.lower()
        return [t for t in self.todos 
                if keyword in t["title"].lower() or 
                keyword in t["description"].lower()]
    
    def get_statistics(self):
        """获取统计信息"""
        total = len(self.todos)
        completed = self.get_completed_count()
        pending = total - completed
        
        # 按优先级统计
        priority_stats = {}
        for priority in ["高", "中", "低"]:
            count = len(self.get_by_priority(priority))
            priority_stats[priority] = count
        
        # 按标签统计
        tag_stats = {}
        for todo in self.todos:
            for tag in todo.get("tags", []):
                tag_stats[tag] = tag_stats.get(tag, 0) + 1
        
        return {
            "总数": total,
            "已完成": completed,
            "待完成": pending,
            "完成率": f"{(completed/total*100):.1f}%" if total > 0 else "0%",
            "优先级分布": priority_stats,
            "标签使用频率": tag_stats
        }
    
    def get_completion_time_stats(self):
        """获取完成时间统计"""
        from datetime import datetime
        
        completed_todos = [t for t in self.todos if t["completed"] and t.get("completed_at")]
        if not completed_todos:
            return None
        
        times = []
        for todo in completed_todos:
            created = datetime.fromisoformat(todo["created_at"])
            completed = datetime.fromisoformat(todo["completed_at"])
            delta = completed - created
            times.append(delta.total_seconds() / 86400)  # 转换为天
        
        return {
            "平均完成时间": f"{sum(times)/len(times):.1f}天",
            "最短完成时间": f"{min(times):.1f}天",
            "最长完成时间": f"{max(times):.1f}天"
        }

# 测试代码
if __name__ == "__main__":
    # 测试闭包
    print("=== 测试闭包 ===")
    increment, get_count, reset = create_todo_counter()
    print(f"计数: {get_count()}")
    increment()
    increment()
    print(f"计数: {get_count()}")
    reset()
    print(f"重置后: {get_count()}")
    
    # 测试日志闭包
    print("\n=== 测试日志闭包 ===")
    log, get_ops, clear_ops, search_ops = create_operation_logger()
    log("添加", "学习Python")
    log("完成", "买菜")
    log("添加", "写代码")
    print("所有操作:", get_ops())
    print("搜索'学习':", search_ops("学习"))
    
    # 测试分析器
    print("\n=== 测试分析器 ===")
    analyzer = TodoAnalyzer()
    analyzer.add_todo({"title": "任务1", "priority": "高", "completed": True, "tags": ["学习"]})
    analyzer.add_todo({"title": "任务2", "priority": "中", "completed": False, "tags": ["工作"]})
    analyzer.add_todo({"title": "任务3", "priority": "低", "completed": True, "tags": ["学习"]})
    
    stats = analyzer.get_statistics()
    print("统计信息:", stats)
    print("高优先级任务:", [t["title"] for t in analyzer.get_by_priority("高")])
    print("搜索'任务':", [t["title"] for t in analyzer.search_todos("任务")])
