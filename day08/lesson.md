# Day 8 完整教学：文件 I/O

## 1. 文件操作基础
### 1.1 打开文件模式
**说明**：open()函数用于打开文件，返回文件对象。模式参数决定操作类型。

**语法**：
```python
file = open(filename, mode, encoding='utf-8')
```

**模式说明**：
- `'r'`：只读（默认）
- `'w'`：写入（覆盖）
- `'a'`：追加
- `'x'`：创建（文件已存在则报错）
- `'b'`：二进制模式
- `'t'`：文本模式（默认）
- `'+'`：读写模式

**示例**：
```python
# 文本文件读写
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
file.close()

# 二进制文件
with open('image.jpg', 'rb') as f:
    data = f.read()
```

**常见错误**：
- 忘记关闭文件（使用with语句）
- 编码不匹配导致乱码
- 文件不存在时使用'r'模式

### 1.2 with语句
**说明**：上下文管理器，自动关闭文件，推荐使用。

**语法**：
```python
with open('file.txt', 'r') as f:
    content = f.read()
# 自动关闭文件
```

**示例**：
```python
# 读取文件
with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 写入文件
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, World!')
```

**优势**：
- 自动关闭文件
- 异常安全
- 代码更简洁

## 2. 文件读取方法
### 2.1 read()方法
**说明**：读取整个文件内容为字符串。

**语法**：
```python
content = file.read()  # 读取全部
content = file.read(n)  # 读取n个字符
```

**示例**：
```python
with open('example.txt', 'r', encoding='utf-8') as f:
    # 读取全部内容
    full_content = f.read()
    
    # 读取前100个字符
    partial = f.read(100)
```

**注意**：大文件慎用，会一次性加载到内存。

### 2.2 readline()方法
**说明**：逐行读取，适合大文件处理。

**语法**：
```python
line = file.readline()  # 读取一行
```

**示例**：
```python
with open('large_file.txt', 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        process(line)
        line = f.readline()
```

### 2.3 readlines()方法
**说明**：读取所有行，返回列表。

**语法**：
```python
lines = file.readlines()  # 返回行列表
```

**示例**：
```python
with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())
```

## 3. 文件写入方法
### 3.1 write()方法
**说明**：写入字符串到文件。

**语法**：
```python
file.write(string)  # 返回写入的字符数
```

**示例**：
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('第一行\n')
    f.write('第二行\n')
```

### 3.2 writelines()方法
**说明**：写入字符串列表。

**语法**：
```python
file.writelines(lines)  # lines是字符串列表
```

**示例**：
```python
lines = ['第一行\n', '第二行\n', '第三行\n']
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
```

**注意**：不会自动添加换行符。

## 4. 编码处理
### 4.1 常见编码
- `'utf-8'`：通用编码，推荐使用
- `'gbk'`：中文Windows默认编码
- `'latin-1'`：西欧字符
- `'ascii'`：仅ASCII字符

### 4.2 编码转换
**示例**：
```python
# 读取GBK编码文件
with open('gbk_file.txt', 'r', encoding='gbk') as f:
    content = f.read()

# 转换为UTF-8保存
with open('utf8_file.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

### 4.3 处理编码错误
**示例**：
```python
# 忽略错误
with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 替换错误字符
with open('file.txt', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
```

## 5. 大文件处理
### 5.1 逐行处理
**示例**：
```python
def process_large_file(filename):
    """处理大文件，逐行读取"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:  # 文件对象可迭代
            process(line.strip())
```

### 5.2 分块读取
**示例**：
```python
def read_in_chunks(file_path, chunk_size=1024):
    """分块读取文件"""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
```

### 5.3 内存映射
**示例**：
```python
import mmap

def search_in_file(filename, pattern):
    """使用内存映射搜索大文件"""
    with open(filename, 'r+b') as f:
        # 内存映射文件
        mm = mmap.mmap(f.fileno(), 0)
        # 搜索模式
        index = mm.find(pattern.encode())
        mm.close()
        return index
```

## 6. 临时文件
### 6.1 tempfile模块
**示例**：
```python
import tempfile

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write('临时数据')
    temp_name = f.name

# 使用临时文件
with open(temp_name, 'r') as f:
    content = f.read()

# 清理
import os
os.unlink(temp_name)
```

### 6.2 临时目录
**示例**：
```python
import tempfile
import shutil

# 创建临时目录
with tempfile.TemporaryDirectory() as temp_dir:
    # 在临时目录中创建文件
    file_path = os.path.join(temp_dir, 'temp.txt')
    with open(file_path, 'w') as f:
        f.write('临时数据')
    
    # 处理文件
    # ...

# 临时目录自动删除
```

## 7. CSV文件基础
### 7.1 csv模块
**示例**：
```python
import csv

# 写入CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['姓名', '年龄', '城市'])
    writer.writerow(['张三', 25, '北京'])
    writer.writerow(['李四', 30, '上海'])

# 读取CSV
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

### 7.2 字典CSV
**示例**：
```python
import csv

# 写入字典CSV
with open('people.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'name': '张三', 'age': 25, 'city': '北京'})

# 读取字典CSV
with open('people.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']}, {row['age']}岁, 来自{row['city']}")
```

## 8. 实际应用：日志分析器
```python
import re
from collections import Counter
from datetime import datetime

class LogAnalyzer:
    """日志文件分析器"""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []
    
    def parse_log_line(self, line):
        """解析日志行"""
        # 示例格式: 2024-01-15 10:30:00 [ERROR] Something went wrong
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)'
        match = re.match(pattern, line.strip())
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        return None
    
    def load_logs(self):
        """加载日志文件"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    log = self.parse_log_line(line)
                    if log:
                        self.logs.append(log)
            return True
        except Exception as e:
            print(f"加载日志失败: {e}")
            return False
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.logs:
            return None
        
        # 按级别统计
        level_count = Counter(log['level'] for log in self.logs)
        
        # 按日期统计
        date_count = Counter(log['timestamp'].split()[0] for log in self.logs)
        
        return {
            'total': len(self.logs),
            'by_level': dict(level_count),
            'by_date': dict(date_count)
        }
    
    def search_logs(self, keyword):
        """搜索日志"""
        return [log for log in self.logs if keyword in log['message']]
    
    def export_report(self, output_file):
        """导出分析报告"""
        stats = self.get_statistics()
        if not stats:
            return False
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("日志分析报告\n")
                f.write("=" * 50 + "\n")
                f.write(f"总记录数: {stats['total']}\n\n")
                
                f.write("按级别统计:\n")
                for level, count in stats['by_level'].items():
                    f.write(f"  {level}: {count}\n")
                
                f.write("\n按日期统计:\n")
                for date, count in stats['by_date'].items():
                    f.write(f"  {date}: {count}\n")
            
            return True
        except Exception as e:
            print(f"导出报告失败: {e}")
            return False

# 使用示例
if __name__ == "__main__":
    # 创建测试日志
    test_log = "test.log"
    with open(test_log, 'w', encoding='utf-8') as f:
        f.write("2024-01-15 10:30:00 [INFO] Application started\n")
        f.write("2024-01-15 10:30:05 [ERROR] Connection failed\n")
        f.write("2024-01-15 10:31:00 [INFO] Retrying connection\n")
        f.write("2024-01-15 10:31:05 [INFO] Connection established\n")
    
    # 分析日志
    analyzer = LogAnalyzer(test_log)
    if analyzer.load_logs():
        stats = analyzer.get_statistics()
        print(f"总记录数: {stats['total']}")
        print(f"按级别统计: {stats['by_level']}")
        
        # 搜索错误日志
        errors = analyzer.search_logs("ERROR")
        print(f"错误日志: {len(errors)}条")
        
        # 导出报告
        analyzer.export_report("log_report.txt")
    
    # 清理
    import os
    os.unlink(test_log)
    if os.path.exists("log_report.txt"):
        os.unlink("log_report.txt")
```

## 9. 常见错误与调试
1. **文件未找到**：检查路径，使用绝对路径或确认当前目录
2. **编码错误**：指定正确的编码，使用errors参数处理
3. **权限错误**：检查文件权限，确保有读写权限
4. **文件被占用**：确保文件未被其他程序打开
5. **内存不足**：大文件使用逐行读取

## 10. 动手练习
1. 实现一个文件复制工具
2. 创建日志轮转程序
3. 实现配置文件解析器
4. 创建CSV数据处理工具
5. 实现文件搜索工具

---
**提示**：文件操作是数据处理的基础，务必掌握！
