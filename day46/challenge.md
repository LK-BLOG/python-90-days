# Day 46 挑战任务

## Challenge 1: 单一职责 & 开闭原则
**目标：** 识别并修复SRP和OCP违反

**场景：** 以下类负责处理订单的所有逻辑：
`python
class OrderProcessor:
    def validate_order(self, order: dict) -> bool: ...
    def calculate_total(self, order: dict) -> float: ...
    def process_payment(self, order: dict, payment_method: str) -> bool: ...
    def send_confirmation_email(self, order: dict) -> None: ...
    def update_inventory(self, order: dict) -> None: ...
    def generate_invoice(self, order: dict) -> str: ...
`

**要求：**
1. 将OrderProcessor拆分为符合SRP的多个类
2. 为支付方式实现策略模式（OCP）
3. 使用依赖注入组合这些类

**验收：** 每个类只负责一件事，新增支付方式不需要修改已有代码
**难度：** ⭐⭐

---

## Challenge 2: 里氏替换 & 接口隔离
**目标：** 正确使用继承和Protocol

**要求：**
1. 定义一个可绘制的形状层次结构（Rectangle, Circle, Triangle）
2. 使用Protocol而非ABC定义接口
3. 实现一个render_all(shapes: list[Drawable])函数
4. 确保所有形状都能无缝替换
5. 写测试验证LSP

**验收：** 所有形状都能通过render_all测试，无运行时类型错误
**难度：** ⭐⭐

---

## Challenge 3: 依赖倒置
**目标：** 实现一个遵循DIP的数据处理管道

**要求：**
1. 定义DataSource和DataSink抽象
2. 实现具体的CSVDataSource、JsonDataSource
3. 实现具体的DatabaseSink、FileSink
4. 通过构造函数注入依赖
5. 写测试验证可以替换不同实现

**验收：** 可以自由组合不同的Source和Sink，不需要修改管道代码
**难度：** ⭐⭐⭐

---

## Challenge 4: 反模式识别
**目标：** 识别代码中的反模式并重构

**代码：** 见starter目录下的bad_code.py
**要求：**
1. 找出所有违反SOLID的地方（至少5处）
2. 每处标注违反了哪个原则
3. 逐一重构
4. 重构后所有测试通过

**验收：** bad_code_refactored.py通过所有测试
**难度：** ⭐⭐⭐
