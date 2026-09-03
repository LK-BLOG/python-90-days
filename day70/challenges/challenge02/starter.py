# -*- coding: utf-8 -*-
class SpeechToText:
    def __init__(self, model='whisper-1'):
        self.model = model
    def transcribe(self, audio_path, language='zh'):
        # TODO
        pass
    def transcribe_stream(self, audio_stream):
        # TODO: 流式转写
        pass
