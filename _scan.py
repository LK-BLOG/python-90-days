import os, re
base = r"D:\Python-Learn-30-days"
deps = {
    "SQL": 35, "SQLAlchemy": 35, "sqlite": 35,
    "Docker": 37, "docker": 37,
    "FastAPI": 33, "fastapi": 33,
    "Flask": 33, "flask": 33,
    "pytest": 32,
    "JWT": 34, "jwt": 34,
    "OAuth": 34, "oauth": 34,
    "Redis": 36, "redis": 36,
    "Celery": 40, "celery": 40,
    "Elasticsearch": 56, "elasticsearch": 56,
    "Pydantic": 33, "pydantic": 33,
    "aiohttp": 28,
}
violations = []
for dirpath, dirs, files in os.walk(base):
    if ".git" in dirpath or "__pycache__" in dirpath:
        continue
    dm = re.search(r"day(\d+)", dirpath)
    if not dm:
        continue
    day = int(dm.group(1))
    for f in files:
        if not f.endswith((".md", ".py")):
            continue
        fp = os.path.join(dirpath, f)
        try:
            content = open(fp, encoding="utf-8").read()
        except:
            continue
        for kw, threshold in deps.items():
            if day < threshold and re.search(r"\b" + re.escape(kw) + r"\b", content, re.IGNORECASE):
                rel = os.path.relpath(fp, base)
                violations.append(f"{rel}|{kw}|Day{threshold}|Day{day}")
for v in violations:
    print(v)
print(f"TOTAL:{len(violations)}")

