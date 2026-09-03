# Day 78 示例 4: 数据库查询工具
import sqlite3
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data = None
    error: str = ""

class DatabaseTool:
    name = "database_query"
    FORBIDDEN = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE"]
    
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_demo()
    
    def _init_demo(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            c.executemany("INSERT INTO users VALUES (?, ?, ?)", [(1,"Alice",30),(2,"Bob",25),(3,"Charlie",35)])
            self.conn.commit()
    
    def _is_safe(self, query: str) -> tuple:
        for kw in self.FORBIDDEN:
            if kw in query.upper():
                return False, f"禁止: {kw}"
        return True, ""
    
    def execute(self, query: str) -> ToolResult:
        ok, reason = self._is_safe(query)
        if not ok:
            return ToolResult(False, error=reason)
        try:
            c = self.conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            return ToolResult(True, data=[dict(r) for r in rows])
        except Exception as e:
            return ToolResult(False, error=str(e))

if __name__ == "__main__":
    db = DatabaseTool()
    print(db.execute("SELECT * FROM users"))
    print(db.execute("SELECT * FROM users WHERE age > 28"))
    print(db.execute("DROP TABLE users"))
