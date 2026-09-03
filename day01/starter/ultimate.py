# Day 1 Boss 挑战：多格式报告生成器 (综合版)
# 难度: ★★★★★
# 要求: 综合运用函数参数设计（*args、**kwargs、默认值、类型注解、
#       关键字-only参数），构建一个完整的报告生成系统。


class ReportGenerator:
    """多格式报告生成器 —— 综合 Day 1 所有知识点。
    
    功能说明:
        - 支持 text/markdown/csv/html 四种输出格式
        - 支持数据排序、过滤、聚合
        - 支持自定义列映射和格式化
        - 使用 *args/**kwargs 展示参数设计能力
        - 使用闭包实现格式化器工厂
    
    用法:
        >>> gen = ReportGenerator("月度报告", data)
        >>> print(gen.render(format="markdown", sort_by="revenue"))
    """
    
    def __init__(self, title, data, **options):
        """初始化报告生成器。
        
        Args:
            title: 报告标题
            data: 数据列表（字典列表）
            **options: 可选配置:
                - precision (int): 数值精度，默认 2
                - date_format (str): 日期格式，默认 "%Y-%m-%d"
                - encoding (str): 输出编码，默认 "utf-8"
        """
        # TODO: 存储标题、数据和选项
        # TODO: 从 data 中自动提取列名
        pass
    
    def add_column(self, name, *, formatter=None, alias=None, **kwargs):
        """添加一个自定义列。
        
        Args:
            name: 列名（对应数据字典中的键）
            formatter: 自定义格式化函数（可选）
            alias: 列的显示别名（可选）
            **kwargs: 额外列配置
        """
        # TODO: 存储列的配置信息
        pass
    
    def filter_data(self, **conditions):
        """按条件过滤数据。
        
        Args:
            **conditions: 过滤条件，键为列名，值为期望值或 callable
        
        Returns:
            ReportGenerator: 返回自身，支持链式调用
        """
        # TODO: 遍历条件，过滤 self._data
        # TODO: 返回 self 支持链式调用
        pass
    
    def render(self, format="text", **kwargs):
        """渲染报告。
        
        Args:
            format: 输出格式 ("text"/"markdown"/"csv"/"html")
            **kwargs: 额外渲染选项
        
        Returns:
            str: 渲染后的报告字符串
        """
        # TODO: 根据 format 分派到不同的渲染方法
        pass
    
    def _get_formatter(self, format):
        """工厂方法：根据格式名返回对应的格式化函数（闭包）。
        
        Args:
            format: 格式名
        
        Returns:
            callable: 格式化函数
        """
        # TODO: 使用闭包返回对应格式的格式化函数
        pass


def make_formatter(format_name, **options):
    """格式化工厂函数 —— 闭包应用。
    
    功能说明:
        返回一个格式化函数，该函数接收数据并返回格式化字符串。
    
    Args:
        format_name: 格式名 ("text"/"markdown"/"csv")
        **options: 格式化选项
    
    Returns:
        callable: 格式化函数
    """
    # TODO: 使用闭包捕获 format_name 和 options
    # TODO: 返回内层格式化函数
    pass


# ===== 测试 =====
if __name__ == "__main__":
    sales_data = [
        {"product": "手机", "region": "北京", "revenue": 150000, "units": 300},
        {"product": "手机", "region": "上海", "revenue": 120000, "units": 250},
        {"product": "平板", "region": "北京", "revenue": 80000, "units": 100},
        {"product": "平板", "region": "上海", "revenue": 65000, "units": 80},
        {"product": "耳机", "region": "北京", "revenue": 45000, "units": 500},
    ]
    
    gen = ReportGenerator("Q3 销售报告", sales_data, precision=0)
    
    # 链式调用: 过滤 + 渲染
    print(gen.filter_data(region="北京").render(format="markdown", sort_by="revenue"))
