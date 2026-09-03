\"\"\"API测试示例\"\"\"

import pytest

# 以下为测试结构模板，需要根据实际实现调整


class TestAuth:
    \"\"\"认证测试\"\"\"

    @pytest.mark.asyncio
    async def test_register(self, client):
        resp = await client.post(\"/api/v1/auth/register\", json={
            \"username\": \"testuser\",
            \"email\": \"test@example.com\",
            \"password\": \"test123456\"
        })
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_register_duplicate(self, client):
        # 注册两次相同用户名
        await client.post(\"/api/v1/auth/register\", json={
            \"username\": \"dup_user\", \"email\": \"a@a.com\", \"password\": \"test123456\"
        })
        resp = await client.post(\"/api/v1/auth/register\", json={
            \"username\": \"dup_user\", \"email\": \"b@b.com\", \"password\": \"test123456\"
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_login(self, client):
        # 先注册
        await client.post(\"/api/v1/auth/register\", json={
            \"username\": \"loginuser\", \"email\": \"login@test.com\", \"password\": \"test123456\"
        })
        # 登录
        resp = await client.post(\"/api/v1/auth/login\", data={
            \"username\": \"loginuser\", \"password\": \"test123456\"
        })
        assert resp.status_code == 200
        assert \"access_token\" in resp.json()


class TestArticles:
    \"\"\"文章测试\"\"\"

    @pytest.mark.asyncio
    async def test_create_article(self, client, auth_headers):
        resp = await client.post(\"/api/v1/articles/\", json={
            \"title\": \"Test Article\", \"content\": \"Content here\"
        }, headers=auth_headers)
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_list_articles_pagination(self, client):
        resp = await client.get(\"/api/v1/articles/?page=1&page_size=10\")
        assert resp.status_code == 200
        data = resp.json()
        assert \"items\" in data
        assert \"total\" in data

    @pytest.mark.asyncio
    async def test_author_can_delete(self, client, auth_headers):
        # 创建
        resp = await client.post(\"/api/v1/articles/\", json={
            \"title\": \"To Delete\", \"content\": \"Content\"
        }, headers=auth_headers)
        article_id = resp.json()[\"id\"]
        # 删除
        resp = await client.delete(f\"/api/v1/articles/{article_id}\", headers=auth_headers)
        assert resp.status_code == 204

    @pytest.mark.asyncio
    async def test_non_author_cannot_delete(self, client, auth_headers, other_auth_headers):
        # 创建
        resp = await client.post(\"/api/v1/articles/\", json={
            \"title\": \"Author Only\", \"content\": \"Content\"
        }, headers=auth_headers)
        article_id = resp.json()[\"id\"]
        # 其他用户尝试删除
        resp = await client.delete(f\"/api/v1/articles/{article_id}\", headers=other_auth_headers)
        assert resp.status_code == 403
