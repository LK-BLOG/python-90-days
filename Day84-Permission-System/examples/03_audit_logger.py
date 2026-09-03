"""Day 84 Example 03: 审计日志系统"""

import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path
from collections import Counter


@dataclass
class AuditEntry:
    """审计日志条目"""
    timestamp: str
    user: str
    action: str
    resource: str
    function: str
    result: str  # success / denied / error
    details: Optional[str] = None
    ip: Optional[str] = None


class AuditLogger:
    """生产级审计日志"""

    def __init__(self, log_dir: str = "audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._entries: List[AuditEntry] = []
        self._current_file = self.log_dir / self._date_str() / "audit.jsonl"

    @staticmethod
    def _date_str() -> str:
        return datetime.date.today().isoformat()

    def log(self, user: str, action: str, resource: str,
            function: str, result: str = "success",
            details: str = None, ip: str = None):
        """记录审计事件"""
        entry = AuditEntry(
            timestamp=datetime.datetime.now().isoformat(),
            user=user, action=action, resource=resource,
            function=function, result=result,
            details=details, ip=ip,
        )
        self._entries.append(entry)

        # 追加写入 JSONL 文件（每天一个文件）
        date_dir = self.log_dir / self._date_str()
        date_dir.mkdir(parents=True, exist_ok=True)
        jsonl_path = date_dir / "audit.jsonl"
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

        # 控制台输出
        sym = {"success": "✓", "denied": "✗", "error": "!"}.get(result, "?")
        print(f"  [{sym}] {user} | {action} | {resource} | {function}")

    def query(self, user: str = None, resource: str = None,
              result: str = None, since: str = None) -> List[AuditEntry]:
        """查询审计日志"""
        entries = self._entries
        if user:
            entries = [e for e in entries if e.user == user]
        if resource:
            entries = [e for e in entries if e.resource == resource]
        if result:
            entries = [e for e in entries if e.result == result]
        if since:
            entries = [e for e in entries if e.timestamp >= since]
        return entries

    def summary(self, hours: int = 24) -> dict:
        """审计统计摘要"""
        cutoff = (
            datetime.datetime.now() - datetime.timedelta(hours=hours)
        ).isoformat()
        recent = [e for e in self._entries if e.timestamp >= cutoff]

        user_counts = Counter(e.user for e in recent)
        action_counts = Counter(e.action for e in recent)
        result_counts = Counter(e.result for e in recent)
        denied = [e for e in recent if e.result == "denied"]

        return {
            "total_events": len(recent),
            "by_user": dict(user_counts),
            "by_action": dict(action_counts),
            "by_result": dict(result_counts),
            "denied_count": len(denied),
            "top_denied_users": Counter(
                e.user for e in denied
            ).most_common(5),
        }

    def security_alerts(self) -> List[dict]:
        """安全告警：检测异常模式"""
        alerts = []

        # 检查单用户大量被拒绝
        denied_by_user = Counter(
            e.user for e in self._entries if e.result == "denied"
        )
        for user, count in denied_by_user.items():
            if count >= 5:
                alerts.append({
                    "type": "excessive_denials",
                    "user": user,
                    "count": count,
                    "message": f"用户 '{user}' 被拒绝 {count} 次，可能在暴力破解",
                })

        # 检查非工作时间访问
        for entry in self._entries:
            hour = int(entry.timestamp.split("T")[1].split(":")[0])
            if hour < 6 or hour > 23:
                alerts.append({
                    "type": "off_hours_access",
                    "user": entry.user,
                    "time": entry.timestamp,
                    "message": f"用户 '{entry.user}' 在非工作时间访问",
                })

        return alerts

    def export(self, path: str):
        """导出为 JSON"""
        Path(path).write_text(
            json.dumps(
                [asdict(e) for e in self._entries],
                indent=2, ensure_ascii=False
            ),
            encoding="utf-8"
        )


# ========== 使用示例 ==========
def main():
    logger = AuditLogger("audit_demo")

    print("=== 模拟操作 ===")
    logger.log("alice", "read", "file:/config.yaml", "load_config")
    logger.log("alice", "write", "file:/config.yaml", "save_config")
    logger.log("bob", "read", "file:/secret.key", "read_key", result="denied")
    logger.log("bob", "read", "file:/secret.key", "read_key", result="denied")
    logger.log("bob", "read", "file:/secret.key", "read_key", result="denied")
    logger.log("alice", "execute", "tool:shell", "run_command")
    logger.log("root", "manage", "user:bob", "create_user")

    # 查询
    print("\n=== Alice 的操作 ===")
    for e in logger.query(user="alice"):
        print(f"  {e.timestamp[:19]} | {e.action} | {e.resource}")

    # 统计
    print("\n=== 统计摘要 ===")
    s = logger.summary()
    print(f"  总事件: {s['total_events']}")
    print(f"  被拒绝: {s['denied_count']}")
    print(f"  按用户: {s['by_user']}")

    # 安全告警
    print("\n=== 安全告警 ===")
    for alert in logger.security_alerts():
        print(f"  ⚠ {alert['message']}")


if __name__ == "__main__":
    main()
