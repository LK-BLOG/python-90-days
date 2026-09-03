class SystemPromptBuilder:
    def __init__(self, template: str):
        pass

    def set_var(self, key: str, value: str) -> 'SystemPromptBuilder':
        pass

    def set_conditional(self, name: str, enabled: bool) -> 'SystemPromptBuilder':
        pass

    def build(self) -> str:
        pass

    def estimate_tokens(self) -> int:
        pass


class PromptRegistry:
    def __init__(self):
        self.prompts = {}

    def register(self, name: str, builder: SystemPromptBuilder):
        pass

    def get(self, name: str) -> str:
        pass

    def list_versions(self) -> list:
        pass


if __name__ == "__main__":
    pass
