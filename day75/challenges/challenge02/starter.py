# -*- coding: utf-8 -*-
class ConversationManager:
    def __init__(self, system_prompt=''):
        self.history = []
        self.system = system_prompt
    def add_user(self, text):
        # TODO
        pass
    def add_assistant(self, text):
        # TODO
        pass
    def get_context(self, max_turns=5):
        # TODO: 获取上下文
        pass
    def clear(self):
        # TODO
        pass
