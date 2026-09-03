# Day 87 课程：Agent 安全 & Guardrails

## 1. 输入验证与过滤

`python
from dataclasses import dataclass
from enum import Enum
from typing import Any
import re


class ThreatLevel(Enum):
    '''威胁级别'''
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"


@dataclass
class ValidationResult:
    '''验证结果'''
    is_valid: bool
    threat_level: ThreatLevel
    message: str = ""
    sanitized_input: str | None = None


class InputValidator:
    '''输入验证器'''
    
    # 已知的注入模式
    INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"ignore all previous",
        r"disregard.*instructions",
        r"you are now",
        r"new instructions:",
        r"system prompt:",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
    ]
    
    # 危险字符
    DANGEROUS_CHARS = ["<", ">", "{", "}", "[", "]", "(", ")"]
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.blocked_patterns = []
    
    def validate(self, user_input: str) -> ValidationResult:
        '''验证用户输入'''
        # 检查注入攻击
        threat = self._check_injection(user_input)
        if threat == ThreatLevel.BLOCKED:
            return ValidationResult(
                is_valid=False,
                threat_level=threat,
                message="检测到潜在的Prompt注入攻击"
            )
        
        # 检查恶意内容
        if self._check_malicious(user_input):
            return ValidationResult(
                is_valid=False,
                threat_level=ThreatLevel.DANGEROUS,
                message="输入包含潜在危险内容"
            )
        
        # 清理输入
        sanitized = self._sanitize(user_input)
        
        return ValidationResult(
            is_valid=True,
            threat_level=ThreatLevel.SAFE,
            sanitized_input=sanitized
        )
    
    def _check_injection(self, text: str) -> ThreatLevel:
        '''检查注入攻击'''
        text_lower = text.lower()
        
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                return ThreatLevel.BLOCKED
        
        # 检查异常长度
        if len(text) > 10000:
            return ThreatLevel.SUSPICIOUS
        
        return ThreatLevel.SAFE
    
    def _check_malicious(self, text: str) -> bool:
        '''检查恶意内容'''
        # 简单的启发式检查
        suspicious_count = 0
        
        # 检查base64编码
        if re.search(r'[A-Za-z0-9+/]{50,}={0,2}', text):
            suspicious_count += 1
        
        # 检查Unicode异常
        if re.search(r'[\u200b-\u200f\u2028-\u202f\ufeff]', text):
            suspicious_count += 1
        
        return suspicious_count >= 2
    
    def _sanitize(self, text: str) -> str:
        '''清理输入'''
        # 移除潜在危险字符（如果严格模式）
        if self.strict:
            for char in self.DANGEROUS_CHARS:
                text = text.replace(char, "")
        
        # 移除零宽字符
        text = re.sub(r'[\u200b-\u200f\u2028-\u202f\ufeff]', '', text)
        
        return text.strip()
`

## 2. 输出安全检查

`python
class OutputFilter:
    '''输出过滤器'''
    
    # 敏感信息模式
    SENSITIVE_PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3,4}[-.]?\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    }
    
    def __init__(self, mask: bool = True):
        self.mask = mask
        self.replacement = "***REDACTED***"
    
    def filter(self, text: str) -> tuple[str, list[str]]:
        '''过滤输出'''
        findings = []
        filtered_text = text
        
        for pattern_name, pattern in self.SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, text)
            
            for match in matches:
                findings.append({
                    "type": pattern_name,
                    "value": match
                })
                
                if self.mask:
                    filtered_text = filtered_text.replace(match, self.replacement)
        
        return filtered_text, findings
    
    def contains_sensitive(self, text: str) -> bool:
        '''检查是否包含敏感信息'''
        _, findings = self.filter(text)
        return len(findings) > 0


class SafetyChecker:
    '''安全检查器'''
    
    def __init__(self):
        self.input_validator = InputValidator()
        self.output_filter = OutputFilter()
    
    def check_input(self, user_input: str) -> ValidationResult:
        '''检查输入'''
        return self.input_validator.validate(user_input)
    
    def check_output(self, agent_output: str) -> tuple[bool, str, list]:
        '''检查输出'''
        filtered, findings = self.output_filter.filter(agent_output)
        
        is_safe = len(findings) == 0
        
        return is_safe, filtered, findings
`

## 3. 权限控制与沙箱

`python
from functools import wraps


class Permission(Enum):
    '''权限'''
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"
    DATABASE = "database"
    ADMIN = "admin"


class PermissionDenied(Exception):
    '''权限不足异常'''
    pass


class AgentPermissions:
    '''Agent权限'''
    
    def __init__(self):
        self.permissions: set[Permission] = set()
        self.deny_list: set[str] = set()
    
    def grant(self, permission: Permission):
        '''授予权限'''
        self.permissions.add(permission)
    
    def deny(self, permission: Permission):
        '''撤销权限'''
        self.permissions.discard(permission)
    
    def check(self, permission: Permission) -> bool:
        '''检查权限'''
        return permission in self.permissions
    
    def require(self, permission: Permission):
        '''要求权限'''
        if not self.check(permission):
            raise PermissionDenied(f"需要权限: {permission.value}")


def require_permission(permission: Permission):
    '''权限检查装饰器'''
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'permissions'):
                self.permissions.require(permission)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class ToolSandbox:
    '''工具沙箱'''
    
    def __init__(self):
        self.allowed_operations: set[str] = set()
        self.blocked_operations: set[str] = set()
        self.resource_limits: dict[str, Any] = {
            "max_memory": 1024 * 1024 * 100,  # 100MB
            "max_time": 30,  # 30秒
            "max_output": 10000  # 10000字符
        }
    
    def allow(self, operation: str):
        '''允许操作'''
        self.allowed_operations.add(operation)
    
    def block(self, operation: str):
        '''阻止操作'''
        self.blocked_operations.add(operation)
    
    def is_allowed(self, operation: str) -> bool:
        '''检查操作是否允许'''
        if operation in self.blocked_operations:
            return False
        
        if self.allowed_operations and operation not in self.allowed_operations:
            return False
        
        return True
    
    def execute(self, operation: str, func, *args, **kwargs):
        '''在沙箱中执行'''
        if not self.is_allowed(operation):
            raise PermissionDenied(f"操作被阻止: {operation}")
        
        # 这里可以添加资源限制检查
        return func(*args, **kwargs)
`

## 4. Guardrails框架

`python
from abc import ABC, abstractmethod


class Guardrail(ABC):
    '''Guardrail基类'''
    
    def __init__(self, name: str):
        self.name = name
        self.enabled: bool = True
    
    @abstractmethod
    def check(self, content: str, context: dict = None) -> tuple[bool, str]:
        '''检查内容'''
        pass


class ProfanityGuardrail(Guardrail):
    '''脏话过滤'''
    
    def __init__(self):
        super().__init__("profanity_filter")
        self.bad_words = ["badword1", "badword2"]  # 示例
    
    def check(self, content: str, context: dict = None) -> tuple[bool, str]:
        content_lower = content.lower()
        
        for word in self.bad_words:
            if word in content_lower:
                filtered = content_lower.replace(word, "***")
                return False, filtered
        
        return True, content


class TopicGuardrail(Guardrail):
    '''主题限制'''
    
    def __init__(self, allowed_topics: list[str] = None):
        super().__init__("topic_guardrail")
        self.allowed_topics = allowed_topics or []
    
    def check(self, content: str, context: dict = None) -> tuple[bool, str]:
        if not self.allowed_topics:
            return True, content
        
        # 简单的关键词检查
        # 实际实现中应该用更复杂的NLP技术
        return True, content


class HallucinationGuardrail(Guardrail):
    '''幻觉检测'''
    
    def __init__(self):
        super().__init__("hallucination_detector")
    
    def check(self, content: str, context: dict = None) -> tuple[bool, str]:
        # 检查是否包含不确定性表述
        uncertainty_phrases = [
            "可能", "也许", "不确定", "我不确定",
            "probably", "maybe", "not sure"
        ]
        
        has_uncertainty = any(phrase in content.lower() for phrase in uncertainty_phrases)
        
        if has_uncertainty:
            return False, f"[需要验证] {content}"
        
        return True, content


class GuardrailsManager:
    '''Guardrails管理器'''
    
    def __init__(self):
        self.guardrails: list[Guardrail] = []
        self.check_history: list[dict] = []
    
    def add_guardrail(self, guardrail: Guardrail):
        '''添加Guardrail'''
        self.guardrails.append(guardrail)
    
    def check(self, content: str, context: dict = None) -> tuple[bool, str, list[str]]:
        '''运行所有Guardrails检查'''
        is_safe = True
        current_content = content
        violations = []
        
        for guardrail in self.guardrails:
            if not guardrail.enabled:
                continue
            
            passed, result = guardrail.check(current_content, context)
            
            if not passed:
                is_safe = False
                violations.append(guardrail.name)
                current_content = result  # 使用过滤后的内容
        
        self.check_history.append({
            "content": content[:100],  # 只记录前100字符
            "is_safe": is_safe,
            "violations": violations
        })
        
        return is_safe, current_content, violations
`

## 5. 红队测试基础

`python
class RedTeamTest:
    '''红队测试'''
    
    def __init__(self, agent, guardrails: GuardrailsManager):
        self.agent = agent
        self.guardrails = guardrails
        self.test_cases: list[dict] = []
        self.results: list[dict] = []
    
    def add_test_case(self, name: str, input_text: str, expected_behavior: str):
        '''添加测试用例'''
        self.test_cases.append({
            "name": name,
            "input": input_text,
            "expected": expected_behavior
        })
    
    def run_all(self) -> list[dict]:
        '''运行所有测试'''
        for test in self.test_cases:
            result = self.run_single(test)
            self.results.append(result)
        
        return self.results
    
    def run_single(self, test: dict) -> dict:
        '''运行单个测试'''
        # 检查Guardrails
        is_safe, filtered, violations = self.guardrails.check(test["input"])
        
        # 如果不安全，检查是否正确阻止
        blocked_correctly = not is_safe
        
        return {
            "test_name": test["name"],
            "input": test["input"],
            "expected": test["expected"],
            "is_safe": is_safe,
            "violations": violations,
            "blocked_correctly": blocked_correctly,
            "passed": blocked_correctly  # 简化的通过条件
        }
    
    def get_report(self) -> dict:
        '''获取测试报告'''
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "details": self.results
        }
`

## 6. 本日总结

- InputValidator验证用户输入
- OutputFilter过滤敏感信息
- AgentPermissions控制工具权限
- ToolSandbox提供沙箱执行
- GuardrailsManager管理安全护栏
- RedTeamTest进行安全测试

明天我们将开始构建AI Assistant Runtime项目！
