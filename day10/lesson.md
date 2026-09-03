# Day 10 完整教学：pathlib + os

## 1. pathlib基础
### 1.1 Path对象创建
**说明**：pathlib提供面向对象的路径操作。

**语法**：
```python
from pathlib import Path

# 创建路径对象
p = Path('file.txt')
p = Path('/home/user/file.txt')
p = Path('C:/Users/user/file.txt')
```

**示例**：
```python
from pathlib import Path

# 创建路径对象
file_path = Path('documents/report.txt')
dir_path = Path('projects/python')

print(f"文件路径: {file_path}")
print(f"目录路径: {dir_path}")
print(f"类型: {type(file_path)}")
```

### 1.2 路径拼接
**说明**：使用 `/` 运算符拼接路径。

**语法**：
```python
base = Path('/home/user')
full_path = base / 'documents' / 'report.txt'
```

**示例**：
```python
from pathlib import Path

# 路径拼接
base_dir = Path('/home/user')
project_dir = base_dir / 'projects' / 'python'
file_path = project_dir / 'main.py'

print(f"基础目录: {base_dir}")
print(f"项目目录: {project_dir}")
print(f"文件路径: {file_path}")
```

### 1.3 路径解析
**说明**：获取路径的各个部分。

**属性**：
- `name`：文件名
- `stem`：文件名（不含扩展名）
- `suffix`：扩展名
- `parent`：父目录
- `parts`：路径组成部分

**示例**：
```python
from pathlib import Path

file_path = Path('/home/user/documents/report.txt')

print(f"完整路径: {file_path}")
print(f"文件名: {file_path.name}")        # report.txt
print(f"文件名（无扩展名）: {file_path.stem}")  # report
print(f"扩展名: {file_path.suffix}")      # .txt
print(f"父目录: {file_path.parent}")      # /home/user/documents
print(f"路径部分: {file_path.parts}")     # ('/', 'home', 'user', 'documents', 'report.txt')
```

## 2. 文件操作
### 2.1 文件存在性检查
**方法**：
- `exists()`：是否存在
- `is_file()`：是否是文件
- `is_dir()`：是否是目录

**示例**：
```python
from pathlib import Path

# 检查存在性
file_path = Path('test.txt')
if file_path.exists():
    if file_path.is_file():
        print("这是一个文件")
    elif file_path.is_dir():
        print("这是一个目录")
else:
    print("路径不存在")
```

### 2.2 文件读写
**方法**：
- `read_text()`：读取文本
- `read_bytes()`：读取字节
- `write_text()`：写入文本
- `write_bytes()`：写入字节

**示例**：
```python
from pathlib import Path

# 写入文件
file_path = Path('example.txt')
file_path.write_text('Hello, World!', encoding='utf-8')

# 读取文件
content = file_path.read_text(encoding='utf-8')
print(content)

# 二进制写入
binary_path = Path('data.bin')
binary_path.write_bytes(b'\x00\x01\x02\x03')

# 二进制读取
binary_data = binary_path.read_bytes()
print(binary_data)
```

### 2.3 文件操作
**方法**：
- `mkdir()`：创建目录
- `rmdir()`：删除目录
- `unlink()`：删除文件
- `rename()`：重命名
- `replace()`：替换文件

**示例**：
```python
from pathlib import Path

# 创建目录
new_dir = Path('new_directory')
new_dir.mkdir(exist_ok=True)  # 如果已存在不报错

# 创建多级目录
multi_dir = Path('parent/child/grandchild')
multi_dir.mkdir(parents=True, exist_ok=True)

# 删除文件
temp_file = Path('temp.txt')
temp_file.write_text('临时文件')
temp_file.unlink()  # 删除文件

# 删除目录
empty_dir = Path('empty_dir')
empty_dir.mkdir(exist_ok=True)
empty_dir.rmdir()  # 删除空目录

# 重命名
old_name = Path('old_name.txt')
new_name = Path('new_name.txt')
old_name.write_text('重命名测试')
old_name.rename(new_name)
```

## 3. 目录遍历
### 3.1 遍历目录内容
**方法**：
- `iterdir()`：遍历目录内容
- `glob()`：模式匹配
- `rglob()`：递归模式匹配

**示例**：
```python
from pathlib import Path

# 遍历目录
dir_path = Path('.')
for item in dir_path.iterdir():
    if item.is_file():
        print(f"文件: {item.name}")
    elif item.is_dir():
        print(f"目录: {item.name}")

# 使用glob匹配
python_files = list(Path('.').glob('*.py'))
print(f"Python文件: {python_files}")

# 递归匹配
all_python_files = list(Path('.').rglob('*.py'))
print(f"所有Python文件: {all_python_files}")
```

### 3.2 目录树遍历
**示例**：
```python
from pathlib import Path

def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """打印目录树"""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            
            if item.is_dir():
                print(f"{prefix}{connector}{item.name}/")
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(item, new_prefix, max_depth, current_depth + 1)
            else:
                print(f"{prefix}{connector}{item.name}")
    except PermissionError:
        print(f"{prefix}[权限不足]")

# 使用示例
print("目录树:")
print_tree(Path('.'), max_depth=2)
```

## 4. glob模式匹配
### 4.1 基础模式
**模式**：
- `*`：匹配任意字符
- `?`：匹配单个字符
- `[seq]`：匹配字符序列
- `[!seq]`：不匹配字符序列

**示例**：
```python
from pathlib import Path

# 查找所有Python文件
py_files = list(Path('.').glob('*.py'))
print(f"Python文件: {py_files}")

# 查找以'test'开头的文件
test_files = list(Path('.').glob('test*.py'))
print(f"测试文件: {test_files}")

# 查找包含数字的文件
numeric_files = list(Path('.').glob('*[0-9]*.py'))
print(f"包含数字的文件: {numeric_files}")

# 递归查找所有Python文件
all_py_files = list(Path('.').rglob('*.py'))
print(f"所有Python文件: {all_py_files}")
```

### 4.2 高级模式
**示例**：
```python
from pathlib import Path

# 使用多种模式
patterns = ['*.py', '*.txt', '*.md']
for pattern in patterns:
    files = list(Path('.').glob(pattern))
    print(f"{pattern}: {files}")

# 组合模式
# 查找所有.py文件，排除test_开头的
all_py = set(Path('.').rglob('*.py'))
test_py = set(Path('.').rglob('test_*.py'))
non_test_py = all_py - test_py
print(f"非测试Python文件: {non_test_py}")
```

## 5. os模块
### 5.1 文件操作
**函数**：
- `os.rename()`：重命名
- `os.remove()`：删除文件
- `os.makedirs()`：创建目录
- `os.rmdir()`：删除目录

**示例**：
```python
import os

# 创建目录
os.makedirs('new_dir/subdir', exist_ok=True)

# 重命名
if os.path.exists('old_name.txt'):
    os.rename('old_name.txt', 'new_name.txt')

# 删除文件
if os.path.exists('temp.txt'):
    os.remove('temp.txt')

# 删除目录
if os.path.exists('empty_dir'):
    os.rmdir('empty_dir')
```

### 5.2 环境变量
**函数**：
- `os.getenv()`：获取环境变量
- `os.environ`：环境变量字典

**示例**：
```python
import os

# 获取环境变量
home_dir = os.getenv('HOME') or os.getenv('USERPROFILE')
print(f"主目录: {home_dir}")

# 获取所有环境变量
print("\n环境变量:")
for key, value in sorted(os.environ.items()):
    if 'PATH' in key.upper():
        print(f"  {key}: {value[:50]}...")
```

## 6. shutil高级操作
### 6.1 文件复制
**函数**：
- `shutil.copy()`：复制文件
- `shutil.copy2()`：复制文件（保留元数据）
- `shutil.copytree()`：复制目录树

**示例**：
```python
import shutil
from pathlib import Path

# 复制文件
src = Path('source.txt')
dst = Path('destination.txt')
if src.exists():
    shutil.copy2(src, dst)  # 保留元数据

# 复制目录
src_dir = Path('source_dir')
dst_dir = Path('destination_dir')
if src_dir.exists():
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
```

### 6.2 文件移动和删除
**函数**：
- `shutil.move()`：移动文件/目录
- `shutil.rmtree()`：删除目录树

**示例**：
```python
import shutil
from pathlib import Path

# 移动文件
src = Path('file_to_move.txt')
dst = Path('destination/file_moved.txt')
if src.exists():
    shutil.move(str(src), str(dst))

# 删除目录树（危险操作）
dir_to_delete = Path('dir_to_delete')
if dir_to_delete.exists():
    shutil.rmtree(dir_to_delete)
```

## 7. 文件元数据
### 7.1 获取文件信息
**属性**：
- `stat()`：获取文件状态
- `st_size`：文件大小
- `st_mtime`：修改时间
- `st_ctime`：创建时间

**示例**：
```python
from pathlib import Path
import time

file_path = Path('example.txt')
if file_path.exists():
    stat = file_path.stat()
    
    print(f"文件大小: {stat.st_size} 字节")
    print(f"修改时间: {time.ctime(stat.st_mtime)}")
    print(f"创建时间: {time.ctime(stat.st_ctime)}")
```

## 8. 实际应用：智能文件管理器
```python
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class SmartFileManager:
    """智能文件管理器"""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def organize_by_extension(self, target_dir=None):
        """按扩展名整理文件"""
        if target_dir is None:
            target_dir = self.base_dir
        
        target_dir = Path(target_dir)
        
        # 按扩展名分组
        ext_groups = defaultdict(list)
        for file in target_dir.iterdir():
            if file.is_file():
                ext = file.suffix.lower() or '无扩展名'
                ext_groups[ext].append(file)
        
        # 创建目录并移动文件
        for ext, files in ext_groups.items():
            ext_dir = target_dir / ext.lstrip('.')
            ext_dir.mkdir(exist_ok=True)
            
            for file in files:
                dst = ext_dir / file.name
                if not dst.exists():
                    shutil.move(str(file), str(dst))
                    print(f"移动: {file.name} -> {ext}/")
    
    def find_duplicates(self, target_dir=None):
        """查找重复文件"""
        if target_dir is None:
            target_dir = self.base_dir
        
        target_dir = Path(target_dir)
        
        # 按大小分组
        size_groups = defaultdict(list)
        for file in target_dir.rglob('*'):
            if file.is_file():
                size_groups[file.stat().st_size].append(file)
        
        # 查找相同大小的文件
        duplicates = []
        for size, files in size_groups.items():
            if len(files) > 1:
                # 进一步比较内容
                content_groups = defaultdict(list)
                for file in files:
                    try:
                        content = file.read_bytes()
                        content_groups[content].append(file)
                    except:
                        pass
                
                for content, group in content_groups.items():
                    if len(group) > 1:
                        duplicates.append(group)
        
        return duplicates
    
    def clean_old_files(self, days=30, target_dir=None):
        """清理旧文件"""
        if target_dir is None:
            target_dir = self.base_dir
        
        target_dir = Path(target_dir)
        cutoff_time = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_time.timestamp()
        
        cleaned = []
        for file in target_dir.rglob('*'):
            if file.is_file() and file.stat().st_mtime < cutoff_timestamp:
                cleaned.append(file)
                # 这里可以选择删除或移动到回收站
                # file.unlink()
        
        return cleaned
    
    def generate_report(self):
        """生成目录报告"""
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': defaultdict(int),
            'by_date': defaultdict(int)
        }
        
        for item in self.base_dir.rglob('*'):
            if item.is_file():
                stats['total_files'] += 1
                stats['total_size'] += item.stat().st_size
                stats['by_extension'][item.suffix.lower() or '无扩展名'] += 1
                
                # 按日期统计
                date = datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d')
                stats['by_date'][date] += 1
            elif item.is_dir():
                stats['total_dirs'] += 1
        
        return stats

# 使用示例
if __name__ == "__main__":
    # 创建测试目录
    test_dir = Path('test_file_manager')
    test_dir.mkdir(exist_ok=True)
    
    # 创建测试文件
    for i in range(5):
        (test_dir / f'test_{i}.txt').write_text(f'测试内容 {i}')
        (test_dir / f'data_{i}.json').write_text(f'{{"id": {i}}}')
    
    # 使用文件管理器
    manager = SmartFileManager(test_dir)
    
    # 生成报告
    report = manager.generate_report()
    print("目录报告:")
    print(f"  总文件数: {report['total_files']}")
    print(f"  总目录数: {report['total_dirs']}")
    print(f"  总大小: {report['total_size']} 字节")
    
    # 按扩展名整理
    print("\n按扩展名整理:")
    manager.organize_by_extension()
    
    # 清理测试目录
    shutil.rmtree(test_dir)
```

## 9. 常见错误与调试
1. **路径不存在**：先检查`exists()`
2. **权限错误**：检查文件权限
3. **跨平台路径**：使用pathlib自动处理
4. **编码问题**：指定正确的编码
5. **大文件处理**：考虑内存使用

## 10. 动手练习
1. 实现文件搜索工具
2. 创建目录同步工具
3. 实现文件备份系统
4. 创建文件清理工具
5. 实现文件统计分析

---
**提示**：pathlib是现代Python的推荐方式，比os模块更易用！
