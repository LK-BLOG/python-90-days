# -*- coding: utf-8 -*-
class ChatSession:
    def __init__(self, system="你是一个助手"):
        self.messages = [{"role":"system","content":system}]
    def chat(self, text):
        self.messages.append({"role":"user","content":text})
        reply = f"[回复] {text}"
        self.messages.append({"role":"assistant","content":reply})
        return reply
    def clear(self):
        self.messages = [self.messages[0]]
if __name__ == "__main__":
    s = ChatSession("Python老师")
    print(s.chat("什么是装饰器?"))
    print(s.chat("给我例子"))
