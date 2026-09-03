# Day 31 终极挑战：创建 Python 包项目

## 项目名称
**pytools** — Python 实用工具包

## 需求

创建一个名为 `pytools` 的 Python 工具包，包含以下模块：

### P0 — 必须完成
- [ ] src layout 项目结构
- [ ] pyproject.toml 完整配置
- [ ] `pytools.text` 模块：文本处理工具（截断、统计、清洗等）
- [ ] `pytools.cli` 模块：命令行参数解析包装器
- [ ] `pytools.config` 模块：配置加载（JSON/YAML/ENV）
- [ ] 所有函数有类型注解和 docstring
- [ ] README.md 含安装和使用说明
- [ ] `pip install -e .` 可安装
- [ ] `python -m pytools` 可运行

### P1 — 应该完成
- [ ] 完整 .gitignore
- [ ] LICENSE（MIT）
- [ ] requirements.txt 导出
- [ ] 每个模块至少 3 个函数
- [ ] examples/ 下有可运行示例
- [ ] Git 使用 Conventional Commits

### P2 — 加分项
- [ ] 配置 uv 或 poetry
- [ ] 添加 pytest 测试
- [ ] 添加 CLI 入口点（[project.scripts]）
- [ ] 版本管理（__version__）
- [ ] CI 配置文件（.github/workflows/ci.yml）

## 验收标准
```bash
git clone <repo>
cd pytools
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"
python -c "from pytools.text import truncate; print(truncate('hello world', 5))"
# 输出: hello...
python -m pytools
# 显示工具包信息
```
