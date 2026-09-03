# Day 60 课程：项目部署 & DevOps

## 第一部分：CI/CD

### 1.1 持续集成/持续部署
代码提交 -> 自动测试 -> 自动构建 -> 自动部署

### 1.2 GitHub Actions
- 矩阵策略测试多Python版本
- 自动lint + type check + test
- 测试通过后自动部署
- 使用secrets管理敏感信息

### 1.3 GitLab CI
- stages: test -> build -> deploy
- Docker镜像构建和推送
- K8s滚动更新

---

## 第二部分：部署策略

### 2.1 蓝绿部署
蓝色（当前版本）接收流量 -> 部署绿色 -> 测试通过 -> 切换流量 -> 回滚切回蓝色

### 2.2 金丝雀部署
95个v1实例 + 5个v2实例 -> 监控指标 -> 正常则逐步扩大 -> 全量切换

### 2.3 滚动更新
10个实例，一次更新2个，逐步替换直到全部更新完成

---

## 第三部分：Kubernetes基础

### 3.1 核心概念
- Pod: 最小部署单元
- Deployment: 管理Pod副本
- Service: 服务发现和负载均衡
- Ingress: HTTP路由
- ConfigMap/Secret: 配置管理

### 3.2 关键配置
- replicas: 副本数
- resources: CPU/内存限制
- livenessProbe: 健康检查
- env: 环境变量（从Secret读取）

---

## 第四部分：监控告警

### 4.1 Prometheus + Grafana
- Prometheus: 指标收集
- Grafana: 可视化Dashboard
- AlertManager: 告警通知

### 4.2 应用指标
- Counter: 计数器（请求数）
- Histogram: 直方图（延迟分布）
- Gauge: 仪表盘（当前值）

### 4.3 告警规则
- 高错误率: 5xx > 10%
- 高延迟: P95 > 1s
- 磁盘空间: < 10%

---

## 第五部分：日志聚合

### 5.1 ELK/EFK栈
- Elasticsearch: 存储和搜索
- Logstash/Fluentd: 收集和转换
- Kibana: 可视化

### 5.2 结构化日志
- 使用structlog
- 包含request_id/method/path/status/duration
- JSON格式输出

### 5.3 Docker日志
- fluentd日志驱动
- 自动转发到ELK

---

## 本课总结

| 模块 | 关键点 |
|------|--------|
| CI/CD | 自动测试+构建+部署 |
| 蓝绿部署 | 零停机切换 |
| 金丝雀 | 渐进式发布 |
| K8s | 容器编排 |
| Prometheus | 指标收集 |
| ELK | 日志聚合 |
