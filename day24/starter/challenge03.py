# Day 24 - Challenge 3: Makefile 构建系统
# 难度: ⭐⭐
# 为 Python 项目编写完整的 Makefile，支持常见构建目标

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class MakeTarget:
    """Makefile 目标"""
    name: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    recipe: list[str] = field(default_factory=list)


class MakefileGenerator:
    """Makefile 生成器

    自动生成包含 install、dev、test、lint、format、clean、build 等目标的 Makefile。
    """

    def __init__(self, project_name: str = "my_project"):
        """初始化

        Args:
            project_name: 项目名称
        """
        self.project_name = project_name
        # TODO: 注册所有默认目标
        self._targets: dict[str, MakeTarget] = {}

    def add_target(self, name: str, description: str,
                   dependencies: list[str] = None,
                   recipe: list[str] = None) -> None:
        """添加一个 Makefile 目标

        Args:
            name: 目标名称
            description: 目标描述
            dependencies: 依赖目标列表
            recipe: 执行命令列表
        """
        # TODO: 创建 MakeTarget 并注册
        ...

    def register_defaults(self) -> None:
        """注册所有默认构建目标"""
        # TODO: 注册以下目标：
        # - install: pip install -e .
        # - dev: pip install -e ".[dev]"
        # - test: pytest
        # - lint: ruff check .
        # - format: black . && ruff format .
        # - clean: 清理缓存和构建产物
        # - build: python -m build
        # - help: 显示所有可用目标
        ...

    def generate(self) -> str:
        """生成 Makefile 文本内容

        Returns:
            Makefile 文件的完整文本
        """
        # TODO: 生成符合 Makefile 语法的文本
        # 头部变量定义（PYTHON, SRC_DIR 等）
        # .PHONY 声明
        # 每个目标的描述和 recipe
        # help 目标自动列出所有命令
        ...

    def save(self, path: str = "Makefile") -> None:
        """保存 Makefile 到文件

        Args:
            path: 输出路径
        """
        # TODO: 调用 generate() 并写入文件
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    gen = MakefileGenerator("demo_project")
    gen.register_defaults()
    content = gen.generate()
    print(content)
