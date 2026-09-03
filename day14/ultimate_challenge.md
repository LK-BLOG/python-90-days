# Day 14 Boss 挑战 — 图形系统

## 项目名称
ShapeGraphics — 图形继承系统

## 目标
设计完整的图形继承链，用 ABC、Mixin、多继承构建可扩展的图形系统。

## 功能要求

### 基础继承
1. Shape ABC: area(), perimeter(), describe()
2. Circle: 支持半径
3. Rectangle: 支持宽高
4. Triangle: 支持三边（海伦公式）

### Mixin 功能
5. Drawable Mixin: draw() 返回 ASCII 图形
6. Serializable Mixin: to_dict(), from_dict()
7. Comparable Mixin: 按面积比较

### 高级图形
8. Polygon(Shape): 任意多边形（边长列表）
9. Composite: 图形组合（支持 add, total_area）
10. ScaledShape: 装饰器，缩放图形

### 工厂
11. ShapeFactory: 从字符串创建图形
12. Shape.from_dict(data): 反序列化

## 验收标准
- Circle(5).area() ≈ 78.54
- Rectangle(3, 4).perimeter() == 14
- Triangle(3, 4, 5).area() == 6.0
- 所有图形支持 to_dict()/from_dict()
- Composite 可以嵌套
- ShapeFactory('circle', radius=5) 创建 Circle
