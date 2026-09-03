from typing import Protocol, Any

class Plugin(Protocol):
    name: str
    def execute(self, data: dict[str, Any]) -> dict[str, Any]: ...

class LoggerPlugin:
    name: str = "logger"
    def execute(self, data):
        print(f"Log: {data}")
        return data

def run_plugin(plugin: Plugin, data: dict) -> dict:
    pass  # TODO: call plugin.execute

# Test
if __name__ == "__main__":
    result = run_plugin(LoggerPlugin(), {"action": "test"})
    print(result)