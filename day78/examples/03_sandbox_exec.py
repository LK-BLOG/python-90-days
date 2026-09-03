# Day 78 示例 3: 代码沙箱
import io, traceback
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data = None
    error: str = ""

class CodeSandbox:
    name = "code_exec"
    description = "安全执行 Python 代码"
    BLOCKED = ["import os", "import subprocess", "import sys", "__import__", "open("]
    
    def execute(self, code: str) -> ToolResult:
        for b in self.BLOCKED:
            if b in code:
                return ToolResult(False, error=f"禁止: {b}")
        
        stdout = io.StringIO()
        stderr = io.StringIO()
        safe_builtins = {"print": print, "len": len, "range": range, "int": int, "float": float, "str": str, "list": list, "dict": dict, "min": min, "max": max, "sum": sum, "sorted": sorted, "enumerate": enumerate, "zip": zip, "abs": abs, "round": round}
        
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, {"__builtins__": safe_builtins}, {})
            return ToolResult(True, data={"output": stdout.getvalue(), "errors": stderr.getvalue()})
        except Exception as e:
            return ToolResult(False, error=f"{type(e).__name__}: {e}")

if __name__ == "__main__":
    sandbox = CodeSandbox()
    print(sandbox.execute("print(sum(range(10)))"))
    print(sandbox.execute("import os; os.system('ls')"))
