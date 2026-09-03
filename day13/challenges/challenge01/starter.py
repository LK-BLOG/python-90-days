"""Challenge 1: 学生计数器 - 起手代码"""
# TODO: 完成 Student 类

class Student:
    # TODO: 添加类属性 total_count

    def __init__(self, name, age, scores):
        # TODO: 初始化实例属性
        pass

    # TODO: 实现 __del__ 方法

    def average_score(self):
        # TODO: 返回平均分
        pass

# 测试
if __name__ == '__main__':
    print(Student.total_count)  # 应该是 0
    s1 = Student('Alice', 20, [90, 85, 92])
    s2 = Student('Bob', 21, [78, 82, 85])
    print(Student.total_count)  # 应该是 2
    print(s1.average_score())   # 应该是 89.0
    del s1
    print(Student.total_count)  # 应该是 1
