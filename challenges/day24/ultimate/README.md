# Day 24 终极挑战：专业工程结构重构

## 项目名称：PyProject Pro

## 背景
你之前的项目（比如计算器、TODO 应用、爬虫等）都是单文件脚本。
现在要把其中一个重构为**可发布、可维护、可协作**的专业 Python 工程。

## 目标
将一个现有项目改造为符合 Python 工业标准的工程结构。

## 功能要求

### 1. 项目结构（src layout）
```
pyproject-pro/
├── src/
│   └── pyproject_pro/
│       ├── __init__.py       # 版本号、包信息
│       ├── __main__.py       # python -m 入口
│       ├── cli.py            # 命令行接口
│       ├── core.py           # 核心逻辑
│       └── utils.py          # 工具函数
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # unittest fixtures
│   ├── test_core.py
│   ├── test_cli.py
│   └── test_utils.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── test.txt
├── pyproject.toml
├── Makefile
├── .gitignore
├── .flake8
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### 2. pyproject.toml 配置
- 完整的 project 元数据
- build-system 配置
- black/isort/flake8/unittest/mypy 工具配置
- 可选依赖组（dev、test）

### 3. Makefile
- help（自动列出目标）
- install、dev、test、lint、format、clean、build、typecheck
- 至少 8 个目标

### 4. CI 配置
- .github/workflows/ci.yml
- 多 Python 版本测试（3.9、3.10、3.11）
- lint + test + build 三阶段

### 5. 代码质量
- 所有代码通过 black 格式化
- import 排序通过 isort
- 无 flake8 警告

### 6. 文档
- README.md：安装、使用、开发指南
- CHANGELOG.md：版本变更记录
- 代码中关键函数有 docstring

## 输入
你选择的之前项目的源代码

## 输出
完整可运行的专业 Python 工程

## 限制
- 必须使用 src layout
- 必须使用 pyproject.toml（不能用 setup.py）
- 代码必须通过 black 检查
- Makefile 中的命令必须全部可执行

## 验收标准
- [ ] `python -m build` 能成功构建 wheel 和 sdist
- [ ] `make test` 通过所有测试
- [ ] `make lint` 无错误
- [ ] `make help` 显示所有可用命令
- [ ] `pip install -e ".[dev]"` 安装成功
- [ ] CI 配置语法正确
- [ ] README.md 包含安装和使用说明

## 可选扩展
- 添加 package|publish|buildfile 和 package|publish|build-compose.yml
- 集成 pre-commit hooks
- 添加 Sphinx 文档生成
- 配置 dependabot
- 添加代码覆盖率 badge

