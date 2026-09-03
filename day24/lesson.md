# Day 24 课程：Python 工程化

## 模块一：pip 包管理

### 1.1 什么是 pip

pip 是 Python 的官方包管理器，用于安装、升级和卸载第三方库。

### 1.2 常用命令

```bash
# 安装包
pip install requests
pip install requests==2.28.1          # 指定版本
pip install "requests>=2.28,<3.0"    # 版本范围
pip install requests --upgrade       # 升级
pip install requests --user          # 安装到用户目录

# 查看已安装包
pip list
pip list --outdated                  # 查看过期包

# 查看包信息
pip show requests

# 卸载
pip uninstall requests
pip uninstall requests -y            # 不确认卸载

# 导出/导入依赖
pip freeze > requirements.txt
pip install -r requirements.txt

# 搜索（已弃用，用 PyPI 网站）
pip search requests
```

### 1.3 requirements.txt 最佳实践

```txt
# requirements.txt
# 固定版本 — 生产环境推荐
requests==2.28.1
flask==2.3.2

# 版本范围 — 开发环境可用
numpy>=1.24,<2.0

# 从 Git 安装
git+https://github.com/user/repo.git@main

# 从文件安装
-r base.txt
```

**常见错误：** 忘记 `pip freeze` 导致部署时缺包。解决方案：维护 `requirements.txt` 并在 CI 中自动检查。

### 1.4 分层依赖管理

```
requirements/
├── base.txt          # 核心依赖
├── dev.txt           # 开发工具（-r base.txt）
├── test.txt          # 测试依赖（-r base.txt）
└── prod.txt          # 生产环境（-r base.txt）
```

```txt
# base.txt
requests==2.28.1
flask==2.3.2

# dev.txt
-r base.txt
black==23.7.0
flake8==6.1.0
isort==5.12.0

# test.txt
-r base.txt
pytest==7.4.0
pytest-cov==4.1.0
```

---

## 模块二：虚拟环境

### 2.1 为什么需要虚拟环境

不同项目可能依赖不同版本的包。虚拟环境为每个项目创建独立的 Python 环境。

### 2.2 venv 使用

```bash
# 创建虚拟环境
python -m venv .venv

# 激活（Windows）
.venv\Scripts\activate

# 激活（macOS/Linux）
source .venv/bin/activate

# 退出虚拟环境
deactivate

# 删除虚拟环境 — 直接删目录
rm -rf .venv
```

### 2.3 实际项目工作流

```bash
# 1. 创建项目
mkdir myproject && cd myproject

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux/Mac

# 4. 安装依赖
pip install -r requirements.txt

# 5. 开发...
# 6. 导出新依赖
pip freeze > requirements.txt
```

**常见错误：** 在虚拟环境外安装包。**解决方案：** 始终确认终端提示符前有 `(.venv)` 标记。

---

## 模块三：pyproject.toml 与项目打包

### 3.1 pyproject.toml 基础

`pyproject.toml` 是 Python 项目的标准化配置文件（PEP 517/518）。

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-awesome-lib"
version = "1.0.0"
description = "一个示例 Python 库"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "你的名字", email = "you@example.com"}
]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "black>=23.0",
    "flake8>=6.0",
    "pytest>=7.0",
]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.urls]
Homepage = "https://github.com/yourname/my-awesome-lib"
Documentation = "https://my-awesome-lib.readthedocs.io"

[project.scripts]
my-cli = "my_awesome_lib.cli:main"

# 工具配置
[tool.black]
line-length = 88
target-version = ["py39"]

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=my_awesome_lib"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
```

### 3.2 项目目录结构

**src layout（推荐）：**
```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
├── LICENSE
├── Makefile
└── .gitignore
```

**flat layout：**
```
my-project/
├── my_project/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── tests/
├── pyproject.toml
├── README.md
└── .gitignore
```

**区别：** src layout 防止本地代码意外覆盖已安装的包，CI/CD 中更可靠。大型项目推荐 src layout。

### 3.3 setup.py（遗留方式）

```python
# 现代项目优先用 pyproject.toml
# setup.py 仅在需要动态配置时使用
from setuptools import setup, find_packages

setup(
    name="my-awesome-lib",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests>=2.28"],
)
```

---

## 模块四：代码质量工具

### 4.1 Black — 代码格式化器

```bash
# 安装
pip install black

# 格式化单个文件
black my_script.py

# 格式化整个项目
black .

# 检查模式（不修改文件）
black --check .

# 指定行宽
black --line-length 100 .
```

**配置（pyproject.toml）：**
```toml
[tool.black]
line-length = 88
target-version = ["py39", "py310"]
include = '\.pyi?$'
```

### 4.2 isort — import 排序

```bash
# 安装
pip install isort

# 排序
isort .

# 检查
isort --check-only .

# 显示 diff
isort --diff .
```

**配置（pyproject.toml）：**
```toml
[tool.isort]
profile = "black"       # 与 black 兼容
line_length = 88
known_first_party = ["my_project"]
```

### 4.3 flake8 — 代码检查

```bash
# 安装
pip install flake8

# 检查
flake8 .

# 指定文件
flake8 src/my_project/

# 显示代码
flake8 --show-source .
```

**配置（.flake8）：**
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503    # 与 black 兼容
exclude =
    .git,
    __pycache__,
    build,
    dist,
    .venv
per-file-ignores =
    __init__.py:F401
```

### 4.4 组合使用

```bash
# 一键检查
black --check . && isort --check-only . && flake8 .

# 自动修复
black . && isort . && flake8 --fix .
```

---

## 模块五：Makefile 与开发自动化

### 5.1 Makefile 基础

```makefile
.PHONY: help install dev test lint format clean build

help:               ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:            ## 安装依赖
	pip install -r requirements.txt

dev:                ## 安装开发依赖
	pip install -e ".[dev]"

test:               ## 运行测试
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:               ## 代码检查
	black --check .
	isort --check-only .
	flake8 .

format:             ## 格式化代码
	black .
	isort .

clean:              ## 清理构建文件
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:              ## 构建包
	python -m build

typecheck:          ## 类型检查
	mypy src/
```

### 5.2 tox 基础

tox 用于在多个 Python 版本中运行测试。

```ini
# tox.ini
[tox]
envlist = py39, py310, py311
isolated_build = true

[testenv]
deps =
    -r requirements/test.txt
commands =
    pytest tests/ {posargs}

[testenv:lint]
deps =
    black
    isort
    flake8
commands =
    black --check .
    isort --check-only .
    flake8 .
```

### 5.3 .gitignore 模板

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
*.egg

# 虚拟环境
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 测试/覆盖率
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# 系统
.DS_Store
Thumbs.db
```

---

## 模块六：动手练习

### 练习 1：创建项目结构
创建一个 src layout 的 Python 项目，包含 pyproject.toml、src 目录、tests 目录。

### 练习 2：配置工具链
在 pyproject.toml 中配置 black、isort、pytest。

### 练习 3：Makefile
编写 Makefile 包含 install、dev、test、lint、format、clean 目标。

### 练习 4：分层依赖
创建 requirements/base.txt、dev.txt、test.txt 三层依赖文件。

### 练习 5：打包发布
用 `python -m build` 构建你的包，检查生成的 wheel 和 sdist 文件。

---

## 常见错误汇总

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError` | 没装包或忘激活虚拟环境 | `pip install <pkg>` 或激活 `.venv` |
| `pip` 命令找不到 | Python 没加到 PATH | 重装 Python 勾选"Add to PATH" |
| `black` 和 `isort` 冲突 | 配置不一致 | isort 设置 `profile = "black"` |
| `setup.py` vs `pyproject.toml` | 混用两种方式 | 统一用 `pyproject.toml` |
| 包安装到系统 Python | 没用虚拟环境 | 始终在 `.venv` 中操作 |

## 实际应用场景

- **团队协作：** 统一的代码格式消除 style 争论
- **CI/CD：** 自动化 lint + test + build 流程
- **开源项目：** 标准结构让贡献者快速上手
- **微服务：** 每个服务独立虚拟环境，互不干扰
