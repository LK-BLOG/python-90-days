# Challenge 02: 项目脚手架生成器

## 项目名称：PyScaffold

## 目标
编写一个命令行工具，一键生成标准 Python 项目结构。

## 背景
每次开始新项目都要手动创建目录和文件，费时费力。一个好的脚手架工具能让你专注于代码。

## 功能要求

### 1. 项目生成
- 输入项目名称，生成完整的项目结构
- 支持 src layout 和 flat layout
- 自动生成 pyproject.toml（带正确的项目名）

### 2. 模板定制
- 支持自定义作者、邮箱、许可证
- 支持选择 Python 版本
- 支持选择是否包含 CI 配置

### 3. 文件生成
- README.md（带项目名称和描述）
- .gitignore（Python 模板）
- Makefile（基础 targets）
- requirements/dev.txt、test.txt

### 4. Git 初始化
- 可选自动 git init
- 自动创建初始 commit

## 输入
- 项目名称（必需）
- 选项：--layout, --author, --email, --license, --python-version, --no-ci, --no-git

## 输出
完整的项目目录结构

## 限制
- 生成的 pyproject.toml 必须能通过 `python -m build`
- 生成的代码必须通过 black 检查
- 支持 Python 3.9+

## 示例
```
$ python pyscaffold.py my_awesome_project --layout src --author "张三"
正在创建项目: my_awesome_project

创建目录结构...
生成配置文件...
初始化 Git 仓库...

项目创建成功！

目录结构：
my_awesome_project/
├── src/my_awesome_project/__init__.py
├── tests/__init__.py
├── pyproject.toml
├── Makefile
├── .gitignore
└── README.md

下一步：
  cd my_awesome_project
  python -m venv .venv
  .venv\\Scripts\\activate
  make dev
```

## 验收标准
- [ ] 能生成正确的目录结构
- [ ] 生成的 pyproject.toml 格式正确
- [ ] 生成的 Makefile 可执行
- [ ] 支持命令行参数
- [ ] 生成的 README 包含项目信息

## 可选扩展
- 支持从模板目录生成
- 支持交互式配置
- 集成 GitHub Actions 模板
- 支持 package|publish|buildfile 生成

