from typing import List, Dict, Callable

class SmartWindow:
    def __init__(self, max_tokens: int, count_fn: Callable = None):
        pass

    def add(self, role: str, content: str):
        pass

    def _score(self, msg: Dict, idx: int, total: int) -> float:
        pass

    def select(self) -> List[Dict]:
        pass

    def get_messages(self) -> List[Dict]:
        return self.select()

    def stats(self) -> Dict:
        pass


if __name__ == "__main__":
    pass
