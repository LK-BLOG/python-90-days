class QueryBuilder:
    def __init__(self):
        self._table: str = ""
        self._conditions: list[str] = []
        self._limit: int = 0

    def table(self, name: str) -> "QueryBuilder":
        pass  # TODO: return self for chaining

    def where(self, condition: str) -> "QueryBuilder":
        pass  # TODO

    def limit(self, n: int) -> "QueryBuilder":
        pass  # TODO

    def build(self) -> str:
        pass  # TODO: build SQL string

# Test
if __name__ == "__main__":
    query = (QueryBuilder()
             .table("users")
             .where("age > 18")
             .where("active = true")
             .limit(10)
             .build())
    print(query)