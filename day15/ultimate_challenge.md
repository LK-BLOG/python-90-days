# Day 15 Boss 挑战 — ORM 模型基类

## 项目名称
MiniORM — 轻量级 ORM 模型

## 目标
设计一个 ORM 风格的模型基类，支持字段定义、类型验证、JSON 序列化、查询方法。

## 功能要求

### 字段系统
1. Field 基类（name, type, required, default）
2. StringField, IntegerField, FloatField, BooleanField
3. 字段描述符自动验证
4. 默认值和必填字段

### Model 基类
5. 类属性声明字段
6. 实例初始化自动绑定
7. to_dict() 序列化
8. from_dict(cls, data) 反序列化
9. validate() 验证所有字段

### 数据库模拟
10. save() 存入 JSON 文件
11. load(cls, id) 从 JSON 加载
12. all(cls) 获取所有实例
13. filter(cls, **kwargs) 查询

### 查询
14. 链式查询: User.filter(age__gt=18).filter(name__contains='a')
15. 排序: .order_by('name')

## 验收标准
- User(name='Alice', age=25) 正常创建
- User(name='') 抛 ValueError（required）
- user.to_dict() 返回字典
- user.save() 写入 JSON 文件
- User.all() 返回所有用户
- User.filter(age__gt=18) 返回过滤结果
