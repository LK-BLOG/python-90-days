# Day 89 骨架代码 - Runtime ②
class MemoryManager:
    def __init__(self, size=50): pass
    def add_message(self, role, content): pass
    def get_messages(self, last_n=None): pass
    def get_context(self): pass

class PlanningModule:
    def create_plan(self, goal, tools): pass

class SelfCorrectionModule:
    def check_output(self, output, goal): pass
    def correct(self, output, issues, goal): pass

class AssistantRuntime:
    def __init__(self): pass
    def register_tool(self, name, tool): pass
    def run(self, goal): pass
