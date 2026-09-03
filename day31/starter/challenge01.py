# Day 31 - Challenge 1: Git 仓库初始化
# 难度: ⭐
# 规范的 Git 仓库、.gitignore、Conventional Commits

import subprocess
import sys
from pathlib import Path


class GitInitializer:
    """Git 仓库初始化器"""

    PYTHON_GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project
*.log
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
"""

    def __init__(self, project_dir: str):
        """初始化

        Args:
            project_dir: 项目目录
        """
        self.project_dir = Path(project_dir)

    def init_repo(self) -> bool:
        """初始化 Git 仓库"""
        # TODO: git init
        # TODO: 创建 .gitignore
        # TODO: 创建 README.md
        ...

    def create_gitignore(self) -> None:
        """创建 .gitignore 文件"""
        # TODO: 写入 PYTHON_GITIGNORE
        ...

    def initial_commit(self, message: str = "feat: initial commit") -> None:
        """创建初始提交"""
        # TODO: git add . && git commit -m message
        ...

    def create_feature_branch(self, branch_name: str) -> None:
        """创建功能分支"""
        # TODO: git checkout -b branch_name
        ...

    def commit(self, message: str) -> None:
        """创建 Conventional Commit"""
        # TODO: git add . && git commit -m message
        ...

    def rebase_to_main(self) -> None:
        """Rebase 到 main 分支"""
        # TODO: git checkout main && git merge feature-branch
        ...

    def show_log(self) -> str:
        """显示 git log --oneline --graph"""
        # TODO: 执行 git log --oneline --graph 并返回输出
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    init = GitInitializer("./demo_repo")
    print("Git 仓库初始化器就绪")
    print("请取消注释 init.init_repo() 开始使用")
