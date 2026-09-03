# Day 87 骨架代码
class InputGuard:
    def validate(self, text): pass

class OutputGuard:
    def validate_output(self, output): pass

class Guardrails:
    def add(self, name, check_fn, action='block'): pass
    def validate(self, text): pass
