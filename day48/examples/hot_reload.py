\"\"\"配置热更新\"\"\"

import json
import time
import threading
from pathlib import Path
from typing import Callable, Any
from dataclasses import dataclass, field


@dataclass
class ConfigManager:
    \"\"\"支持热更新的配置管理器\"\"\"

    _config: dict = field(default_factory=dict)
    _callbacks: list[Callable] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _watch_thread: threading.Thread | None = None
    _running: bool = False

    def load(self, path: str) -> dict:
        with open(path) as f:
            with self._lock:
                self._config = json.load(f)
        return dict(self._config)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            old = self._config.get(key)
            self._config[key] = value
        if old != value:
            self._notify(key, old, value)

    def on_change(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    def _notify(self, key: str, old: Any, new: Any) -> None:
        for cb in self._callbacks:
            try:
                cb(key, old, new)
            except Exception as e:
                print(f\"Callback error: {e}\")

    def reload(self, path: str) -> None:
        with open(path) as f:
            new_config = json.load(f)
        with self._lock:
            old_config = dict(self._config)
            self._config = new_config

        # 通知变化
        for key in set(list(old_config.keys()) + list(new_config.keys())):
            if old_config.get(key) != new_config.get(key):
                self._notify(key, old_config.get(key), new_config.get(key))

    def watch(self, path: str, interval: float = 2.0) -> None:
        \"\"\"监控配置文件变化\"\"\"
        last_mtime = Path(path).stat().st_mtime

        def _watch():
            nonlocal last_mtime
            self._running = True
            while self._running:
                time.sleep(interval)
                try:
                    mtime = Path(path).stat().st_mtime
                    if mtime > last_mtime:
                        last_mtime = mtime
                        self.reload(path)
                        print(f\"Config reloaded from {path}\")
                except Exception:
                    pass

        self._watch_thread = threading.Thread(target=_watch, daemon=True)
        self._watch_thread.start()

    def stop_watching(self) -> None:
        self._running = False


if __name__ == \"__main__\":
    import tempfile, os

    # 创建临时配置文件
    config_path = tempfile.mktemp(suffix=\".json\")
    with open(config_path, \"w\") as f:
        json.dump({\"db_host\": \"localhost\", \"port\": 8000, \"debug\": True}, f)

    manager = ConfigManager()

    # 注册变更回调
    def on_config_change(key, old, new):
        print(f\"  Config changed: {key}: {old} -> {new}\")

    manager.on_change(on_config_change)
    manager.load(config_path)

    print(f\"Initial: {manager.get('db_host')}, {manager.get('port')}\")

    # 模拟文件变化
    time.sleep(0.5)
    with open(config_path, \"w\") as f:
        json.dump({\"db_host\": \"prod-server\", \"port\": 443, \"debug\": False, \"new_key\": \"added\"}, f)

    time.sleep(3)
    print(f\"After reload: {manager.get('db_host')}, {manager.get('port')}\")

    os.unlink(config_path)
