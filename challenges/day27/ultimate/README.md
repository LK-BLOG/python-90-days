# DataAggregator — 多 API 聚合系统

> Day 27 终极挑战 | 难度：★★★★★

## 目标

构建一个多数据源聚合系统，从多个 API 并发获取数据、缓存结果，并生成结构化的 Markdown 报告。

## 功能要求

- **数据源注册**：动态注册数据源（名称、URL、解析函数、缓存 TTL）
- **单源获取**：支持缓存检查、HTTP 请求、自定义解析、缓存更新
- **并发获取**：使用 `ThreadPoolExecutor` 并发拉取所有已注册数据源，带超时控制和错误隔离
- **数据聚合**：
  - GitHub 数据聚合（用户信息、仓库数、 followers 等）
  - 天气数据聚合
  - 新闻数据聚合
- **报告生成**：输出包含标题、时间戳、各数据源详情和统计摘要的 Markdown 报告
- **报告持久化**：保存为本地 `.md` 文件

## 验收标准

- [ ] `register_source()` 能正确注册数据源及其解析函数
- [ ] `fetch_source()` 命中缓存时不再发请求（TTL 有效期内）
- [ ] `fetch_all()` 使用线程池并发执行，单个失败不影响其他源
- [ ] 各聚合方法（`aggregate_github/weather/news`）返回结构化字典
- [ ] `generate_report()` 输出格式正确的 Markdown 文档
- [ ] `save_report()` 将报告写入 `cache_dir` 目录
- [ ] 所有 TODO 注释处均已实现
