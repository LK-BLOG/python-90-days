import os
base = r"D:\Python-Learn-30-days"
days = [
    (84, "Permission System", ["RBAC", "ABAC", "Tool Permission", "User Auth", "Inheritance", "Audit Log"], "Perm Middleware"),
    (85, "Trace", ["Span/Trace/Context", "Agent Tracing", "Perf Monitor", "Cost Tracking", "Observability", "Distributed Trace"], "Observability Platform"),
    (86, "MCP", ["MCP Architecture", "MCP Server", "MCP Client", "Tool Standardization", "MCP Ecosystem", "Security"], "MCP Server Impl"),
    (87, "Multi-Agent", ["Collab Modes", "Communication", "Task Assignment", "Conflict Resolution", "Debugging", "Optimization"], "Multi-Agent Framework"),
    (88, "Runtime Architecture", ["Overall Arch", "Module Split", "DI/Interfaces", "Config System", "Plugin System", "Extensibility"], "Runtime Arch Impl"),
    (89, "Runtime Impl", ["Agent Loop", "Tool Engine", "Memory+State", "Sandbox+Perm", "Trace+Eval", "Error Handling"], "Full Runtime Impl"),
    (90, "Release", ["Testing", "Docs", "Packaging", "Deployment", "Graduation", "Maintenance"], "Graduation Project"),
]
for num, title, topics, boss in days:
    d = os.path.join(base, "day%02d" % num)
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Day %d: %s\n\n## Topics\n" % (num, title))
        for t in topics: f.write("- %s\n" % t)
        f.write("\n## Boss: %s\n" % boss)
    with open(os.path.join(d, "lesson.md"), "w", encoding="utf-8") as f:
        f.write("# %s\n\n" % title)
        for i, t in enumerate(topics, 1):
            f.write("## %d. %s\n\n### Concept\nCore concepts of %s.\n\n### Example\n```python\n# TODO\n```\n\n### Exercise\nModify the code.\n\n" % (i, t, t))
    with open(os.path.join(d, "challenge.md"), "w", encoding="utf-8") as f:
        f.write("# Day %d Challenges\n\n" % num)
        for c in range(1, 6):
            f.write("## Challenge %d\nImplement %s.\n\n" % (c, topics[(c-1)%len(topics)]))
    with open(os.path.join(d, "ultimate_challenge.md"), "w", encoding="utf-8") as f:
        f.write("# Boss: %s\n\n## Requirements\n" % boss)
        for t in topics: f.write("1. %s\n" % t)
    for j in range(1, 4):
        open(os.path.join(d, "examples", "%02d_example.py" % j), "w").write("# Example %d\n" % j)
    open(os.path.join(d, "starter", "exercise.py"), "w").write("# TODO\n")
    open(os.path.join(d, "tests", "test.py"), "w").write("import unittest\nclass T(unittest.TestCase):\n    def test(self): self.assertTrue(True)\n")
    open(os.path.join(d, "code", ".gitkeep"), "w").close()
    cdir = os.path.join(base, "challenges", "day%02d" % num)
    for ch in range(1, 6):
        chd = os.path.join(cdir, "challenge%02d" % ch)
        open(os.path.join(chd, "README.md"), "w").write("# Challenge %d\n" % ch)
        open(os.path.join(chd, "starter.py"), "w").write("# TODO\n")
    ultd = os.path.join(cdir, "ultimate")
    open(os.path.join(ultd, "README.md"), "w").write("# Boss: %s\n" % boss)
    open(os.path.join(ultd, "starter.py"), "w").write("# TODO\n")
    print("day%02d OK" % num)
print("All done")
