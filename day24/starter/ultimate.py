# Day 24 - Boss Challenge: 专业工程结构重构
# 难度: ⭐⭐⭐⭐
# 把之前的项目重构为专业级 Python 工程

import subprocess
import sys
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    version: str = "0.1.0"
    author: str = ""
    description: str = ""
    python_requires: str = ">=3.10"
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=lambda: ["pytest", "black", "ruff"])


class ProfessionalProjectBuilder:
    """专业项目重构器

    将已有项目重构为标准 src layout + pyproject.toml + CI + 文档 的专业工程结构。
    """

    def __init__(self, source_dir: str, config: ProjectConfig):
        """初始化

        Args:
            source_dir: 原项目目录
            config: 项目配置
        """
        self.source_dir = Path(source_dir)
        self.config = config
        self.target_dir = Path(f"refactored_{config.name}")

    def create_structure(self) -> Path:
        """创建标准 src layout 目录结构

        Returns:
            新项目根目录
        """
        # TODO: 创建 src/{name}/, tests/, docs/ 等目录
        # TODO: 移动和重构源代码
        ...

    def setup_pyproject(self) -> None:
        """生成完整的 pyproject.toml"""
        # TODO: 包含项目元数据、依赖、工具配置（black/ruff/pytest）
        ...

    def setup_ci(self) -> None:
        """生成 GitHub Actions CI 配置"""
        # TODO: .github/workflows/ci.yml
        # TODO: 包含 lint、test、build 步骤
        ...

    def setup_docs(self) -> None:
        """生成项目文档"""
        # TODO: README.md（安装、使用、开发指南）
        # TODO: CHANGELOG.md
        # TODO: CONTRIBUTING.md
        ...

    def setup_quality_tools(self) -> None:
        """配置代码质量工具"""
        # TODO: 配置 black、ruff、mypy、pre-commit
        ...

    def migrate_code(self) -> list[str]:
        """迁移和重构源代码

        Returns:
            重构日志列表
        """
        # TODO: 分析原项目结构
        # TODO: 提取可复用模块
        # TODO: 添加类型注解
        # TODO: 添加 docstring
        ...

    def validate(self) -> bool:
        """验证重构后的项目

        Returns:
            是否通过验证
        """
        # TODO: 检查目录结构
        # TODO: 尝试 pip install -e .
        # TODO: 运行测试
        # TODO: 运行 linter
        ...

    def generate_report(self) -> str:
        """生成重构报告

        Returns:
            Markdown 格式的重构报告
        """
        # TODO: 列出所有变更
        # TODO: 显示文件统计
        # TODO: 给出后续建议
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    config = ProjectConfig(
        name="my_toolkit",
        version="1.0.0",
        author="小戡",
        description="我的工具集",
    )
    builder = ProfessionalProjectBuilder(".", config)
    report = builder.generate_report()
    print(report)
