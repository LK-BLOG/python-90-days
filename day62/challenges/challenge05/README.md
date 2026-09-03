# Challenge 05: Prompt 模板系统

## Boss 挑战

前 4 个挑战分别实现了模板引擎、Few-shot、CoT 构建和 Prompt 优化。现在整合为一个完整的 **Prompt 模板管理系统**。

## 目标

实现 `PromptTemplateSystem` 类，支持：
- 模板定义（变量插槽 `{{var}}`、条件块 `{% if %}`、循环 `{% for %}`）
- 模板继承与组合（base template + overrides）
- 版本管理（保存/回滚/对比历史版本）
- Few-shot 示例自动选择（根据输入相似度选取最相关示例）
- A/B 测试框架（同一输入随机分配不同 Prompt，收集效果数据）
- Prompt 库管理（分类/搜索/标签）

## 验收标准
- [ ] 模板引擎支持变量、条件、循环
- [ ] 模板可以继承和覆盖
- [ ] 版本历史可查询和回滚
- [ ] Few-shot 示例按相似度自动选取 Top-K
- [ ] A/B 测试能统计各版本胜率
- [ ] Prompt 库支持标签搜索
- [ ] 通过 test_day62.py 全部测试
