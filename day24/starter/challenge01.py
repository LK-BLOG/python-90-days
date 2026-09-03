# Day 24 - Challenge 1: 依赖管理器
# 难度: ⭐⭐
# 解析 requirements.txt，列出依赖、检查安装状态、检查更新、生成 requirements.txt

import subprocess
import sys
from typing import NamedTuple


class PackageInfo(NamedTuple):
    """包信息"""
    name: str
    version_installed: str | None
    version_required: str | None
    has_update: bool


class DependencyManager:
    """依赖管理工具

    功能：
    - 解析 requirements.txt
    - 检查已安装/未安装的包
    - 检查可用更新
    - 生成 requirements.txt
    """

    def __init__(self, requirements_path: str = "requirements.txt"):
        """初始化依赖管理器

        Args:
            requirements_path: requirements.txt 文件路径
        """
        self.requirements_path = requirements_path
        # TODO: 初始化内部状态
        self._packages: dict[str, str | None] = {}

    def parse_requirements(self) -> dict[str, str | None]:
        """解析 requirements.txt 文件

        Returns:
            包名 -> 版本约束 的映射，版本为 None 表示无版本约束
        """
        # TODO: 读取文件，逐行解析包名和版本
        # 处理格式：package, package==1.0, package>=1.0
        # 忽略注释行和空行
        ...

    def check_installed(self) -> list[PackageInfo]:
        """检查哪些包已安装、哪些未安装、哪些有更新

        Returns:
            PackageInfo 列表
        """
        # TODO: 用 pip show 检查每个包的安装状态
        # TODO: 对比已安装版本和最新可用版本
        ...

    def check_updates(self) -> list[PackageInfo]:
        """检查哪些包有更新可用

        Returns:
            有更新的包列表
        """
        # TODO: 使用 pip index versions 或类似方法查询最新版本
        ...

    def generate_requirements(self, output_path: str = "requirements.txt") -> str:
        """生成当前环境的 requirements.txt

        Args:
            output_path: 输出文件路径

        Returns:
            生成的文件内容
        """
        # TODO: 用 pip freeze 获取当前环境的包列表
        # TODO: 写入到文件并返回内容
        ...

    def summary(self) -> str:
        """生成依赖状态摘要

        Returns:
            Markdown 格式的摘要
        """
        # TODO: 生成包含已安装/未安装/可更新 统计的摘要
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    dm = DependencyManager()
    print("=== 解析 requirements.txt ===")
    packages = dm.parse_requirements()
    print(f"找到 {len(packages)} 个依赖")

    print("\n=== 检查安装状态 ===")
    for info in dm.check_installed():
        status = "✅" if info.version_installed else "❌"
        print(f"  {status} {info.name}: {info.version_installed or '未安装'}")

    print("\n=== 检查更新 ===")
    updates = dm.check_updates()
    print(f"  {len(updates)} 个包有更新")
