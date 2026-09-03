# -*- coding: utf-8 -*-
import json
class FinetuneDataFormatter:
    def __init__(self, system="你是助手"):
        self.system = system
    def format_qa(self, qa_pairs):
        msgs = [{"role":"system","content":self.system}]
        for q,a in qa_pairs:
            msgs.extend([{"role":"user","content":q},{"role":"assistant","content":a}])
        return {"messages": msgs}
if __name__ == "__main__":
    fmt = FinetuneDataFormatter("Python老师")
    print(json.dumps(fmt.format_qa([("什么是装饰器","装饰器是语法糖")]), ensure_ascii=False, indent=2))
