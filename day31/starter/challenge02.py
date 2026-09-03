# Day 31 - Challenge 2: 创建项目结构（src layout）
# 难度: ⭐⭐
# 标准 src layout 项目骨架

from pathlib import Path
from typing import Optional


class ProjectStructureCreator:
    """项目结构创建器

    创建标准的 Python src layout 项目。
    """

    SRC_LAYOUT = {
        "src/{name}/__init__.py": '"""Package {name}"""\n\n__version__ = "0.1.0"\n',
        "src/{name}/__main__.py": 'def main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
        "src/{name}/cli.py": '"""命令行接口"""\nimport sys\n\ndef main():\n    print("CLI not implemented yet")\n',
        "src/{name}/utils.py": '"""工具函数"""\n',
        "src/{name}/config.py": '"""配置管理"""\n',
        "tests/__init__.py": "",
        "tests/test_cli.py": '"""CLI 测试"""\nimport pytest\n\ndef test_placeholder():\n    assert True\n',
        "examples/": None,
        "pyproject.toml": None,
    }

    def __init__(self, base_dir: str = ".", project_name: str = "my_tool"):
        self.base_dir = Path(base_dir)
        self.project_name = project_name

    def create(self) -> Path:
        """创建项目结构

        Returns:
            项目根目录路径
        """
        # TODO: 遍历 SRC_LAYOUT 创建文件
        # TODO: 替换 {name} 占位符
        ...

    def _create_pyproject(self) -> str:
        """生成 pyproject.toml"""
        # TODO: 生成标准 pyproject.toml
        ...

    def make_executable(self) -> None:
        """设置 __main__.py 可执行"""
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    creator = ProjectStructureCreator(project_name="my_tool")
    print("项目结构创建器就绪")
    print(f"将创建: {creator.SRC_LAYOUT.keys()}")
