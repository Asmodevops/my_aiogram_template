from environs import Env
from pydantic import BaseModel, SecretStr, PostgresDsn, NatsDsn


class TgBot(BaseModel):
    token: SecretStr
    throttling_time: float


class PgDB(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class BasicIds(BaseModel):
    admin_id: int
    admin_chat_id: int


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    password: SecretStr


class NatsConfig(BaseModel):
    server: NatsDsn


class DelayedConsumer(BaseModel):
    subject: str
    stream: str
    durable: str


class Config(BaseModel):
    pg_db: PgDB
    tg_bot: TgBot
    basic_ids: BasicIds
    redis: RedisConfig
    nats: NatsConfig
    delayed_consumer: DelayedConsumer

    @classmethod
    def load_config(cls, path: str | None = None) -> "Config":
        env = Env()
        env.read_env(path)
        return cls(
            tg_bot=TgBot(
                token=SecretStr(env.str("BOT_TOKEN")),
                throttling_time=env.float("THROTTLING_TIME"),
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
            basic_ids=BasicIds(
                admin_id=env.int("ADMIN_ID"),
                admin_chat_id=env.int("ADMINS_CHAT"),
            ),
            redis=RedisConfig(
                host=env.str("REDIS_HOST"),
                port=env.int("REDIS_PORT"),
                db=env.int("REDIS_DB"),
                password=SecretStr(env.str("REDIS_PASSWORD")),
            ),
            nats=NatsConfig(
                server=NatsDsn.build(
                    scheme="nats",
                    host=env.str("NATS_HOST"),
                    port=env.int("NATS_PORT"),
                    username=env.str("NATS_USER"),
                    password=env.str("NATS_PASSWORD")
                )
            ),
            delayed_consumer=DelayedConsumer(
                subject=env.str("DELAYED_CONSUMER_SUBJECT"),
                stream=env.str("DELAYED_CONSUMER_STREAM"),
                durable=env.str("DELAYED_CONSUMER_DURABLE_NAME"),
            )
        )

config: Config = Config.load_config()
