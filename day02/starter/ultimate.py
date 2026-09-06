# Day 2 终极挑战：完整游戏背包
# 难度：★★★★★
# 目标：做一个可交互的背包管理程序。


def add_item(items, name, kind, price, count=1):
    """添加物品；同名物品可以选择叠加数量。"""
    # TODO：实现添加逻辑
    pass


def remove_item(items, name, count=1):
    """减少物品数量；数量归零时删除整条记录。"""
    # TODO：处理物品不存在、数量不足、数量归零
    pass


def search_items(items, keyword='', kind=None, minimum_price=None):
    """按名称关键词、类型和最低价格筛选物品。"""
    # TODO：组合多个条件，返回新的列表
    pass


def backpack_report(items):
    """返回背包报告：种类数、总数量、总价值和物品列表。"""
    # TODO：调用前面写过的函数或自己拆分辅助函数
    pass


def run_demo():
    """运行一组演示数据；真正交互功能可作为加餐。"""
    bag = []
    # TODO：添加至少三种物品
    # TODO：删除一种物品的一部分数量
    # TODO：搜索并打印结果
    # TODO：打印最终报告
    print('请完成完整背包系统')


if __name__ == '__main__':
    run_demo()
