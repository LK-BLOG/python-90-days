# -*- coding: utf-8 -*-
"""Day 70：语音转文字与文字转语音接口。"""
from pathlib import Path
class SpeechPractice:
    def transcribe(self, audio: str | Path) -> dict[str, str]:
        """将音频转换成文字，返回文本和语言。"""
        p=Path(audio)
        if not p.exists(): raise FileNotFoundError(p)
        # TODO：接入STT服务，处理格式、语言和时间戳
        return {"text":"", "language":"unknown"}
    def synthesize(self, text: str, output: str | Path = "speech.mp3") -> Path:
        """将文字合成为音频文件。"""
        if not text.strip(): raise ValueError("文字不能为空")
        # TODO：接入TTS服务并写入output
        return Path(output)
if __name__ == "__main__": print("请实现STT/TTS服务调用")
