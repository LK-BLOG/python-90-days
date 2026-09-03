# 类属性 vs 实例属性

class Dog:
    species = '犬科'  # 类属性：所有实例共享

    def __init__(self, name, age):
        self.name = name    # 实例属性：每个实例独立
        self.age = age

buddy = Dog('Buddy', 3)
print(buddy.species)  # '犬科' -- 读取：先查实例，再查类
print(buddy.name)     # 'Buddy'

# 赋值不会改类属性！
buddy.species = '柴犬'
print(buddy.species)  # '柴犬' -- 实例属性
print(Dog.species)    # '犬科' -- 类属性没变

# 可变类属性的陷阱
class Team:
    members = []  # 危险！所有实例共享

    def __init__(self, name):
        self.name = name

t1, t2 = Team('A'), Team('B')
t1.members.append('Alice')
print(t2.members)  # ['Alice'] -- 意外共享！

# 正确做法
class TeamFixed:
    def __init__(self, name):
        self.name = name
        self.members = []  # 每个实例独立
