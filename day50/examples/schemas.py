\"\"\"Pydantic schemas\"\"\"

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# === User ===
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {\"from_attributes\": True}

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = \"bearer\"


# === Article ===
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: list[str] = []
    is_published: bool = False

class ArticleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    tags: list[str] | None = None
    is_published: bool | None = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: UserResponse
    tags: list[str] = []
    is_published: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {\"from_attributes\": True}

class ArticleListResponse(BaseModel):
    id: int
    title: str
    summary: str
    author_name: str
    tags: list[str]
    created_at: datetime


# === Comment ===
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    id: int
    content: str
    author: UserResponse
    created_at: datetime

    model_config = {\"from_attributes\": True}


# === Pagination ===
class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
