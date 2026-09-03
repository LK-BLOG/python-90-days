# Day 58 课程：打包 & 分发

## 第一部分：打包概述

### 1.1 打包工具演进
distutils → setuptools → flit → poetry → hatchling

### 1.2 包结构
my_package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
└── docs/

---

## 第二部分：pyproject.toml

### 2.1 完整配置
`	oml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-awesome-package"
version = "1.2.3"
description = "A short description"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
dependencies = [
    "fastapi>=0.100",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[project.scripts]
my-tool = "my_package.cli:main"

[project.urls]
Homepage = "https://github.com/you/my-package"
`

---

## 第三部分：版本管理

### 3.1 Semantic Versioning
MAJOR.MINOR.PATCH
1.0.0 → 1.0.1 → 1.1.0 → 2.0.0

### 3.2 动态版本
`	oml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_package/__init__.py"
`

---

## 第四部分：发布到PyPI

### 4.1 构建和发布
`ash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
`

### 4.2 GitHub Actions自动发布
在release事件触发时，自动构建并发布到PyPI。

---

## 本课总结

| 概念 | 说明 |
|------|------|
| pyproject.toml | 统一打包配置 |
| hatchling | 推荐的构建后端 |
| wheel | 二进制分发格式 |
| twine | PyPI上传工具 |
| SemVer | 版本号规范 |
