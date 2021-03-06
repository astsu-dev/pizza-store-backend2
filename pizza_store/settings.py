from pydantic import BaseSettings


class Settings(BaseSettings):
    app_host: str = "localhost"
    app_port: int = 8000
    edgedb_dsn: str
    jwt_algorithm: str = "HS256"
    jwt_secret: str
    jwt_expires_in: int = 24 * 60 * 60  # 1 day


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
