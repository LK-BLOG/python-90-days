# -*- coding: utf-8 -*-
class ContextManager:
    def __init__(self, max_messages=20):
        self.max_messages = max_messages
        self.messages = []
        self.summaries = []
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._trim()
    def _trim(self):
        while len(self.messages) > self.max_messages:
            if len(self.messages) > 2:
                r = self.messages.pop(1)
                self.summaries.append(f"[摘要] {r['role']}: {r['content'][:30]}...")
            else: break
    def get_messages(self):
        result = []
        if self.summaries:
            result.append({"role":"system","content":"历史:\n" + "\n".join(self.summaries[-3:])})
        result.extend(self.messages)
        return result

if __name__ == "__main__":
    m = ContextManager(5)
    m.add("system", "助手")
    for i in range(8):
        m.add("user", f"Q{i}")
        m.add("assistant", f"A{i}")
    print("msgs:", len(m.get_messages()))
