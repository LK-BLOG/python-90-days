# 三种方法类型

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 实例方法：第一个参数是 self
    def iso_format(self):
        return f'{self.year}-{self.month:02d}-{self.day:02d}'

    # 类方法：第一个参数是 cls，用于工厂方法
    @classmethod
    def from_string(cls, date_str):
        y, m, d = map(int, date_str.split('-'))
        return cls(y, m, d)

    # 静态方法：没有 self/cls
    @staticmethod
    def is_valid(y, m, d):
        return 1 <= m <= 12 and 1 <= d <= 31

d = Date.from_string('2024-03-15')
print(d.iso_format())   # 2024-03-15
print(Date.is_valid(2024, 13, 1))  # False
