"""
Day 15 - OOP深入③ 封装与property
===============================
练习：实现一个 Model 基类，演示属性封装和 property

要求：
- 字段验证（类型 + 范围）
- property 做受保护属性的读写控制
- to_dict / from_dict 序列化
- validate 抽象方法由子类实现

运行本文件测试你的实现是否正确。
"""


class Model:
    """模型基类 -- 演示封装与 property

    子类通过 _fields 定义字段:
        class User(Model):
            _fields = {
                'name':  {'type': str, 'required': True},
                'age':   {'type': int, 'min': 0, 'max': 150},
                'email': {'type': str},
            }

    TODO: 实现以下功能:
        1. __init__ 接受关键字参数，调用 validate 后存入 _data
        2. validate() 根据 _fields 规则校验所有字段
        3. to_dict() 返回字段字典
        4. from_dict(cls, data) 类方法，从字典创建实例
        5. 为每个字段实现 property（可选加分项）
    """

    _fields = {}   # 子类覆盖

    def __init__(self, **kwargs):
        self._data = {}
        # TODO: 根据 _fields 初始化字段
        #       - required 字段必须提供
        #       - 未提供的用默认值或 None
        #       - 调用 self.validate()

    def validate(self):
        """根据 _fields 定义验证所有字段

        TODO: 实现验证逻辑
            - 检查类型 (type)
            - 检查范围 (min/max)
            - 检查必填 (required)
            - 验证失败抛出 ValueError
        """
        pass

    def to_dict(self) -> dict:
        """序列化为字典"""
        # TODO: 返回 self._data 的副本
        pass

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        # TODO: 调用 cls(**data)
        pass

    def __repr__(self):
        fields = ', '.join(f'{k}={v!r}' for k, v in self._data.items())
        return f'{self.__class__.__name__}({fields})'


class User(Model):
    """用户模型（示例子类）

    字段定义:
        - name:  字符串，必填
        - age:   整数，范围 0-150
        - email: 字符串，可选
    """

    _fields = {
        'name':  {'type': str, 'required': True},
        'age':   {'type': int, 'min': 0, 'max': 150},
        'email': {'type': str},
    }


# ==================== 测试 ====================
if __name__ == '__main__':
    print('=' * 50)
    print('Day 15 练习: Model 封装与property')
    print('=' * 50)

    user = User(name='Alice', age=25, email='alice@example.com')
    print(user)
    print(user.to_dict())

    user2 = User.from_dict({'name': 'Bob', 'age': 30})
    print(user2)

    # 类型错误
    try:
        bad = User(name='X', age='not_a_number')
        print('ERROR: 应该抛出 ValueError')
    except ValueError as e:
        print(f'验证捕获: {e}')

    # 范围错误
    try:
        bad = User(name='Y', age=-5)
        print('ERROR: 应该抛出 ValueError')
    except ValueError as e:
        print(f'验证捕获: {e}')

    print('OK -- 所有测试通过!')
