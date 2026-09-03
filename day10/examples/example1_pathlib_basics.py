# 示例：pathlib基础操作
from pathlib import Path
import os

# 1. 创建路径对象
print("=== 创建路径对象 ===")
file_path = Path("documents/report.txt")
dir_path = Path("/home/user/projects")
print(f"文件路径: {file_path}")
print(f"目录路径: {dir_path}")

# 2. 路径拼接
print("\n=== 路径拼接 ===")
base = Path("/home/user")
full_path = base / "documents" / "report.txt"
print(f"完整路径: {full_path}")

# 3. 路径解析
print("\n=== 路径解析 ===")
path = Path("/home/user/documents/report.txt")
print(f"文件名: {path.name}")
print(f"文件名（无扩展名）: {path.stem}")
print(f"扩展名: {path.suffix}")
print(f"父目录: {path.parent}")
print(f"路径部分: {path.parts}")

# 4. 文件操作
print("\n=== 文件操作 ===")
# 创建测试文件
test_file = Path("test_file.txt")
test_file.write_text("Hello, World!", encoding='utf-8')

# 检查文件
print(f"文件存在: {test_file.exists()}")
print(f"是文件: {test_file.is_file()}")
print(f"是目录: {test_file.is_dir()}")
print(f"文件大小: {test_file.stat().st_size} 字节")

# 读取文件
content = test_file.read_text(encoding='utf-8')
print(f"文件内容: {content}")

# 5. 目录操作
print("\n=== 目录操作 ===")
# 创建目录
test_dir = Path("test_directory")
test_dir.mkdir(exist_ok=True)

# 创建多级目录
multi_dir = Path("parent/child/grandchild")
multi_dir.mkdir(parents=True, exist_ok=True)

# 列出目录内容
print("当前目录内容:")
for item in Path(".").iterdir():
    if item.is_file():
        print(f"  文件: {item.name}")
    elif item.is_dir():
        print(f"  目录: {item.name}/")

# 6. glob模式匹配
print("\n=== glob模式匹配 ===")
# 创建一些测试文件
for i in range(3):
    (Path(f"test_{i}.txt")).write_text(f"测试 {i}")

# 查找所有.txt文件
txt_files = list(Path(".").glob("*.txt"))
print(f"所有.txt文件: {[f.name for f in txt_files]}")

# 查找所有test_开头的文件
test_files = list(Path(".").glob("test_*.txt"))
print(f"test_开头的文件: {[f.name for f in test_files]}")

# 7. 清理
print("\n=== 清理 ===")
# 删除测试文件
for f in Path(".").glob("test_*.txt"):
    f.unlink()

# 删除测试目录
import shutil
if test_dir.exists():
    shutil.rmtree(test_dir)
if Path("parent").exists():
    shutil.rmtree("parent")

print("演示完成，测试文件已清理")
