# Day 24 挑战：工程化实践

## 挑战 1：依赖管理器
**难度：** ⭐⭐

编写一个依赖管理工具，解析 requirements.txt 并提供以下功能：
- 列出所有依赖及其版本
- 检查哪些包已安装、哪些未安装
- 检查哪些包有更新可用
- 生成当前环境的 requirements.txt

## 挑战 2：项目脚手架生成器
**难度：** ⭐⭐⭐

编写一个命令行工具，输入项目名称，自动生成标准项目结构：
```
my_project/
├── src/my_project/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── pyproject.toml
├── Makefile
├── .gitignore
├── README.md
└── requirements/
    ├── base.txt
    ├── dev.txt
    └── test.txt
```

## 挑战 3：Makefile 构建系统
**难度：** ⭐⭐

为一个已有的 Python 项目编写完整的 Makefile，支持：
- install、dev、test、lint、format、clean、build、docker-build、docker-run 等目标
- help 目标自动列出所有可用命令

## 挑战 4：配置文件解析器
**难度：** ⭐⭐⭐

编写一个配置管理器，支持：
- 从 pyproject.toml 读取项目配置
- 从 .env 文件读取环境变量
- 配置优先级：环境变量 > .env > pyproject.toml > 默认值
- 配置验证（类型检查、必填字段）

## 挑战 5：代码质量检查器
**难度：** ⭐⭐⭐

编写一个工具，扫描 Python 项目并报告：
- 代码行数统计
- 文件大小检查
- 未使用的 import
- 缺少 docstring 的函数
- 生成 Markdown 格式报告

## 🏆 Boss 挑战：专业工程结构重构
**难度：** ⭐⭐⭐⭐

把之前 Day 1-23 写过的某个项目重构为专业级 Python 工程：
- 标准 src layout
- pyproject.toml 完整配置
- Makefile 自动化
- CI 配置（GitHub Actions）
- 完整文档（README.md）
- 版本管理（CHANGELOG.md）
- 代码质量工具集成
