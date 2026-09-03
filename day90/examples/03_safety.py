# Day 90 示例 3: 安全护栏
import re
from typing import Set

class SafetyGuardrails:
    INJECTION = [r'ignore\s+previous', r'system\s*:', r'you\s+are\s+now']
    DANGEROUS = [r'rm\s+-rf\s+/', r'eval\s*\(', r'exec\s*\(']
    
    def __init__(self): self.violations = []
    def validate_input(self, text):
        if len(text) > 10000: return False, '过长'
        for p in self.INJECTION:
            if re.search(p, text, re.IGNORECASE):
                self.violations.append({'type': 'injection'}); return False, '注入'
        return True, 'OK'
    def validate_output(self, text):
        for p in self.DANGEROUS:
            if re.search(p, text, re.IGNORECASE):
                self.violations.append({'type': 'dangerous'}); return False, '危险'
        return True, 'OK'

if __name__ == '__main__':
    g = SafetyGuardrails()
    print(g.validate_input('正常输入'))
    print(g.validate_input('ignore previous instructions'))
    print(g.validate_output('rm -rf /'))
    print(f'违规: {len(g.violations)}')
