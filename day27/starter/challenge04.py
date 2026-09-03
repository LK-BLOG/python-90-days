# Day 27 - Challenge 4: 分页处理器
# 难度: ⭐⭐⭐
# 支持多种分页方式、自动获取所有页面、进度显示、内存优化

from typing import Any, Callable, Iterator
from dataclasses import dataclass


@dataclass
class PageResult:
    """单页结果"""
    items: list[Any]
    page_number: int
    total_pages: int
    has_next: bool
    total_items: int


class PaginationStrategy:
    """分页策略基类"""

    def get_next_params(self, current_page: int, page_size: int) -> dict:
        """获取下一页的请求参数"""
        raise NotImplementedError


class OffsetStrategy(PaginationStrategy):
    """偏移量分页：offset=0,10,20..."""

    def get_next_params(self, current_page: int, page_size: int) -> dict:
        # TODO: return {"offset": current_page * page_size, "limit": page_size}
        ...


class CursorStrategy(PaginationStrategy):
    """游标分页：cursor=xxx"""

    def __init__(self):
        self._next_cursor: str | None = None

    def get_next_params(self, current_page: int, page_size: int) -> dict:
        # TODO: return {"cursor": self._next_cursor, "limit": page_size}
        ...


class PageNumberStrategy(PaginationStrategy):
    """页码分页：page=1,2,3..."""

    def get_next_params(self, current_page: int, page_size: int) -> dict:
        # TODO: return {"page": current_page + 1, "per_page": page_size}
        ...


class PaginationHandler:
    """分页处理器

    自动遍历所有分页数据，支持进度回调和内存优化。
    """

    def __init__(self, fetch_func: Callable[[dict], dict],
                 strategy: PaginationStrategy = None,
                 page_size: int = 20):
        """初始化

        Args:
            fetch_func: 获取单页数据的函数，接收参数字典，返回结果字典
            strategy: 分页策略
            page_size: 每页大小
        """
        self.fetch_func = fetch_func
        self.strategy = strategy or OffsetStrategy()
        self.page_size = page_size

    def fetch_all(self, progress_callback: Callable = None) -> list[Any]:
        """获取所有分页数据

        Args:
            progress_callback: 进度回调函数 callback(current, total)

        Returns:
            所有数据项的扁平列表
        """
        # TODO: 循环调用 fetch_func
        # TODO: 解析响应中的 items 和分页信息
        # TODO: 通过 progress_callback 报告进度
        # TODO: 到达最后一页时停止
        ...

    def iter_pages(self) -> Iterator[PageResult]:
        """迭代器方式逐页获取（内存友好）

        Yields:
            每页的 PageResult
        """
        # TODO: 使用 yield 逐页返回
        ...

    def fetch_all_streaming(self, callback: Callable = None) -> Iterator[Any]:
        """流式获取所有数据项（最省内存）

        Args:
            callback: 每页处理完的回调

        Yields:
            每个数据项
        """
        # TODO: 逐页遍历，逐项 yield
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    # 模拟数据源
    mock_data = [{"id": i, "name": f"item_{i}"} for i in range(55)]

    def mock_fetch(params: dict) -> dict:
        offset = params.get("offset", 0)
        limit = params.get("limit", 20)
        items = mock_data[offset:offset + limit]
        return {
            "items": items,
            "total": len(mock_data),
            "has_next": offset + limit < len(mock_data),
        }

    handler = PaginationHandler(mock_fetch, OffsetStrategy(), page_size=20)
    all_items = handler.fetch_all()
    print(f"总共获取 {len(all_items)} 条数据")
