# -*- coding: utf-8 -*-
"""Day 71：微调数据集格式化。"""
import json
from pathlib import Path
class FormatPractice:
    def format_qa(self, q: str, a: str, system: str = "") -> dict:
        """转换为聊天微调数据格式。"""
        if not q.strip() or not a.strip(): raise ValueError("问题和答案不能为空")
        # TODO：补充元数据、工具调用和多轮消息格式
        messages=[]
        if system: messages.append({"role":"system","content":system})
        messages += [{"role":"user","content":q},{"role":"assistant","content":a}]
        return {"messages":messages}
    def export_jsonl(self, data: list[dict], path: str | Path) -> Path:
        """逐行写出JSONL，确保每行都是合法JSON。"""
        # TODO：处理目录创建、编码和失败回滚
        p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(x, ensure_ascii=False)+"\n" for x in data), encoding="utf-8")
        return p
if __name__ == "__main__": print(FormatPractice().format_qa("问题", "答案"))
