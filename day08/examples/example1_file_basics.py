# 示例1：文件基础操作
# 展示文件打开模式、读写方法、with语句

def file_basics_demo():
    """文件基础操作演示"""
    
    # 1. 写入文件
    print("=== 写入文件 ===")
    with open('demo.txt', 'w', encoding='utf-8') as f:
        f.write('第一行\n')
        f.write('第二行\n')
        f.write('第三行\n')
    print("文件写入完成")
    
    # 2. 读取文件
    print("\n=== 读取文件 ===")
    with open('demo.txt', 'r', encoding='utf-8') as f:
        # 读取全部内容
        content = f.read()
        print("全部内容:")
        print(content)
    
    # 3. 逐行读取
    print("\n=== 逐行读取 ===")
    with open('demo.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            print(f"第{i}行: {line.strip()}")
    
    # 4. 读取所有行
    print("\n=== 读取所有行 ===")
    with open('demo.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"共{len(lines)}行")
        for line in lines:
            print(f"  - {line.strip()}")
    
    # 5. 追加写入
    print("\n=== 追加写入 ===")
    with open('demo.txt', 'a', encoding='utf-8') as f:
        f.write('第四行（追加）\n')
    
    # 验证追加
    with open('demo.txt', 'r', encoding='utf-8') as f:
        print("追加后的内容:")
        print(f.read())
    
    # 清理
    import os
    os.unlink('demo.txt')
    print("\n演示完成，临时文件已删除")

def binary_file_demo():
    """二进制文件操作演示"""
    
    # 1. 写入二进制数据
    print("=== 二进制文件操作 ===")
    data = bytes([72, 101, 108, 108, 111])  # "Hello"
    
    with open('binary.bin', 'wb') as f:
        f.write(data)
    print(f"写入二进制数据: {data}")
    
    # 2. 读取二进制数据
    with open('binary.bin', 'rb') as f:
        read_data = f.read()
        print(f"读取二进制数据: {read_data}")
        print(f"转换为字符串: {read_data.decode('utf-8')}")
    
    # 清理
    import os
    os.unlink('binary.bin')

if __name__ == "__main__":
    file_basics_demo()
    binary_file_demo()
