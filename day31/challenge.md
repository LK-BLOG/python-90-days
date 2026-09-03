# Day 31 挑战任务

## Challenge 1: Git 仓库初始化
**目标：** 创建一个规范的 Git 仓库

**要求：**
- git init 初始化仓库
- 编写完整的 .gitignore（Python + IDE + OS + 环境变量）
- 创建 README.md
- 用 Conventional Commits 格式提交 3 次
- 创建一个 feature 分支，做 2 次提交，rebase 到 main
- 至少展示 git log --oneline --graph 的结果

**难度：** ⭐

---

## Challenge 2: 创建项目结构（src layout）
**目标：** 搭建一个标准的 Python 项目骨架

**要求：**
- 使用 src layout 创建 `my_tool` 包
- 创建 `__init__.py` + `__main__.py`（能 `python -m my_tool` 运行）
- 创建 `cli.py`、`utils.py`、`config.py` 空模块
- 创建 `tests/` 目录和 `test_cli.py`（空测试文件）
- 创建 `examples/` 目录
- 创建 `pyproject.toml`

**难度：** ⭐⭐

---

## Challenge 3: 配置 pyproject.toml + 依赖管理
**目标：** 完善项目配置

**要求：**
- 在 Challenge 2 的基础上完善 pyproject.toml
- 添加至少 3 个运行时依赖
- 添加 dev 依赖组（pytest、black、ruff）
- 配置 [project.scripts] 入口点
- 配置 [tool.pytest.ini_options]
- 用 venv 安装项目（pip install -e ".[dev]"）
- 用 pip freeze 导出 requirements.txt

**难度：** ⭐⭐

---

## Challenge 4: 整理旧项目
**目标：** 把之前的某个小项目重构为专业结构

**要求：**
- 选择 Day 01-30 中任意一个你写过的项目
- 重构为 src layout
- 添加 pyproject.toml
- 添加 .gitignore
- 使用 Conventional Commits 提交
- 虚拟环境隔离
- 项目能通过 `pip install -e .` 安装

**难度：** ⭐⭐⭐

---

## Challenge 5 (Boss): 创建一个完整的 Python 包
**目标：** 从零创建一个可发布的 Python 包

**要求：**
- 创建一个工具包（如字符串工具集、日期工具集等）
- 完整的 src layout + pyproject.toml
- 至少 3 个模块，每个模块至少 3 个函数
- 完整的类型注解
- README.md（含安装说明和使用示例）
- LICENSE 文件
- 虚拟环境 + 依赖隔离
- 用 poetry 或 uv 管理
- 能 `pip install -e .` 后在 Python 中直接 import 使用
- Git 仓库 + 5 次以上有意义的 commit

**难度：** ⭐⭐⭐⭐
