from pydantic import BaseModel, SecretStr, PostgresDsn
from environs import Env


class TgBot(BaseModel):
    token: SecretStr


class PgDB(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class BasicIds(BaseModel):
    admin_id: int


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int


class Config(BaseModel):
    pg_db: PgDB
    tg_bot: TgBot
    basic_ids: BasicIds
    redis: RedisConfig

    @classmethod
    def load_config(cls, path: str | None = None) -> "Config":
        env = Env()
        env.read_env(path)
        return cls(
            tg_bot=TgBot(
                token=SecretStr(env.str("BOT_TOKEN")),
            ),
            pg_db=PgDB(
                dsn=PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=env.str("POSTGRES_USER"),
                    password=env.str("POSTGRES_PASSWORD"),
                    host=env.str("DB_HOST"),
                    port=env.int("DB_PORT"),
                    path=env.str("POSTGRES_DB"),
                ),
                is_echo=env.bool("ECHO"),
            ),
            basic_ids=BasicIds(admin_id=env.int("ADMIN_ID")),
            redis=RedisConfig(
                host=env.str("REDIS_HOST"),
                port=env.int("REDIS_PORT"),
                db=env.int("REDIS_DB"),
            ),
        )
