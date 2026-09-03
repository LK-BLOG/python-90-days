# Day 24: Python 工程化

## 📋 学习目标

完成今天的学习后，你将能够：
- 使用 pip 管理 Python 包和依赖
- 创建和管理虚拟环境
- 理解 pyproject.toml 和现代 Python 打包
- 搭建标准 Python 项目结构
- 配置代码质量工具（black、isort、flake8）
- 使用 Makefile 和 tox 简化开发流程

## 📚 学习内容

| 模块 | 内容 | 文件 |
|------|------|------|
| pip 包管理 | install/freeze/list/uninstall/requirements.txt | lesson.md |
| 虚拟环境 | venv 创建、激活、管理 | lesson.md |
| 项目打包 | pyproject.toml、setuptools、项目结构 | lesson.md |
| 代码质量 | black、isort、flake8 配置与使用 | lesson.md |
| 开发工具 | Makefile、tox、.gitignore | lesson.md |

## 🎯 挑战任务

| 挑战 | 名称 | 难度 |
|------|------|------|
| Challenge 01 | 依赖管理器 | ⭐⭐ |
| Challenge 02 | 项目脚手架生成器 | ⭐⭐⭐ |
| Challenge 03 | Makefile 构建系统 | ⭐⭐ |
| Challenge 04 | 配置文件解析器 | ⭐⭐⭐ |
| Challenge 05 | 代码质量检查器 | ⭐⭐⭐ |
| Ultimate | 专业工程结构重构 | ⭐⭐⭐⭐ |

## ⏰ 建议时间

- 理论学习：3-4 小时
- 练习 + 挑战：4-5 小时
- Boss 挑战：2-3 小时

## 🔑 核心概念速查

```
pip install requests          # 安装包
pip freeze > requirements.txt # 导出依赖
python -m venv myenv          # 创建虚拟环境
black .                       # 格式化代码
isort .                       # 排序 import
flake8 .                      # 代码检查
```
