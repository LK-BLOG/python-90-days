\"\"\"使用dependency-injector框架\"\"\"

from dependency_injector import containers, providers
from dataclasses import dataclass


# 模拟服务
@dataclass
class UserRepository:
    db_url: str = \"\"
    def find_all(self) -> list[dict]:
        return [{\"id\": 1, \"name\": \"Alice\"}]
    def save(self, user: dict) -> None:
        print(f\"Saved: {user}\")


@dataclass
class PostRepository:
    db_url: str = \"\"
    def find_all(self) -> list[dict]:
        return [{\"id\": 1, \"title\": \"Hello\"}]


@dataclass
class UserService:
    user_repo: UserRepository = None
    def get_users(self) -> list[dict]:
        return self.user_repo.find_all()


@dataclass
class PostService:
    post_repo: PostRepository = None
    def get_posts(self) -> list[dict]:
        return self.post_repo.find_all()


# DI容器
class ApplicationContainer(containers.DeclarativeContainer):
    \"\"\"应用DI容器\"\"\"

    config = providers.Configuration()

    # Repository providers
    user_repo = providers.Factory(
        UserRepository,
        db_url=config.db.url,
    )

    post_repo = providers.Factory(
        PostRepository,
        db_url=config.db.url,
    )

    # Service providers (注入依赖)
    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
    )

    post_service = providers.Factory(
        PostService,
        post_repo=post_repo,
    )


def demo():
    container = ApplicationContainer()

    # 配置
    container.config.from_dict({
        \"db\": {\"url\": \"postgresql://localhost/blog\"}
    })

    # 解析服务
    user_svc = container.user_service()
    post_svc = container.post_service()

    print(\"Users:\", user_svc.get_users())
    print(\"Posts:\", post_svc.get_posts())

    # 验证单例行为
    assert user_svc is not container.user_service()  # Factory = 不同实例

    # 验证依赖注入
    print(f\"UserRepo URL: {user_svc.user_repo.db_url}\")


if __name__ == \"__main__\":
    demo()
