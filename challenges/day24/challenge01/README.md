# Challenge 01: 依赖管理器

## 项目名称：DepTracker

## 目标
编写一个依赖管理工具，自动分析 Python 项目的依赖关系。

## 背景
在实际开发中，我们需要管理项目的依赖包。一个好用的依赖管理器能帮助我们：
- 追踪哪些包是项目真正需要的
- 检测未声明的依赖
- 生成标准化的 requirements.txt

## 功能要求

### 1. 依赖扫描
- 扫描项目中所有 .py 文件
- 提取所有 import 语句
- 区分标准库、第三方包、本地模块

### 2. 依赖分析
- 解析 requirements.txt
- 检查哪些依赖已安装、哪些未安装
- 检查版本冲突

### 3. 依赖报告
- 生成依赖树
- 显示每个包的版本信息
- 标记未声明但被使用的依赖

### 4. 自动修复
- 自动生成 requirements.txt
- 支持添加缺失的依赖
- 支持锁定版本

## 输入
- 项目根目录路径
- 可选：requirements.txt 路径

## 输出
- 依赖分析报告（Markdown 格式）
- 更新后的 requirements.txt

## 限制
- 不能使用 pip 自身的 API
- 必须能正确区分标准库和第三方包
- 支持 Python 3.9+

## 示例
```
$ python dep_tracker.py ./my_project
依赖分析报告：
================
项目: my_project
Python: 3.11.0

已声明的依赖 (5):
  requests==2.28.1 ✓
  项目框架==2.3.2 ✓
  ORM框架==2.0.0 ✓
  任务队列==5.3.0 ✓
  缓存服务==4.5.0 ✓

未声明但使用的依赖 (2):
  click (来自 项目框架)
  jinja2 (来自 项目框架)

未使用的声明依赖 (1):
  任务队列

建议:
  - 添加: click, jinja2
  - 移除: 任务队列
```

## 验收标准
- [ ] 能正确扫描项目中的 import
- [ ] 能区分标准库和第三方包
- [ ] 能生成 Markdown 格式报告
- [ ] 能检测未声明的依赖
- [ ] 能生成 requirements.txt

## 可选扩展
- 支持 requirements.txt 分层（base/dev/test）
- 支持虚拟环境检测
- 生成依赖关系图（DOT 格式）
- 支持 pyproject.toml 格式
