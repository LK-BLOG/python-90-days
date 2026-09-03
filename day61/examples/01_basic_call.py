# -*- coding: utf-8 -*-
import os
def mock_chat(messages, model="gpt-4o-mini"):
    msg = messages[-1]["content"] if messages else ""
    return {"content": "[Mock] " + msg, "usage": {"prompt_tokens":10,"completion_tokens":20,"total_tokens":30}}
def chat(messages, model="gpt-4o-mini"):
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        r = OpenAI().chat.completions.create(model=model, messages=messages)
        return {"content": r.choices[0].message.content, "usage":{"total_tokens": r.usage.total_tokens}}
    return mock_chat(messages, model)
if __name__ == "__main__":
    r = chat([{"role":"user","content":"用一句话解释Python"}])
    print("回复:", r["content"])
