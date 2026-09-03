# Day 76 示例 3: Agent vs Chatbot vs Copilot
\"\"\"
对比三种交互模式的本质区别
\"\"\"
from abc import ABC, abstractmethod


class Chatbot:
    \"\"\"聊天机器人 - 一问一答，无工具，无循环\"\"\"
    
    def __init__(self, name: str = "Chatbot"):
        self.name = name
    
    def respond(self, user_input: str) -> str:
        # 纯文本生成，没有工具调用
        return f"[{self.name}] 基于 '{user_input}' 的回答..."
    
    def chat(self, messages: list[str]) -> list[str]:
        responses = []
        for msg in messages:
            responses.append(self.respond(msg))
        return responses


class Copilot:
    \"\"\"副驾驶 - 建议模式，人类在环\"\"\"
    
    def __init__(self, name: str = "Copilot"):
        self.name = name
        self.suggestions = []
    
    def suggest(self, context: str) -> list[dict]:
        \"\"\"生成建议，等待人类批准\"\"\"
        self.suggestions = [
            {"action": "edit_code", "desc": "修改这段代码", "approved": None},
            {"action": "add_test", "desc": "添加测试用例", "approved": None},
            {"action": "refactor", "desc": "重构为更简洁的写法", "approved": None},
        ]
        return self.suggestions
    
    def apply_approved(self) -> list[str]:
        \"\"\"只执行人类批准的建议\"\"\"
        results = []
        for s in self.suggestions:
            if s["approved"]:
                results.append(f"✅ 执行: {s['desc']}")
            else:
                results.append(f"⏭ 跳过: {s['desc']}")
        return results


class Agent:
    \"\"\"智能体 - 自主循环，独立完成任务\"\"\"
    
    def __init__(self, name: str = "Agent"):
        self.name = name
        self.memory = []
        self.step_count = 0
    
    def perceive(self, environment: str) -> str:
        \"\"\"感知环境\"\"\"
        return f"感知到: {environment}"
    
    def think(self, perception: str, goal: str) -> str:
        \"\"\"推理决策\"\"\"
        self.step_count += 1
        return f"思考#{self.step_count}: 基于 '{perception}'，为达成 '{goal}'，我需要..."
    
    def act(self, thought: str) -> str:
        \"\"\"执行行动\"\"\"
        action = f"行动#{self.step_count}: 执行操作"
        self.memory.append({"thought": thought, "action": action})
        return action
    
    def execute(self, goal: str, environment: str = "默认环境") -> str:
        \"\"\"自主执行循环\"\"\"
        print(f"🤖 [{self.name}] 开始执行: {goal}")
        
        for _ in range(5):  # 最大步数
            perception = self.perceive(environment)
            thought = self.think(perception, goal)
            result = self.act(thought)
            print(f"  {result}")
            
            if self._is_done(goal):
                break
        
        return f"完成！总共 {self.step_count} 步"
    
    def _is_done(self, goal: str) -> bool:
        return self.step_count >= 3  # 模拟完成条件


# 对比演示
if __name__ == "__main__":
    print("=" * 60)
    print("1️⃣  Chatbot 模式")
    print("=" * 60)
    chatbot = Chatbot("GPT-3.5")
    print(chatbot.respond("帮我写个排序算法"))
    print("特点: 无工具调用，纯文本生成，一问一答\n")
    
    print("=" * 60)
    print("2️⃣  Copilot 模式")
    print("=" * 60)
    copilot = Copilot("GitHub Copilot")
    suggestions = copilot.suggest("当前代码: def sort(arr): ...")
    for s in suggestions:
        s["approved"] = True  # 模拟人类批准
    print(copilot.apply_approved())
    print("特点: 建议+人类批准，辅助角色\n")
    
    print("=" * 60)
    print("3️⃣  Agent 模式")
    print("=" * 60)
    agent = Agent("AutoGPT")
    result = agent.execute("写一个完整的Web应用")
    print(result)
    print("特点: 自主循环，独立完成，目标驱动")
