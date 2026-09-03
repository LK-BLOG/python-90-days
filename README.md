# 🐍 Python 30天高速进阶计划

> 30天、每天约2小时，从Python基础到能独立开发中型项目的实战训练营

## 📋 课程目标

- 掌握Python核心高级特性（闭包、装饰器、生成器、上下文管理器）
- 熟练运用OOP进行软件设计与开发
- 掌握文件IO、JSON、模块系统等工程化技能
- 能独立调用REST API、处理异步编程
- 具备开发AI CLI Agent等中型项目的能力
- 为后续学习FastAPI、AI开发打下坚实基础

## 🎯 适合谁

- 已掌握Python基础语法（变量、循环、条件、列表、字典、函数、类基础）
- 每天能投入约2小时
- 目标是"能写代码"而不是"看懂教程"

## 📅 30天路线图

### 阶段一：Python基础进阶（Day 1-6）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 1](day01/) | 函数参数 | 位置参数、关键字参数、默认参数、`*args`、`**kwargs` |
| [Day 2](day02/) | 函数高级 | 函数作为变量/参数、lambda、`map/filter/sorted` |
| [Day 3](day03/) | 作用域与闭包 | LEGB、`global/nonlocal`、闭包原理与应用 |
| [Day 4](day04/) | 字符串高级 | 切片、格式化、正则基础、文本处理 |
| [Day 5](day05/) | 数据结构进阶 | 推导式、嵌套结构、`enumerate/zip`、数据操作 |
| [Day 6](day06/) | 异常处理 | 完整异常链、自定义异常、防御性编程 |

**🏁 阶段项目 → [Day 7: CLI Todo & 数据管理器](day07/)**

### 阶段二：工程化基础（Day 8-12）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 8](day08/) | 文件 I/O | `open`、读写追加、`with`、编码处理 |
| [Day 9](day09/) | JSON | 序列化/反序列化、自定义编码器、数据持久化 |
| [Day 10](day10/) | pathlib + os | 路径操作、目录遍历、环境变量、文件管理器 |
| [Day 11](day11/) | 模块系统 | `import`机制、模块搜索、`__name__`、项目拆分 |
| [Day 12](day12/) | Package | 包结构、`__init__.py`、模块依赖、工具包开发 |

**🏁 阶段项目 → Day 7 的 CLI Todo 升级为完整包结构**

### 阶段三：面向对象深入（Day 13-18）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 13](day13/) | OOP 深入① | `class/self`、实例/类方法、设计模式基础 |
| [Day 14](day14/) | OOP 深入② | 继承、`super()`、方法重写、MRO |
| [Day 15](day15/) | OOP 深入③ | 封装、property、`classmethod/staticmethod` |
| [Day 16](day16/) | 魔术方法 | `__str__/__eq__/__len__/__getitem__`、运算符重载 |
| [Day 17](day17/) | dataclass | `@dataclass`、类型提示、对象序列化 |
| [Day 18](day18/) | OOP 项目 | 综合运用——RPG/游戏核心框架 |

**🏁 阶段项目 → [Day 18: RPG游戏核心框架](day18/)**

### 阶段四：高级特性（Day 19-23）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 19](day19/) | 迭代器 | iterable/iterator协议、`iter()/next()`、自定义迭代器 |
| [Day 20](day20/) | 生成器 | `yield`、`yield from`、生成器表达式、流式处理 |
| [Day 21](day21/) | 装饰器 | 闭包+装饰器、带参数装饰器、`@timer/@debug/@retry` |
| [Day 22](day22/) | 上下文管理器 | `with`协议、`contextlib`、数据库连接管理 |
| [Day 23](day23/) | 类型系统 | type hints、`Optional/Union`、Protocol、泛型 |

**🏁 阶段项目 → Day 22 的上下文管理器 + Day 21 装饰器 = 日志/重试中间件系统**

### 阶段五：工程实战（Day 24-28）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 24](day24/) | Python 工程化 | `pip`、venv、项目结构、依赖管理 |
| [Day 25](day25/) | Debug + 测试 | `unittest/pytest`、测试用例、覆盖率 |
| [Day 26](day26/) | HTTP | HTTP协议、请求/响应、状态码、Headers |
| [Day 27](day27/) | API 实战 | `requests`、REST API、异常处理、重试机制 |
| [Day 28](day28/) | asyncio | `async/await`、Task、并发、`gather` |

**🏁 阶段项目 → Day 27-28: 多API聚合服务 + 缓存系统**

### 阶段六：AI与毕业（Day 29-30）

| 天数 | 主题 | 核心内容 |
|------|------|----------|
| [Day 29](day29/) | AI + Agent | LLM API、Prompt Engineering、Function Calling、Memory |
| [Day 30](day30/) | 毕业项目 | **独立完成 AI CLI Assistant / Agent** |

## 🏗️ 阶段性项目递进路线

```
Day 7:  CLI Todo（函数+文件+异常）
  ↓ 重构升级
Day 12: 工具包化（模块+包结构）
  ↓ OOP重构  
Day 18: RPG游戏框架（完整OOP）
  ↓ 高级特性加持
Day 22: 中间件系统（装饰器+上下文管理器）
  ↓ 工程化包装
Day 28: API聚合服务（HTTP+asyncio）
  ↓ AI集成
Day 30: AI CLI Agent（毕业大作）
```

## ⚔️ Challenge 规则

每天有 **5个挑战**，难度递增：

- **Challenge 1-2**: 当天知识的基础应用（必做）
- **Challenge 3-4**: 综合应用，接近真实开发（必做）
- **Challenge 5 (Boss)**: 当天最难任务，需要独立设计（挑战）

### 挑战目录结构

```
challenges/
└── dayXX/
    ├── challenge01/
    │   ├── README.md    # 任务说明
    │   └── starter.py   # 起步代码
    ├── challenge02/
    │   ├── README.md
    │   └── starter.py
    ├── ...
    └── ultimate/
        ├── README.md    # Boss挑战说明
        └── starter.py   # 起步代码
```

## 📖 每日学习流程

```
1. 阅读 lesson.md（40分钟）
   - 理解知识点
   - 运行示例代码
   - 完成动手练习

2. 完成 Challenges（60分钟）
   - Challenge 1 → 5 逐步推进
   - 每个Challenge先看README，用starter.py开始
   - 用tests/目录验证

3. 复盘（20分钟）
   - 回顾今天学到什么
   - 标记不懂的地方
   - 预习明天的内容
```

## 🎓 毕业标准

完成以下全部要求即为毕业：

- [ ] 30天的Challenge全部完成（包括Boss Challenge）
- [ ] 6个阶段性项目全部可运行
- [ ] Day 30 毕业项目完成并通过验收
- [ ] 代码有基本的错误处理
- [ ] 代码有基本的测试覆盖
- [ ] 能独立阅读和理解自己写的代码

## ⚠️ 注意事项

1. **不要跳天**：知识是递进的，跳了后面会翻车
2. **不要只看不写**：每天至少写2小时代码
3. **不要抄答案**：starter.py只有骨架，答案需要自己填
4. **卡住了先查文档**：培养独立解决问题的能力
5. **每个测试都要跑**：tests/不是摆设

---

**开始你的第一天 → [Day 1: 函数参数](day01/)**
