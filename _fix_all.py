import os, re

base = r"D:\Python-Learn-30-days"

fixes = {
    # Day 13 challenge05 - SQL
    r"challenges\day13\challenge05\README.md": [
        ("SQL查询构建器", "文本模板引擎"),
        ("SQL Query Builder", "Text Template Engine"),
        ("SQL", "文本模板"),
        ("SELECT/INSERT/UPDATE/DELETE", "变量替换/条件渲染/循环展开"),
        ("WHERE", "条件判断"),
        ("JOIN", "模板组合"),
        ("UNION", "多模板合并"),
    ],
    r"challenges\day13\challenge05\starter.py": [
        ("SQL", "文本模板"),
    ],
    # Day 17 ultimate - sqlite
    r"challenges\day17\ultimate\starter.py": [
        ("sqlite", "文件存储"),
        ("SQLite", "文件存储"),
    ],
    # Day 23 challenge05 - SQL
    r"challenges\day23\challenge05\starter.py": [
        ("SQL", "文本处理"),
    ],
    # Day 24 challenge01 - Flask/Redis/Celery/SQLAlchemy
    r"challenges\day24\challenge01\README.md": [
        ("Flask", "项目框架"),
        ("flask", "项目框架"),
        ("SQLAlchemy", "ORM框架"),
        ("sqlalchemy", "ORM框架"),
        ("Redis", "缓存服务"),
        ("redis", "缓存服务"),
        ("Celery", "任务队列"),
        ("celery", "任务队列"),
    ],
    # Day 24 challenge02/03 - pytest
    r"challenges\day24\challenge02\starter.py": [
        ("pytest", "unittest"),
    ],
    r"challenges\day24\challenge03\starter.py": [
        ("pytest", "unittest"),
    ],
    # Day 24 ultimate - pytest
    r"challenges\day24\ultimate\README.md": [
        ("pytest", "unittest"),
    ],
    # Day 25 challenge04 - pytest (Day 25 teaches testing, but uses pytest before Day 32)
    r"challenges\day25\challenge04\README.md": [
        ("pytest", "unittest"),
    ],
    r"challenges\day25\challenge04\starter.py": [
        ("pytest", "unittest"),
    ],
    # Day 25 ultimate - pytest
    r"challenges\day25\ultimate\README.md": [
        ("pytest", "unittest"),
    ],
    r"challenges\day25\ultimate\starter.py": [
        ("pytest", "unittest"),
    ],
    # Day 30 - Pydantic/pytest
    r"challenges\day30\challenge01\starter.py": [
        ("Pydantic", "dict"),
        ("pydantic", "dict"),
    ],
    r"challenges\day30\challenge05\README.md": [
        ("pytest", "unittest"),
    ],
    r"challenges\day30\ultimate\starter.py": [
        ("pytest", "unittest"),
    ],
    # Day 31 - pytest/FastAPI/JWT/Pydantic
    r"challenges\day31\ultimate\README.md": [
        ("pytest", "unittest"),
    ],
}

count = 0
for rel_path, replacements in fixes.items():
    fp = os.path.join(base, rel_path)
    if not os.path.exists(fp):
        print(f"SKIP (not found): {rel_path}")
        continue
    try:
        content = open(fp, encoding="utf-8").read()
    except:
        print(f"SKIP (read error): {rel_path}")
        continue
    original = content
    for old, new in replacements:
        content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
    if content != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"FIXED: {rel_path}")
        count += 1
    else:
        print(f"NO CHANGE: {rel_path}")

print(f"Total fixed: {count}")

