# -*- coding: utf-8 -*-
class SpeechPipeline:
    def transcribe(self, audio): return f"[转写] {audio}的内容"
    def synthesize(self, text, voice="alloy"): return f"[合成] voice={voice}"
    def voice_assistant(self, audio):
        t = self.transcribe(audio)
        r = f"你说: {t}"
        return {"text": r, "audio": self.synthesize(r)}
if __name__ == "__main__":
    print(SpeechPipeline().voice_assistant("rec.wav"))
