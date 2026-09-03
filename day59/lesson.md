# Day 59 课程：代码质量 & 审查

## 第一部分：静态分析

### 1.1 mypy — 类型检查
`ash
pip install mypy
mypy src/
`

`	oml
# pyproject.toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
`

### 1.2 pyright — 另一个类型检查器
`ash
pip install pyright
pyright src/
`
pyright更快，但mypy更成熟。

### 1.3 pylint — 代码质量分析
`ash
pip install pylint
pylint src/my_package/
`

### 1.4 ruff — 超快的linter
`ash
pip install ruff
ruff check src/
ruff format src/
`

ruff用Rust写的，比flake8/isort/black加起来还快。

---

## 第二部分：代码格式化

### 2.1 black — 不可讨论的格式化
`ash
pip install black
black src/ tests/
black --check src/  # 只检查不修改
black --diff src/   # 显示差异
`

### 2.2 ruff format（替代black）
`ash
ruff format src/
ruff format --check src/
`

### 2.3 isort — 导入排序
`ash
pip install isort
isort src/ tests/
isort --check-only src/
`

### 2.4 统一配置
`	oml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
]

[tool.ruff.lint.isort]
known-first-party = ["my_package"]
`

---

## 第三部分：Pre-commit hooks

### 3.1 配置
`ash
pip install pre-commit
pre-commit init
`

`yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
`

### 3.2 使用
`ash
# 安装hooks
pre-commit install

# 手动运行所有hooks
pre-commit run --all-files

# 运行特定hook
pre-commit run ruff --all-files
`

---

## 第四部分：代码审查

### 4.1 审查清单
1. **功能正确性** — 代码做了它该做的吗？
2. **边界情况** — 空输入/超大输入/并发？
3. **安全性** — SQL注入/XSS/敏感信息泄露？
4. **性能** — N+1查询/不必要的循环？
5. **可读性** — 命名/注释/结构清晰？
6. **测试** — 覆盖率/边界测试？

### 4.2 代码审查工具
`ash
# GitHub PR审查
gh pr checkout 123
gh pr review 123 --approve

# GitLab MR
glab mr checkout 123
`

---

## 本课总结

| 工具 | 用途 |
|------|------|
| mypy | 类型检查 |
| ruff | Lint + 格式化（替代black+isort+flake8） |
| pre-commit | Git hooks自动检查 |
| pylint | 代码质量评分 |
