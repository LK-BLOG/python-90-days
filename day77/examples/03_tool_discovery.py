# Day 77 示例 3: 装饰器工具 + 自动发现
\"\"\"
使用装饰器注册工具，自动发现模块中的工具
\"\"\"
import os
import importlib
import inspect


# 全局注册表
_registry = {}


def register_tool(name: str, description: str, category: str = "general"):
    \"\"\"工具装饰器 - 自动注册\"\"\"
    def decorator(func):
        _registry[name] = {
            "name": name,
            "description": description,
            "category": category,
            "func": func,
            "params": inspect.signature(func).parameters,
        }
        
        def wrapper(**kwargs):
            # 参数验证
            sig = inspect.signature(func)
            bound = sig.bind(**kwargs)
            bound.apply_defaults()
            return func(**bound.arguments)
        
        wrapper.__name__ = name
        wrapper.__doc__ = description
        wrapper.tool_info = _registry[name]
        return wrapper
    
    return decorator


def discover_tools(directory: str) -> dict:
    \"\"\"扫描目录，发现所有用装饰器注册的工具\"\"\"
    found = {}
    
    for filename in os.listdir(directory):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue
        
        module_name = filename[:-3]
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(directory, filename)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 从全局注册表中找到本模块注册的工具
            # 这里简化处理，实际可以用装饰器标记
            for name, info in _registry.items():
                if name not in found:
                    found[name] = info
        except Exception as e:
            print(f"  ⚠ 加载 {filename} 失败: {e}")
    
    return found


# 注册工具
@register_tool("word_count", "统计文本中的单词数", "text")
def word_count(text: str) -> int:
    return len(text.split())


@register_tool("char_count", "统计字符数", "text")
def char_count(text: str) -> int:
    return len(text)


@register_tool("reverse_text", "反转文本", "text")
def reverse_text(text: str) -> str:
    return text[::-1]


# 演示
if __name__ == "__main__":
    print("=== 装饰器注册工具 ===\n")
    
    # 查看注册的工具
    for name, info in _registry.items():
        print(f"  工具: {name}")
        print(f"  描述: {info['description']}")
        print(f"  类别: {info['category']}")
        print(f"  参数: {list(info['params'].keys())}")
        print()
    
    # 使用工具
    print("=== 使用工具 ===\n")
    print(f"  单词数: {word_count(text='hello world foo bar')}")
    print(f"  字符数: {char_count(text='hello world')}")
    print(f"  反转: {reverse_text(text='hello world')}")
