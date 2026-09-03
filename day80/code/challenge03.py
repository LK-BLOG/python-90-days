from typing import List, Dict, Callable

class CompressionStrategy:
    def compress(self, messages: List[Dict], target_tokens: int, count_fn: Callable) -> List[Dict]:
        pass


class SummaryCompression(CompressionStrategy):
    def __init__(self):
        pass
    def compress(self, messages, target_tokens, count_fn):
        pass


class ExtractiveCompression(CompressionStrategy):
    def compress(self, messages, target_tokens, count_fn):
        pass


class SmartCompression(CompressionStrategy):
    def __init__(self, summary_threshold: float = 0.7):
        pass
    def compress(self, messages, target_tokens, count_fn):
        pass


if __name__ == "__main__":
    pass
