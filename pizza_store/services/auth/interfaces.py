from typing import Protocol

from pizza_store.services.auth.models import User, UserCreated, UserInRepoCreate


class IAuthServiceRepo(Protocol):
    async def create_user(self, user: UserInRepoCreate) -> UserCreated:
        ...

    async def get_user(self, username: str) -> User:
        ...
