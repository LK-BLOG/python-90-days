# Day 31 - Challenge 3: 配置 pyproject.toml + 依赖管理
# 难度: ⭐⭐
# 完善 pyproject.toml、依赖管理、pip install -e .

from pathlib import Path


class PyprojectConfigurator:
    """pyproject.toml 配置器"""

    def __init__(self, project_name: str, version: str = "0.1.0",
                 python_requires: str = ">=3.10"):
        self.project_name = project_name
        self.version = version
        self.python_requires = python_requires
        self._dependencies: list[str] = []
        self._dev_dependencies: list[str] = []

    def add_dependency(self, name: str, version: str = "") -> "PyprojectConfigurator":
        """添加运行时依赖"""
        dep = f"{name}>={version}" if version else name
        self._dependencies.append(dep)
        return self

    def add_dev_dependency(self, name: str, version: str = "") -> "PyprojectConfigurator":
        """添加开发依赖"""
        dep = f"{name}>={version}" if version else name
        self._dev_dependencies.append(dep)
        return self

    def generate(self) -> str:
        """生成 pyproject.toml 内容"""
        deps = "\n".join(f'    "{d}",' for d in self._dependencies)
        dev_deps = "\n".join(f'    "{d}",' for d in self._dev_dependencies)
        return f"""[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "{self.project_name}"
version = "{self.version}"
requires-python = "{self.python_requires}"
dependencies = [
{deps}
]

[project.optional-dependencies]
dev = [
{dev_deps}
]

[project.scripts]
{self.project_name} = "{self.project_name}.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
"""

    def save(self, path: str = "pyproject.toml") -> None:
        """保存到文件"""
        Path(path).write_text(self.generate(), encoding="utf-8")


# ==================== 测试 ====================
if __name__ == "__main__":
    config = PyprojectConfigurator("my_tool")
    config.add_dependency("requests", "2.28")
    config.add_dependency("click")
    config.add_dev_dependency("pytest")
    config.add_dev_dependency("black")
    print(config.generate())
