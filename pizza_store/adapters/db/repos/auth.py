import edgedb

from pizza_store.services.auth.models import User, UserCreated, UserInRepoCreate


class AuthServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_user(self, user: UserInRepoCreate) -> UserCreated:
        query = """
        insert auth::User {
            username := <str>$username,
            password_hash := <str>$password_hash,
            is_admin := <bool>$is_admin
        };
        """
        result = await self._client.query_single(
            query,
            username=user.username,
            password_hash=user.password_hash,
            is_admin=user.is_admin,
        )
        # TODO: raise error if alrady exists
        return UserCreated(id=result.id)

    async def get_user(self, username: str) -> User:
        query = """
        select auth::User {
            id,
            username,
            password_hash,
            is_admin
        } filter .username = <str>$username;
        """
        result = await self._client.query_single(query, username=username)
        # TODO: raise error if not exists
        return User(
            id=result.id,
            username=result.username,
            password_hash=result.password_hash,
            is_admin=result.is_admin,
        )
