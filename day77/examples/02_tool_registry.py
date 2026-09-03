# Day 77 示例 2: ToolRegistry
\"\"\"
工具注册表的完整实现
\"\"\"
from typing import Dict, List, Optional


class ToolRegistry:
    \"\"\"工具注册表\"\"\"
    
    def __init__(self):
        self._tools: Dict[str, 'BaseTool'] = {}
        self._categories: Dict[str, List[str]] = {}
        self._call_log: List[dict] = []
    
    def register(self, tool: 'BaseTool', category: str = None) -> None:
        cat = category or tool.category
        if tool.name in self._tools:
            raise ValueError(f"工具 '{tool.name}' 已注册")
        
        self._tools[tool.name] = tool
        self._categories.setdefault(cat, []).append(tool.name)
        print(f"  ✅ 注册: {tool.name} [{cat}]")
    
    def unregister(self, name: str) -> bool:
        if name not in self._tools:
            return False
        tool = self._tools.pop(name)
        cat_tools = self._categories.get(tool.category, [])
        if name in cat_tools:
            cat_tools.remove(name)
        return True
    
    def get(self, name: str) -> Optional['BaseTool']:
        return self._tools.get(name)
    
    def list_all(self) -> List[str]:
        return list(self._tools.keys())
    
    def list_by_category(self, category: str) -> List[str]:
        return self._categories.get(category, [])
    
    def get_schemas(self, categories: List[str] = None) -> List[dict]:
        \"\"\"获取工具描述（给 LLM）\"\"\"
        tools = self._tools.values()
        if categories:
            names = set()
            for cat in categories:
                names.update(self._categories.get(cat, []))
            tools = [self._tools[n] for n in names if n in self._tools]
        return [t.to_dict() for t in tools]
    
    def execute(self, name: str, **kwargs) -> 'ToolResult':
        tool = self.get(name)
        if not tool:
            from day77_examples_01 import ToolResult
            return ToolResult(success=False, error=f"工具 '{name}' 不存在")
        
        result = tool.run(**kwargs)
        
        # 记录调用日志
        self._call_log.append({
            "tool": name,
            "params": kwargs,
            "success": result.success,
        })
        
        return result
    
    def get_call_stats(self) -> dict:
        \"\"\"获取调用统计\"\"\"
        total = len(self._call_log)
        success = sum(1 for c in self._call_log if c["success"])
        by_tool = {}
        for c in self._call_log:
            by_tool.setdefault(c["tool"], 0)
            by_tool[c["tool"]] += 1
        
        return {
            "total_calls": total,
            "success_rate": f"{success/total*100:.1f}%" if total else "N/A",
            "calls_by_tool": by_tool
        }


# 演示
if __name__ == "__main__":
    from abc import ABC, abstractmethod
    from typing import Any
    from dataclasses import dataclass
    
    # 简化版 ToolResult 和 BaseTool
    @dataclass
    class ToolResult:
        success: bool
        data: Any = None
        error: str = ""
    
    class BaseTool(ABC):
        name: str = ""
        description: str = ""
        category: str = "general"
        
        def run(self, **kwargs) -> ToolResult:
            try:
                result = self.execute(**kwargs)
                return ToolResult(success=True, data=result)
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        @abstractmethod
        def execute(self, **kwargs): pass
    
    class CalcTool(BaseTool):
        name = "calc"
        description = "计算"
        category = "math"
        def execute(self, expression=""): return eval(expression)
    
    class SearchTool(BaseTool):
        name = "search"
        description = "搜索"
        category = "web"
        def execute(self, query=""): return f"搜索结果: {query}"
    
    # 使用注册表
    registry = ToolRegistry()
    registry.register(CalcTool())
    registry.register(SearchTool())
    
    print("\n所有工具:", registry.list_all())
    print("分类搜索:", registry.list_by_category("math"))
    
    result = registry.execute("calc", expression="2**10")
    print(f"\n执行结果: {result}")
    
    print(f"\n调用统计: {registry.get_call_stats()}")
