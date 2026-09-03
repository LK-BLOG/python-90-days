# Day 7 挑战三：用户界面 (★★★☆☆)
# 要求: 实现命令行交互界面。


def print_header(title):
    """打印美观的标题。"""
    width = 40
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")


def print_menu(options):
    """打印编号菜单。
    
    Args:
        options: [(编号, 文字), ...] 或 [文字, ...]
    """
    # TODO: 格式化打印菜单选项
    pass


def get_choice(options_count):
    """获取用户选择（带输入验证）。
    
    Returns:
        int: 用户选择的编号（1-based），无效输入返回 None
    """
    # TODO: 读取输入，验证范围
    pass


def get_input(prompt, required=True, default=""):
    """获取用户输入（带验证和默认值）。"""
    # TODO: 显示提示，读取输入，处理空输入和默认值
    pass


class TodoUI:
    """Todo 命令行界面。"""
    
    MENU_OPTIONS = [
        "添加 Todo",
        "查看所有 Todo",
        "搜索 Todo",
        "完成 Todo",
        "删除 Todo",
        "查看统计",
        "退出",
    ]
    
    def __init__(self, manager):
        """初始化界面。
        
        Args:
            manager: TodoManager 实例
        """
        self.manager = manager
        self._running = False
    
    def run(self):
        """主循环。"""
        # TODO: 循环显示菜单，处理用户选择
        # TODO: 捕获 Ctrl+C (KeyboardInterrupt) 优雅退出
        pass
    
    def show_add(self):
        """交互式添加 Todo。"""
        # TODO: 逐步获取 title, description, priority, tags
        # TODO: 调用 manager.add
        # TODO: 显示成功信息
        pass
    
    def show_list(self):
        """显示所有 Todo。"""
        # TODO: 格式化打印列表
        pass
    
    def show_search(self):
        """交互式搜索。"""
        pass
    
    def show_complete(self):
        """交互式标记完成。"""
        pass
    
    def show_delete(self):
        """交互式删除。"""
        pass
    
    def show_stats(self):
        """显示统计信息。"""
        # TODO: 调用 manager.get_stats() 并美观打印
        pass


# ===== 测试 =====
if __name__ == "__main__":
    from challenge02 import TodoManager
    mgr = TodoManager("_test_ui.json")
    mgr.add("测试任务1", priority="高")
    mgr.add("测试任务2", priority="低")
    
    ui = TodoUI(mgr)
    # ui.run()  # 取消注释运行交互式界面
    
    # 非交互式测试
    print_header("Todo 管理器测试")
    print_menu(TodoUI.MENU_OPTIONS)
    
    import os
    if os.path.exists("_test_ui.json"):
        os.remove("_test_ui.json")
