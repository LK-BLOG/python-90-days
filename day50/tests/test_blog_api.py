\"\"\"Day 50: 博客API测试\"\"\"

import pytest


def test_user_model():
    from models import User, Base
    from sqlalchemy import create_engine, inspect

    engine = create_engine(\"sqlite:///:memory:\")
    Base.metadata.create_all(engine)
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    assert \"users\" in tables
    assert \"articles\" in tables
    assert \"comments\" in tables


def test_article_schema():
    from schemas import ArticleCreate, ArticleUpdate

    article = ArticleCreate(title=\"Test\", content=\"Hello World\")
    assert article.title == \"Test\"
    assert article.tags == []
    assert article.is_published is False

    update = ArticleUpdate(title=\"Updated\")
    assert update.title == \"Updated\"
    assert update.content is None


def test_jwt():
    from auth import create_access_token, decode_token

    token = create_access_token({\"sub\": \"1\", \"username\": \"alice\"})
    payload = decode_token(token)
    assert payload[\"sub\"] == \"1\"
    assert payload[\"username\"] == \"alice\"


def test_password():
    from auth import hash_password, verify_password

    hashed = hash_password(\"test123\")
    assert verify_password(\"test123\", hashed)
    assert not verify_password(\"wrong\", hashed)
