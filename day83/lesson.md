# Day 83: 代码执行沙箱

## 1. 什么是代码执行沙箱？

代码执行沙箱是一个**隔离的安全环境**，用于运行不受信任的代码。在Agent系统中，沙箱用于执行用户提交的代码、插件代码、或外部工具返回的脚本。

### 核心安全问题
- **代码注入**：用户代码可能执行恶意操作
- **资源耗尽**：死循环或大量内存分配导致服务崩溃
- **数据泄露**：读取系统敏感文件或环境变量
- **网络攻击**：利用服务器作为跳板发起攻击
- **逃逸攻击**：突破沙箱边界访问宿主系统

### 沙箱层级
```
┌─────────────────────────┐
│     应用层沙箱           │  Python exec() + 内置函数过滤
├─────────────────────────┤
│     进程层沙箱           │  subprocess + 资源限制(ulimit)
├─────────────────────────┤
│     容器层沙箱           │  Docker + namespace + cgroup
├─────────────────────────┤
│     虚拟机层沙箱         │  gVisor / Firecracker
├─────────────────────────┤
│     硬件层隔离           │  Intel SGX / ARM TrustZone
└─────────────────────────┘
```

## 2. 基于subprocess的安全执行

### 基础subprocess封装
```python
import subprocess
import os
import signal
import resource
from typing import Optional, Tuple


class SafeExecutor:
    """安全的子进程执行器"""

    def __init__(self, timeout: int = 5, max_memory_mb: int = 128):
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb

    def run(self, code: str, language: str = "python") -> Tuple[str, str, int]:
        """
        安全执行代码
        返回: (stdout, stderr, return_code)
        """
        # 根据语言选择解释器
        interpreters = {
            "python": ["python3", "-c"],
            "bash": ["bash", "-c"],
        }
        cmd = interpreters.get(language)
        if not cmd:
            raise ValueError(f"不支持的语言: {language}")

        try:
            result = subprocess.run(
                cmd + [code],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                # 安全的环境变量
                env={
                    "PATH": "/usr/bin:/bin",
                    "HOME": "/tmp",
                    "LANG": "en_US.UTF-8",
                },
                # 限制工作目录
                cwd="/tmp",
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "执行超时", -1

    def run_file(self, filepath: str, args: list = None) -> Tuple[str, str, int]:
        """执行脚本文件"""
        cmd = ["python3", filepath] + (args or [])
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "执行超时", -1
```

### 带资源限制的执行
```python
import resource


def set_limits(max_cpu_time: int = 5, max_memory_mb: int = 128):
    """在子进程中设置资源限制（需在预执行函数中调用）"""
    # CPU时间限制（秒）
    resource.setrlimit(resource.RLIMIT_CPU, (max_cpu_time, max_cpu_time))

    # 内存限制（字节）
    max_bytes = max_memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes))

    # 文件大小限制
    resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))

    # 进程数限制
    resource.setrlimit(resource.RLIMIT_NPROC, (50, 50))


# 使用
result = subprocess.run(
    ["python3", "-c", code],
    preexec_fn=set_limits,  # Linux only
    timeout=10,
)
```

## 3. 受限exec() — Python沙箱

### 过滤内置函数
```python
import builtins

# 保存原始builtins
_original_builtins = vars(builtins).copy()

# 危险函数列表
DANGEROUS_BUILTINS = {
    "exec", "eval", "compile", "__import__",
    "open", "input", "breakpoint",
    "exit", "quit",
}

# 危险模块
DANGEROUS_MODULES = {
    "os", "sys", "subprocess", "shutil",
    "socket", "http", "urllib", "requests",
    "ctypes", "importlib", "pathlib",
}


def create_sandbox_globals(allowed_modules: list = None):
    """创建沙箱化的全局命名空间"""
    safe_globals = {
        "__builtins__": {
            name: getattr(builtins, name)
            for name in dir(builtins)
            if not name.startswith("_")
            and name not in DANGEROUS_BUILTINS
        }
    }

    # 只允许安全模块
    if allowed_modules:
        for mod_name in allowed_modules:
            try:
                safe_globals[mod_name] = __import__(mod_name)
            except ImportError:
                pass

    return safe_globals


def safe_exec(code: str, timeout: int = 5):
    """安全exec执行"""
    safe_globals = create_sandbox_globals(
        allowed_modules=["math", "json", "datetime", "re"]
    )
    safe_locals = {}

    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError("代码执行超时")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        exec(code, safe_globals, safe_locals)
        return safe_locals
    except TimeoutError:
        raise
    finally:
        signal.alarm(0)  # 取消定时器
```

### AST级别的安全检查
```python
import ast


class SecurityChecker(ast.NodeVisitor):
    """AST安全检查器"""

    DANGEROUS_CALLS = {
        "exec", "eval", "compile", "__import__",
        "open", "getattr", "setattr", "delattr",
    }

    DANGEROUS_MODULES = {
        "os", "sys", "subprocess", "shutil",
        "socket", "ctypes", "importlib",
    }

    def __init__(self):
        self.violations = []

    def check(self, code: str) -> bool:
        """检查代码是否安全，返回True表示安全"""
        try:
            tree = ast.parse(code)
            self.visit(tree)
        except SyntaxError as e:
            self.violations.append(f"语法错误: {e}")

        return len(self.violations) == 0

    def visit_Call(self, node):
        """检查函数调用"""
        if isinstance(node.func, ast.Name):
            if node.func.id in self.DANGEROUS_CALLS:
                self.violations.append(
                    f"禁止调用: {node.func.id} (行 {node.lineno})"
                )
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ("system", "popen", "spawn", "kill"):
                self.violations.append(
                    f"禁止调用: {node.func.attr} (行 {node.lineno})"
                )
        self.generic_visit(node)

    def visit_Import(self, node):
        """检查import语句"""
        for alias in node.names:
            mod = alias.name.split(".")[0]
            if mod in self.DANGEROUS_MODULES:
                self.violations.append(
                    f"禁止导入: {alias.name} (行 {node.lineno})"
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """检查from import语句"""
        if node.module:
            mod = node.module.split(".")[0]
            if mod in self.DANGEROUS_MODULES:
                self.violations.append(
                    f"禁止导入: {node.module} (行 {node.lineno})"
                )
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """检查危险属性访问"""
        if isinstance(node.value, ast.Name) and node.value.id == "__builtins__":
            self.violations.append(
                f"禁止访问__builtins__ (行 {node.lineno})"
            )
        self.generic_visit(node)
```

## 4. 文件系统隔离

### 虚拟文件系统
```python
import os
import io
import tempfile
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class VirtualFile:
    """虚拟文件"""
    name: str
    content: bytes = b""
    is_dir: bool = False
    children: Dict[str, "VirtualFile"] = field(default_factory=dict)


class VirtualFileSystem:
    """内存虚拟文件系统"""

    def __init__(self):
        self.root = VirtualFile("/", is_dir=True)
        self.cwd = "/"
        self.open_files: Dict[int, io.BytesIO] = {}
        self._next_fd = 0

    def resolve_path(self, path: str) -> str:
        """解析路径"""
        if not path.startswith("/"):
            path = os.path.join(self.cwd, path)
        # 规范化
        parts = [p for p in path.split("/") if p]
        resolved = []
        for part in parts:
            if part == "..":
                if resolved:
                    resolved.pop()
            elif part != ".":
                resolved.append(part)
        return "/" + "/".join(resolved)

    def get_node(self, path: str) -> Optional[VirtualFile]:
        """获取路径对应的节点"""
        path = self.resolve_path(path)
        if path == "/":
            return self.root

        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node

    def makedirs(self, path: str):
        """创建目录"""
        path = self.resolve_path(path)
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = VirtualFile(part, is_dir=True)
            node = node.children[part]
            if not node.is_dir:
                raise IsADirectoryError(f"不是目录: {path}")

    def write_file(self, path: str, content: bytes):
        """写入文件"""
        path = self.resolve_path(path)
        parent_path = "/".join(path.split("/")[:-1]) or "/"
        filename = path.split("/")[-1]

        parent = self.get_node(parent_path)
        if parent is None or not parent.is_dir:
            raise FileNotFoundError(f"目录不存在: {parent_path}")

        parent.children[filename] = VirtualFile(filename, content=content)

    def read_file(self, path: str) -> bytes:
        """读取文件"""
        node = self.get_node(path)
        if node is None:
            raise FileNotFoundError(f"文件不存在: {path}")
        if node.is_dir:
            raise IsADirectoryError(f"是目录: {path}")
        return node.content
```

### 目录Chroot隔离
```python
import tempfile
import os
from pathlib import Path


class ChrootSandbox:
    """Chroot沙箱 - 限制文件系统访问范围"""

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or tempfile.mkdtemp(prefix="sandbox_")
        self.setup_chroot()

    def setup_chroot(self):
        """设置chroot环境"""
        # 创建基本目录结构
        dirs = ["bin", "lib", "usr", "tmp", "workspace"]
        for d in dirs:
            os.makedirs(os.path.join(self.base_dir, d), exist_ok=True)

        # 创建最小化的环境
        # 复制必要的系统文件
        self._copy_if_exists("/bin/sh", "bin/sh")
        self._copy_if_exists("/usr/bin/python3", "usr/bin/python3")

    def _copy_if_exists(self, src: str, dst: str):
        """复制文件到沙箱"""
        import shutil
        src_path = os.path.join(self.base_dir, src.lstrip("/"))
        os.makedirs(os.path.dirname(src_path), exist_ok=True)
        if os.path.exists(src):
            try:
                shutil.copy2(src, src_path)
            except (PermissionError, OSError):
                pass

    def get_chroot_cmd(self, cmd: list) -> list:
        """生成chroot命令"""
        return ["chroot", self.base_dir] + cmd
```

## 5. 网络访问控制

### 网络隔离
```python
import socket
from typing import List, Set
from dataclasses import dataclass


@dataclass
class NetworkPolicy:
    """网络访问策略"""
    allow_outbound: bool = False
    allowed_hosts: Set[str] = None
    allowed_ports: Set[int] = None
    blocked_hosts: Set[str] = None
    blocked_ports: Set[int] = None

    def __post_init__(self):
        self.allowed_hosts = self.allowed_hosts or set()
        self.allowed_ports = self.allowed_ports or set()
        self.blocked_hosts = self.blocked_hosts or set()
        self.blocked_ports = self.blocked_ports or set()

    def is_allowed(self, host: str, port: int) -> bool:
        """检查是否允许访问"""
        if not self.allow_outbound:
            return False
        if host in self.blocked_hosts:
            return False
        if port in self.blocked_ports:
            return False
        if self.allowed_hosts and host not in self.allowed_hosts:
            return False
        if self.allowed_ports and port not in self.allowed_ports:
            return False
        return True


class NetworkFilter:
    """网络访问过滤器"""

    def __init__(self, policy: NetworkPolicy = None):
        self.policy = policy or NetworkPolicy()
        self._original_socket = socket.socket
        self._blocked_connections = []

    def install(self):
        """安装网络过滤（替换socket）"""
        original_connect = self._original_socket.connect

        def filtered_connect(self_socket, address):
            host, port = address
            if not self.policy.is_allowed(host, port):
                self._blocked_connections.append((host, port))
                raise PermissionError(
                    f"网络访问被拒绝: {host}:{port}"
                )
            return original_connect(self_socket, address)

        socket.socket.connect = filtered_connect

    def uninstall(self):
        """卸载网络过滤"""
        socket.socket.connect = self._original_socket.connect

    def get_blocked(self) -> List[tuple]:
        """获取被阻止的连接列表"""
        return self._blocked_connections.copy()
```

## 6. 资源限制

### CPU/内存/时间限制
```python
import resource
import signal
import threading
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResourceLimits:
    """资源限制配置"""
    max_cpu_time: int = 5          # CPU时间（秒）
    max_wall_time: int = 10        # 挂钟时间（秒）
    max_memory_mb: int = 128       # 内存（MB）
    max_output_bytes: int = 1024*1024  # 输出大小（1MB）
    max_file_size_mb: int = 10     # 文件大小（MB）
    max_processes: int = 50        # 最大进程数


class ResourceLimiter:
    """资源限制器"""

    def __init__(self, limits: ResourceLimits = None):
        self.limits = limits or ResourceLimits()

    def apply_in_child(self):
        """在子进程中应用限制（作为preexec_fn）"""
        # CPU时间
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (self.limits.max_cpu_time, self.limits.max_cpu_time)
        )

        # 内存
        max_bytes = self.limits.max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes))

        # 文件大小
        file_bytes = self.limits.max_file_size_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (file_bytes, file_bytes))

        # 进程数
        resource.setrlimit(
            resource.RLIMIT_NPROC,
            (self.limits.max_processes, self.limits.max_processes)
        )

        # 禁止core dump
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

    def monitor_wall_time(self, proc, callback=None):
        """监控挂钟时间"""
        def _timeout():
            if proc.poll() is None:
                proc.kill()
                if callback:
                    callback("超时终止")

        timer = threading.Timer(self.limits.max_wall_time, _timeout)
        timer.start()
        return timer
```

## 7. 超时控制

### 多种超时策略
```python
import signal
import threading
from enum import Enum, auto
from typing import Callable, Optional
from contextlib import contextmanager


class TimeoutStrategy(Enum):
    """超时策略"""
    SIGNAL = auto()     # 信号方式（仅主线程）
    THREAD = auto()     # 线程方式
    PROCESS = auto()    # 子进程方式


class TimeoutController:
    """超时控制器"""

    @staticmethod
    @contextmanager
    def signal_timeout(seconds: int):
        """基于信号的超时（仅主线程可用）"""
        def handler(signum, frame):
            raise TimeoutError(f"执行超时 ({seconds}秒)")

        old_handler = signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

    @staticmethod
    @contextmanager
    def thread_timeout(seconds: int):
        """基于线程的超时"""
        timer = None
        exception_holder = []

        def raise_timeout():
            exception_holder.append(
                TimeoutError(f"执行超时 ({seconds}秒)")
            )

        timer = threading.Timer(seconds, raise_timeout)
        timer.start()
        try:
            yield
        finally:
            timer.cancel()
            if exception_holder:
                raise exception_holder[0]

    @staticmethod
    def with_timeout(func: Callable, args: tuple = (), kwargs: dict = None,
                     timeout: int = 5, strategy: TimeoutStrategy = None):
        """带超时的函数执行"""
        kwargs = kwargs or {}

        if strategy == TimeoutStrategy.THREAD:
            result = [None]
            error = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    error[0] = e

            t = threading.Thread(target=target)
            t.start()
            t.join(timeout)

            if t.is_alive():
                raise TimeoutError(f"执行超时 ({timeout}秒)")
            if error[0]:
                raise error[0]
            return result[0]
        else:
            # 默认使用信号方式
            with TimeoutController.signal_timeout(timeout):
                return func(*args, **kwargs)
```

## 8. 完整沙箱系统

### 组合所有组件
```python
import subprocess
import tempfile
import shutil
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class ExecutionResult:
    """执行结果"""
    stdout: str = ""
    stderr: str = ""
    return_code: int = -1
    timed_out: bool = False
    resource_exceeded: str = ""
    execution_time: float = 0.0
    security_violations: list = field(default_factory=list)


class CodeSandbox:
    """完整的代码执行沙箱"""

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.timeout = config.get("timeout", 5)
        self.max_memory_mb = config.get("max_memory_mb", 128)
        self.max_output_bytes = config.get("max_output_bytes", 1024*1024)
        self.allowed_modules = config.get("allowed_modules", ["math", "json"])
        self.temp_dir = tempfile.mkdtemp(prefix="sandbox_")

    def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """执行代码"""
        result = ExecutionResult()

        # 安全检查
        if language == "python":
            checker = SecurityChecker()
            if not checker.check(code):
                result.security_violations = checker.violations
                result.stderr = "安全检查失败:\n" + "\n".join(checker.violations)
                result.return_code = -2
                return result

        # 写入临时文件
        suffix = ".py" if language == "python" else ".sh"
        code_file = os.path.join(self.temp_dir, f"code{suffix}")
        with open(code_file, "w") as f:
            f.write(code)

        # 执行
        start_time = datetime.now()
        try:
            cmd = ["python3", code_file] if language == "python" else ["bash", code_file]
            result_obj = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.temp_dir,
                env={"PATH": "/usr/bin:/bin", "HOME": self.temp_dir},
            )
            result.stdout = result_obj.stdout[:self.max_output_bytes]
            result.stderr = result_obj.stderr[:self.max_output_bytes]
            result.return_code = result_obj.returncode
        except subprocess.TimeoutExpired:
            result.timed_out = True
            result.stderr = "执行超时"
            result.return_code = -1
        except Exception as e:
            result.stderr = str(e)
            result.return_code = -3

        result.execution_time = (datetime.now() - start_time).total_seconds()
        return result

    def cleanup(self):
        """清理临时目录"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
```

## 9. 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `TimeoutError` | 代码执行超时 | 增加timeout或优化代码 |
| `PermissionError` | 权限不足 | 检查沙箱权限配置 |
| `OSError: [Errno 12]` | 内存不足 | 增加max_memory_mb |
| `SyntaxError` | 代码语法错误 | 检查输入代码 |
| `SecurityError` | 安全检查失败 | 检查代码是否包含危险操作 |

## 10. 应用场景

1. **在线代码编辑器**：LeetCode/Codeforces式的在线评测
2. **Agent工具执行**：安全执行AI生成的代码
3. **插件系统**：安全运行第三方插件
4. **教学平台**：学生代码的安全执行
5. **CI/CD**：构建和测试的隔离环境

## 11. 练习

1. 实现一个支持Python/Bash/JS的多语言沙箱
2. 实现内存中的虚拟文件系统，支持基本的文件操作
3. 实现网络访问白名单，只允许访问指定API
4. 实现AST级别的安全检查，覆盖所有危险操作
5. 组合所有组件，构建完整的沙箱系统
