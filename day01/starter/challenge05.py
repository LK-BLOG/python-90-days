# Day 1 挑战五：逐行打印报告
# 难度：★★★☆☆
#
# 只使用：普通参数、列表、for、print。
# 先不要用 *args、**kwargs、join、字典、类。


def print_report(title, names, scores):
    """打印一份最简单的成绩报告。

    参数：
        title: 报告标题，例如 "数学成绩"
        names: 姓名列表，例如 ["小明", "小红"]
        scores: 分数列表，例如 [90, 85]

    输出示例：
        数学成绩
        小明：90分
        小红：85分
    """
    # TODO：打印 title
    # TODO：用一个 for 循环按下标同时取出 names 和 scores
    # 提示：range(len(names))
    # TODO：打印“姓名：分数分”
    print("title: ", title,"\nnames: ", names,"\nscores: ", scores)


if __name__ == "__main__":
    print_report("数学成绩", ["小明", "小红"], [90, 85])
