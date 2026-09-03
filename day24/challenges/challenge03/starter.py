"""
Challenge 03: Makefile 构建系统 - MakeBuild
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# Makefile 模板
MAKEFILE_TEMPLATE = """# 自动生成的 Makefile
# 项目: {project_name}
# 生成时间: {timestamp}

.PHONY: help install dev test lint format clean build \\
        typecheck coverage docs \\
        package|publish|build package|publish|build release

# 配置变量
PYTHON ?= python
PIP ?= pip
PROJECT_NAME ?= {project_name}
SRC_DIR ?= src
TEST_DIR ?= tests
DIST_DIR ?= dist
BUILD_DIR ?= build

help: ## 显示此帮助信息
\t@echo "可用命令："
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {{FS = ":.*?## "}}; {{printf "  \\033[36m%-20s\\033[0m %s\\n", $$1, $$2}}'

install: ## 安装生产依赖
\t$(PIP) install -r requirements.txt

dev: ## 安装开发依赖
\t$(PIP) install -e ".[dev]"

test: ## 运行测试套件
\t$(PYTHON) -m unittest $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=term-missing

test-quick: ## 快速运行测试（不生成覆盖率）
\t$(PYTHON) -m unittest $(TEST_DIR)/ -x -q

lint: format ## 代码质量检查
\t$(PYTHON) -m black --check .
\t$(PYTHON) -m isort --check-only .
\t$(PYTHON) -m flake8 .

format: ## 自动格式化代码
\t$(PYTHON) -m black .
\t$(PYTHON) -m isort .

typecheck: ## 类型检查
\t$(PYTHON) -m mypy $(SRC_DIR)/

coverage: test ## 生成覆盖率报告
\t$(PYTHON) -m coverage html
\t@echo "覆盖率报告已生成: htmlcov/index.html"

clean: ## 清理构建文件
\trm -rf $(DIST_DIR) $(BUILD_DIR) *.egg-info .unittest_cache .mypy_cache
\trm -rf htmlcov .coverage
\tfind . -type d -name __pycache__ -exec rm -rf {{}} + 2>/dev/null || true
\tfind . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean ## 深度清理（包括虚拟环境）
\trm -rf .venv venv

build: clean ## 构建 wheel 和 sdist
\t$(PYTHON) -m build

upload-test: build ## 上传到 TestPyPI
\t$(PYTHON) -m twine upload --repository testpypi $(DIST_DIR)/*

upload: build ## 上传到 PyPI
\t$(PYTHON) -m twine upload $(DIST_DIR)/*

docs: ## 生成文档
\t@echo "TODO: 实现文档生成"

package|publish|build: ## 构建 package|publish|build 镜像
\tpackage|publish|build -t $(PROJECT_NAME):latest .

package|publish|build: ## 运行 package|publish|build 容器
\tpackage|publish|build -it --rm $(PROJECT_NAME):latest

release: ## 发布新版本
\t@echo "TODO: 实现发布流程"

# 开发辅助
watch: ## 监视文件变化（需要 entr）
\t@echo "监视 $(SRC_DIR) 和 $(TEST_DIR) ..."
\twhile true; do \\
\t\tfind $(SRC_DIR) $(TEST_DIR) -name "*.py" | entr -d $(MAKE) test-quick; \\
\tdone

stats: ## 项目统计
\t@echo "=== 代码统计 ==="
\t@find $(SRC_DIR) -name "*.py" -exec cat {{}} + | wc -l
\t@echo "行 Python 代码"
\t@find $(TEST_DIR) -name "*.py" -exec cat {{}} + | wc -l
\t@echo "行测试代码"
"""


class MakefileGenerator:
    """Makefile 生成器"""
    
    def __init__(self, project_name: str, config_file: str = None):
        self.project_name = project_name
        self.config = self._load_config(config_file)
        self.targets = {}
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置"""
        default_config = {
            "python": "python",
            "pip": "pip",
            "src_dir": "src",
            "test_dir": "tests",
            "dist_dir": "dist",
            "build_dir": "build",
        }
        
        if config_file and os.path.exists(config_file):
            # TODO: 加载配置文件
            pass
        
        return default_config
    
    def add_target(self, name: str, commands: List[str], 
                   description: str = "", dependencies: List[str] = None):
        """添加 target"""
        # TODO: 实现
        pass
    
    def generate(self) -> str:
        """生成 Makefile 内容"""
        # TODO: 实现
        pass
    
    def write(self, output_path: str = "Makefile"):
        """写入 Makefile"""
        content = self.generate()
        Path(output_path).write_text(content, encoding="utf-8")
        print(f"Makefile 已生成: {output_path}")


def generate_makefile_from_pyproject(project_dir: str = ".") -> str:
    """从 pyproject.toml 生成 Makefile"""
    # TODO: 实现
    # 读取 pyproject.toml
    # 提取项目名称、依赖等信息
    # 生成定制的 Makefile
    pass


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Makefile 生成器")
    parser.add_argument("--project-name", default="my_project", help="项目名称")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--output", default="Makefile", help="输出文件")
    
    args = parser.parse_args()
    
    generator = MakefileGenerator(args.project_name, args.config)
    
    # 添加默认 targets
    generator.add_target("help", ["@echo '可用命令：'"], "显示帮助信息")
    generator.add_target("install", ["pip install -r requirements.txt"], "安装依赖")
    generator.add_target("test", ["unittest tests/ -v"], "运行测试")
    generator.add_target("lint", ["black --check .", "isort --check-only ."], "代码检查")
    generator.add_target("format", ["black .", "isort ."], "格式化代码")
    generator.add_target("clean", ["rm -rf dist/ build/"], "清理")
    
    generator.write(args.output)
    print(f"Makefile 已生成: {args.output}")


if __name__ == "__main__":
    main()

