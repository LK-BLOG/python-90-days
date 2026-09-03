# Challenge 03: Makefile 构建系统

## 项目名称：MakeBuild

## 目标
为 Python 项目编写一个智能的 Makefile 构建系统。

## 功能要求

### 1. 基础 targets
- install: 安装依赖
- dev: 安装开发依赖
- test: 运行测试
- lint: 代码检查
- format: 格式化代码
- clean: 清理构建文件
- build: 构建包

### 2. 高级 targets
- typecheck: 类型检查（mypy）
- coverage: 生成覆盖率报告
- docs: 生成文档
- docker-build: 构建 Docker 镜像
- docker-run: 运行 Docker 容器
- release: 发布到 PyPI

### 3. 智能功能
- 自动检测虚拟环境
- 自动检测 Python 版本
- 支持自定义配置
- 显示执行时间

### 4. 帮助系统
- 自动生成帮助信息
- 显示所有可用 targets
- 显示每个 target 的描述

## 输入
- 项目配置（pyproject.toml）
- 可选：Makefile.conf 配置文件

## 输出
完整的 Makefile

## 限制
- 支持 Linux/macOS/Windows（WSL）
- 不能依赖非标准工具
- 支持增量构建

## 示例
```
$ make help
可用命令：
  install        安装生产依赖
  dev            安装开发依赖
  test           运行测试套件
  lint           代码质量检查
  format         自动格式化代码
  clean          清理构建文件
  build          构建 wheel 和 sdist
  typecheck      运行 mypy 类型检查
  coverage       生成覆盖率报告
  docker-build   构建 Docker 镜像
  docker-run     运行 Docker 容器
  release        发布到 PyPI
```

## 验收标准
- [ ] 所有 targets 可正常执行
- [ ] help 显示所有 targets
- [ ] 支持依赖关系（如 lint 依赖 format）
- [ ] 清理功能完整
- [ ] 跨平台兼容

## 可选扩展
- 支持 watch 模式（文件变化自动执行）
- 支持并行执行
- 集成 pre-commit hooks
- 支持自定义插件
