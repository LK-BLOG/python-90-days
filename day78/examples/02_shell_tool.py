# Day 78 示例 2: Shell 执行工具
import subprocess
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data = None
    error: str = ""

class ShellTool:
    name = "shell"
    description = "执行 Shell 命令"
    BLACKLIST = ["rm -rf /", "mkfs", "dd if=", ":(){:|:&};:"]
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def _is_safe(self, cmd: str) -> tuple:
        for b in self.BLACKLIST:
            if b in cmd:
                return False, f"危险命令: {b}"
        return True, ""
    
    def execute(self, command: str) -> ToolResult:
        ok, reason = self._is_safe(command)
        if not ok:
            return ToolResult(False, error=reason)
        try:
            r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=self.timeout)
            return ToolResult(
                success=r.returncode == 0,
                data={"stdout": r.stdout, "stderr": r.stderr, "code": r.returncode},
                error=r.stderr if r.returncode != 0 else ""
            )
        except subprocess.TimeoutExpired:
            return ToolResult(False, error="命令超时")
        except Exception as e:
            return ToolResult(False, error=str(e))

if __name__ == "__main__":
    shell = ShellTool()
    print(shell.execute("echo Hello from Shell!"))
    print(shell.execute("ls -la"))
    print(shell.execute("rm -rf /"))
