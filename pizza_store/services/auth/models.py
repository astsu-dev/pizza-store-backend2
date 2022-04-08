import uuid
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class UserCreate:
    username: str
    password: str


@dataclass(frozen=True)
class UserLogIn:
    username: str
    password: str


@dataclass(frozen=True)
class UserInRepoCreate:
    username: str
    password_hash: str
    is_admin: bool


@dataclass(frozen=True)
class UserCreated:
    id: uuid.UUID


@dataclass(frozen=True)
class User:
    id: uuid.UUID
    username: str
    password_hash: str
    is_admin: bool


@dataclass(frozen=True)
class UserTokenData:
    id: uuid.UUID
    is_admin: bool


@dataclass(frozen=True)
class UserToken:
    access_token: str
    token_type: Literal["Bearer"]
    expires_in: int


@dataclass(frozen=True)
class JWTConfig:
    algorithm: str
    secret: str
    expires_in: int
