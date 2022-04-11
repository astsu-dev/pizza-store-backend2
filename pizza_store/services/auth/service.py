import datetime
import uuid

import bcrypt
import jwt

from pizza_store.services.auth.exceptions import (
    AccessForbiddenError,
    InvalidAccessToken,
    InvalidCredentialsError,
    UserNotFoundError,
)
from pizza_store.services.auth.interfaces import IAuthServiceRepo
from pizza_store.services.auth.models import (
    JWTConfig,
    UserCreate,
    UserInRepoCreate,
    UserLogIn,
    UserToken,
    UserTokenData,
)


class AuthService:
    def __init__(self, repo: IAuthServiceRepo, jwt_config: JWTConfig) -> None:
        self._repo = repo
        self._jwt_config = jwt_config

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Returns hashed `password."""

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return password_hash

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    @classmethod
    def create_access_token(
        cls, user: UserTokenData, timestamp: int, config: JWTConfig
    ) -> str:
        user_id = str(user.id)
        expiration_timestamp = timestamp + config.expires_in
        data = {
            "sub": user_id,
            "iat": timestamp,
            "exp": expiration_timestamp,
            "user": {"id": user_id, "is_admin": user.is_admin},
        }
        token = jwt.encode(data, config.secret, algorithm=config.algorithm)
        return token

    @classmethod
    def decode_access_token(cls, token: str, config: JWTConfig) -> UserTokenData:
        """Decodes access token and returns user from it."""

        try:
            token_data = jwt.decode(token, config.secret, algorithms=[config.algorithm])
        except jwt.PyJWTError:
            raise InvalidAccessToken
        return UserTokenData(
            id=token_data["user"]["id"], is_admin=token_data["user"]["is_admin"]
        )

    async def register_user(self, user: UserCreate) -> UserToken:
        """Registers a user.

        Returns:
            Token
        """

        password_hash = self.hash_password(user.password)
        is_admin = False
        user_in_repo = await self._repo.create_user(
            UserInRepoCreate(user.username, password_hash, is_admin)
        )

        return self._create_user_token(user_in_repo.id, is_admin)

    async def login_user(self, user: UserLogIn) -> UserToken:
        """Login a user.

        Returns:
            Token
        """

        try:
            user_in_repo = await self._repo.get_user(user.username)
        except UserNotFoundError:
            raise InvalidCredentialsError

        if not self.verify_password(user.password, user_in_repo.password_hash):
            raise InvalidCredentialsError

        return self._create_user_token(user_in_repo.id, user_in_repo.is_admin)

    def get_user_from_token(self, token: str, is_admin_required: bool) -> UserTokenData:
        """Decodes token and returns user from it.

        If `is_admin_required` is True check if user is admin.
        """

        user_token_data = self.decode_access_token(token, self._jwt_config)
        if is_admin_required and not user_token_data.is_admin:
            raise AccessForbiddenError
        return user_token_data

    def _create_user_token(self, user_id: uuid.UUID, is_admin: bool) -> UserToken:
        timestamp = int(datetime.datetime.now().timestamp())
        config = self._jwt_config
        access_token = self.create_access_token(
            user=UserTokenData(id=user_id, is_admin=is_admin),
            timestamp=timestamp,
            config=config,
        )
        return UserToken(
            access_token=access_token, token_type="Bearer", expires_in=config.expires_in
        )
