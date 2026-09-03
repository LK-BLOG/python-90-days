\"\"\"Pydantic高级序列化\"\"\"

from pydantic import BaseModel, Field, field_serializer, ConfigDict
from datetime import datetime
from typing import Any


class Article(BaseModel):
    title: str
    content: str
    tags: list[str] = []
    author: str = \"\"
    created_at: datetime = Field(default_factory=datetime.now)
    is_published: bool = False

    model_config = ConfigDict(from_attributes=True)

    @field_serializer(\"created_at\")
    def serialize_date(self, v: datetime) -> str:
        return v.strftime(\"%Y-%m-%d %H:%M\")

    def to_xml(self) -> str:
        tags_xml = \"\".join(f\"<tag>{t}</tag>\" for t in self.tags)
        return (
            f\"<article>\"
            f\"<title>{self.title}</title>\"
            f\"<content>{self.content}</content>\"
            f\"<tags>{tags_xml}</tags>\"
            f\"<author>{self.author}</author>\"
            f\"<created_at>{self.created_at.strftime('%Y-%m-%d')}</created_at>\"
            f\"</article>\"
        )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    items: list[dict]
    total: int
    page: int
    page_size: int

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_dict(self) -> dict:
        return self.model_dump()


if __name__ == \"__main__\":
    article = Article(
        title=\"Hello World\",
        content=\"This is a test article.\",
        tags=[\"python\", \"tutorial\"],
        author=\"Alice\",
    )

    print(\"JSON:\", article.model_dump_json(indent=2))
    print(\"\\nDict:\", article.model_dump())
    print(\"\\nXML:\", article.to_xml())
