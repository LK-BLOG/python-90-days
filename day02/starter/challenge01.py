# Day 2 挑战一：显示背包物品
# 难度：★☆☆☆☆
# 目标：遍历列表，把每个物品打印出来。


def show_items(items):
    """逐个打印背包里的物品。

    输入：['药水', '木剑', '盾牌']
    输出：
        1. 药水
        2. 木剑
        3. 盾牌
    """
    # TODO：用 range(len(items)) 遍历列表
    # TODO：用下标取出每个物品
    # TODO：打印编号和物品名称

    for i in range(len(items)):
        print(str(i+1)+"."+items[i])


if __name__ == '__main__':
    bag = ['药水', '木剑', '盾牌']
    show_items(bag)
