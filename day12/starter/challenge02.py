# Day 12 - Challenge 2: 依赖管理
# 难度: ⭐⭐⭐☆☆
#
# 要求: 创建 requirements.txt、pyproject.toml、处理可选依赖
# 参考 challenge.md

"""
依赖管理挑战 — 学习 Python 项目依赖管理

核心知识点:
- requirements.txt 的写法和版本锁定
- pyproject.toml 的现代配置方式
- 可选依赖 (extras)
- 虚拟环境隔离
"""

from dataclasses import dataclass, field


# ===== 依赖规格模拟 =====

@dataclass
class Dependency:
    """依赖规格

    Attributes:
        name: 包名
        version: 版本约束（如 ">=1.0"）
        optional: 是否可选
        group: 所属依赖组
        extras: 额外特性列表
    """
    name: str
    version: str = ""
    optional: bool = False
    group: str = "main"
    extras: list = field(default_factory=list)

    def __str__(self) -> str:
        """返回 pip 风格的字符串

        Example:
            str(Dependency("requests", ">=2.28"))
            -> "requests>=2.28"
        """
        # TODO: 拼接 name + version
        pass

    def __eq__(self, other) -> bool:
        # TODO: 按 name 比较
        pass


@dataclass
class ProjectSpec:
    """项目规格

    Attributes:
        name: 项目名
        version: 项目版本
        python_requires: Python 版本要求
        dependencies: 主依赖列表
        dev_dependencies: 开发依赖
        test_dependencies: 测试依赖
    """
    name: str
    version: str = "0.1.0"
    python_requires: str = ">=3.10"
    dependencies: list = field(default_factory=list)
    dev_dependencies: list = field(default_factory=list)
    test_dependencies: list = field(default_factory=list)


class RequirementsWriter:
    """requirements.txt 生成器

    将 Dependency 列表写为标准 requirements.txt 格式。
    """

    def __init__(self, project: ProjectSpec):
        # TODO: 保存项目规格
        pass

    def generate_main(self) -> str:
        """生成主依赖的 requirements.txt 内容

        Returns:
            每行一个依赖的字符串
        """
        # TODO: 遍历 dependencies，生成 "name>=version" 格式
        pass

    def generate_dev(self) -> str:
        """生成开发依赖 (requirements-dev.txt)"""
        # TODO: 遍历 dev_dependencies
        pass

    def generate_all(self) -> str:
        """生成包含所有依赖的 requirements.txt"""
        # TODO: 合并主依赖 + 开发依赖 + 测试依赖
        pass

    def validate(self) -> list[str]:
        """验证依赖规格，返回警告信息

        Returns:
            警告信息列表（空列表表示无警告）
        """
        warnings = []
        # TODO: 检查重复依赖、版本冲突等
        # 提示: 用 dict 检查 name 是否重复
        return warnings


class PyProjectWriter:
    """pyproject.toml 生成器"""

    def __init__(self, project: ProjectSpec):
        self.project = project

    def to_toml(self) -> str:
        """生成 pyproject.toml 内容（简易版）

        Returns:
            TOML 格式字符串

        Hint:
            使用 f-string 手动构建（不依赖第三方 TOML 库）
        """
        # TODO: 构建 [build-system]、[project]、[project.optional-dependencies] 段
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 依赖管理测试 ===")

    proj = ProjectSpec(
        name="my-toolkit",
        version="1.0.0",
        dependencies=[
            Dependency("requests", ">=2.28"),
            Dependency("click", ">=8.0"),
        ],
        dev_dependencies=[
            Dependency("pytest", ">=7.0"),
            Dependency("black", ">=22.0"),
        ],
    )

    writer = RequirementsWriter(proj)
    print("--- main ---")
    print(writer.generate_main())
    print("--- all ---")
    print(writer.generate_all())

    warnings = writer.validate()
    if warnings:
        print(f"警告: {warnings}")

    toml_writer = PyProjectWriter(proj)
    print("\n--- pyproject.toml ---")
    print(toml_writer.to_toml())

    print("✅ Challenge 02 完成")
