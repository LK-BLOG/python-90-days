# Day 2 挑战四：背包统计
# 难度：★★★★☆
# 目标：把一个大问题拆成多个小函数。


def total_count(items):
    """统计所有物品的数量。"""
    # TODO：遍历 items，把每个 item['count'] 加到 total
    total = 0
    for item in items:
        total += item['count']
    return total


def total_value(items):
    """计算背包总价值：price * count。"""
    # TODO：遍历 items，累计每件物品的价格乘数量
    bag_money_total=0
    for item in items:
        bag_money_total += item['count'] * item['price']
    return bag_money_total

def inventory_summary(items):
    """返回统计结果字典。

    返回格式：
        {'种类数': 2, '总数量': 3, '总价值': 110}
    """
    # TODO：调用上面两个函数，不要重复写统计逻辑
    total_key_word={}
    total_key_word['种类数']=len(items)
    total_key_word['总数量']=total_count(items)
    total_key_word['总价值']=total_value(items)
    return total_key_word


if __name__ == '__main__':
    bag = [
        {'name': '药水', 'price': 30, 'count': 2},
        {'name': '木剑', 'price': 50, 'count': 1},
    ]
    print(inventory_summary(bag))
