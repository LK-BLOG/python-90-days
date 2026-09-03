# Day 31 课程：Git & 项目结构

## 第一部分：Git 工作流

### 1.1 Git 核心命令

```bash
# 初始化仓库
git init

# 查看状态
git status

# 添加到暂存区
git add .                    # 所有文件
git add src/                 # 只添加 src 目录
git add -p                   # 交互式选择要暂存的代码块

# 提交
git commit -m "feat: 添加用户认证模块"

# 查看历史
git log --oneline --graph

# 分支操作
git branch feature/auth      # 创建分支
git checkout feature/auth    # 切换分支
git checkout -b feature/auth # 创建并切换
git switch feature/auth      # 新语法，等价于上面
git branch -d feature/auth   # 删除分支

# 合并
git checkout main
git merge feature/auth       # 合并到当前分支

# 变基（线性历史）
git checkout feature/auth
git rebase main              # 把 feature 分支的提交移到 main 最新之后
```

### 1.2 Rebase vs Merge

````
# Merge: 保留分支历史，产生合并提交
main:    A---B---C---M (merge commit)
                      /
feature:      D---E

# Rebase: 线性历史，重写提交
main:    A---B---C
                  \
feature:          D'---E'  (D' E' 是重放后的新提交)
````

**原则：** 本地分支用 rebase 保持整洁，公共分支用 merge 保留历史。

### 1.3 Commit Message 规范（Conventional Commits）

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型：**
- `feat`: 新功能
- `fix`: 修bug
- `docs`: 文档
- `style`: 格式调整（不影响逻辑）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建/工具/依赖
- `ci`: CI/CD 配置

**示例：**
```
feat(auth): 添加 JWT 认证中间件

- 实现 token 生成和验证
- 添加 refresh token 机制
- 集成到 FastAPI 路由

Closes #23
```

### 1.4 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
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

# 环境变量
.env
.env.local

# 测试和覆盖率
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

**常见错误：** 已经提交了 .env 再想忽略——为时已晚。密码已经进了 git 历史。正确做法是先 .gitignore 再提交。

---

## 第二部分：Python 项目结构

### 2.1 两种主流布局

**Flat Layout（扁平布局）：**
````
my_project/
├── my_package/
│   ├── __init__.py
│   └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml
├── README.md
└── LICENSE
````

**Src Layout（推荐）：**
````
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml
├── README.md
└── LICENSE
````

**为什么 src layout 更好？**
- 防止 import 本地目录而不是安装的包（常见坑）
- 强制你通过 `pip install -e .` 安装后才能测试
- 与 CI/CD 流程更兼容

### 2.2 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-awesome-package"
version = "0.1.0"
description = "一个示例Python包"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "骆戡", email = " lk@example.com"}
]
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "black",
    "ruff",
    "mypy",
]

[project.scripts]
my-tool = "my_package.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
target-version = "py310"
```

### 2.3 setup.cfg（旧式，仍在使用）

```ini
[metadata]
name = my-awesome-package
version = 0.1.0

[options]
package_dir =
    = src
packages = find:
install_requires =
    requests>=2.28.0
    pydantic>=2.0

[options.packages.find]
where = src

[options.extras_require]
dev =
    pytest>=7.0
    pytest-cov
```

---

## 第三部分：虚拟环境

### 3.1 venv（标准库自带）

```bash
# 创建
python -m venv .venv

# 激活（Windows）
.venv\Scripts\activate

# 激活（Mac/Linux）
source .venv/bin/activate

# 退出
deactivate

# 导出依赖
pip freeze > requirements.txt

# 安装依赖
pip install -r requirements.txt
```

### 3.2 virtualenv（功能更强的第三方工具）

```bash
# 安装
pip install virtualenv

# 创建（可指定 Python 版本）
virtualenv -p python3.11 .venv

# 用法同 venv
```

### 3.3 依赖管理工具对比

```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│             │ requirements │   Poetry     │     uv       │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ 速度        │ 慢           │ 中等         │ 极快         │
│ 锁文件      │ 无           │ poetry.lock  │ uv.lock      │
│ 依赖分组    │ 手动         │ 内置         │ 内置         │
│ 发布到PyPI  │ 手动         │ poetry publish│ uv publish  │
│ 虚拟环境    │ 手动管理     │ 自动管理     │ 自动管理     │
│ 学习曲线    │ 低           │ 中           │ 低           │
│ 推荐场景    │ 简单项目     │ 成熟项目     │ 所有项目     │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

### 3.4 Poetry 使用

```bash
# 安装
pip install poetry

# 创建项目
poetry new my-project

# 添加依赖
poetry add requests
poetry add --group dev pytest

# 安装所有依赖
poetry install

# 运行命令
poetry run python -m my_package

# 发布
poetry build
poetry publish
```

### 3.5 uv 使用（推荐）

```bash
# 安装
pip install uv

# 创建虚拟环境
uv venv

# 添加依赖（极快）
uv pip install requests
uv pip install -e ".[dev]"

# 同步依赖
uv pip sync requirements.txt

# 生成 requirements
uv pip freeze > requirements.txt
```

---

## 常见错误

1. **忘记激活虚拟环境** → pip install 装到了全局
2. **requirements.txt 不区分依赖和开发依赖** → 生产环境装了一堆不需要的东西
3. **pyproject.toml 的 build-backend 写错** → pip install 报错
4. **src layout 忘了在 src 下放 __init__.py** → import 失败
5. **rebase 公共分支** → 团队成员的代码全乱了

## 动手练习

1. 用 `git init` 创建一个仓库，写 .gitignore，做 3 次 conventional commit
2. 创建一个 src layout 的 Python 项目，配置 pyproject.toml
3. 用 venv 创建虚拟环境，pip install 几个包，导出 requirements.txt
4. 把之前的某个小项目重构为专业工程结构
