# Day 1 挑战三：默认设置函数
# 难度：★★★☆☆
#
# 目标：用户只改需要改的设置，其它设置使用默认值。


def create_report_settings(title="未命名报告", format="text", show_total=False, separator=","):
    """创建报告设置字典。

    示例：
        create_report_settings(title="成绩单", format="csv")

    返回：
        {
            "title": "成绩单",
            "format": "csv",
            "show_total": False,
            "separator": ","
        }
    """
    # TODO：把四个参数放进一个字典，然后 return 这个字典。
    pass


if __name__ == "__main__":
    print(create_report_settings())
    print(create_report_settings(title="成绩单", format="csv"))
