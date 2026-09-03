import os
base = r"D:\Python-Learn-30-days"
days = {
    61: ("通用LLM客户端", "封装一个支持多模型、多参数、Token计数、流式输出的通用LLM客户端"),
    62: ("Prompt模板引擎", "实现一个支持变量注入、Few-shot、CoT的Prompt模板系统"),
    63: ("Prompt优化系统", "实现一个带注入检测、A/B测试、上下文管理的Prompt优化框架"),
    64: ("多工具AI助手", "实现一个支持工具注册、调用解析、多工具组合的AI助手"),
    65: ("MiniRAG系统", "实现一个完整的RAG系统：分块、嵌入、向量存储、检索、生成"),
    69: ("AI应用网关", "实现一个带限流、重试、缓存、成本追踪的AI应用网关"),
    70: ("多模态助手", "实现一个支持图片、语音、文本的多模态AI助手"),
    71: ("微调数据集管理", "实现一个支持多格式、验证、版本控制的微调数据集管理工具"),
    72: ("AI安全过滤器", "实现一个带内容过滤、幻觉检测、审核日志的安全过滤系统"),
    73: ("RAG评估平台", "实现一个支持多指标、自动化测试、报告生成的RAG评估平台"),
    74: ("文档解析管道", "实现一个支持PDF/DOCX/HTML的文档解析、分块、嵌入管道"),
    75: ("完整文档助手", "实现一个带多轮对话、引用溯源、答案验证的文档问答助手"),
}
for day_num, (name, desc) in days.items():
    d = os.path.join(base, "challenges", f"day{day_num:02d}", "challenge05")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# Boss: {name}\n\n## 目标\n{desc}\n\n## 难度\n★★★★★\n\n## 验收标准\n- [ ] 核心功能完整\n- [ ] 错误处理健壮\n- [ ] 代码结构清晰\n- [ ] 可直接运行\n")
    with open(os.path.join(d, "starter.py"), "w", encoding="utf-8") as f:
        f.write(f"# Boss: {name}\n# Day {day_num}\n\ndef main():\n    # TODO\n    print(\"{name}\")\n\nif __name__ == \"__main__\":\n    main()\n")
    print(f"  day{day_num:02d}/challenge05/ OK")
print("Done")

