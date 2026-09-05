# -*- coding: utf-8 -*-
"""Day 74：多格式文档加载器。"""
from pathlib import Path
from typing import Any
class LoaderPractice:
    def __init__(self, parsers: dict[str, Any] | None = None): self.parsers=parsers or {}
    def load(self, path: str | Path) -> dict[str, Any]:
        """根据扩展名选择解析器，统一输出文档结构。"""
        p=Path(path)
        if not p.exists(): raise FileNotFoundError(p)
        suffix=p.suffix.lower()
        # TODO：注册PDF/DOCX/HTML/Markdown解析器并统一元数据
        parser=self.parsers.get(suffix)
        if parser is None:
            return {"text":p.read_text(encoding="utf-8"),"source":str(p),"type":suffix}
        return {"text":parser(p),"source":str(p),"type":suffix}
    def load_batch(self, paths: list[str | Path]) -> list[dict[str, Any]]:
        """批量加载文档，记录单个文件错误而不是让全批次崩溃。"""
        # TODO：返回成功/失败分组和错误报告
        return [self.load(p) for p in paths]
if __name__ == "__main__": print("请传入文档路径")
