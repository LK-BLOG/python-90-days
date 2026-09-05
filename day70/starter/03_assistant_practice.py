# -*- coding: utf-8 -*-
"""Day 70：语音助手流水线骨架：STT -> LLM -> TTS。"""
from typing import Callable, Any
class AssistantPractice:
    def __init__(self, stt: Callable[..., Any] | None = None, llm: Callable[..., str] | None = None, tts: Callable[..., Any] | None = None):
        self.stt, self.llm, self.tts = stt, llm, tts
    def process(self, audio_path: str) -> dict[str, Any]:
        """处理一段语音输入并返回各阶段结果。"""
        # TODO：依次调用STT、LLM、TTS，并处理任一阶段失败
        if not self.stt or not self.llm or not self.tts: raise RuntimeError("请注入完整的三阶段服务")
        text = self.stt(audio_path)
        answer = self.llm(text)
        audio = self.tts(answer)
        return {"text": text, "answer": answer, "audio": audio}
if __name__ == "__main__": print("语音助手骨架")
