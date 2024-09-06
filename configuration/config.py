from dataclasses import dataclass
from environs import Env


@dataclass(slots=True, frozen=True)
class TgBot:
    token: str
    bot_link: str
    admin_ids: list[int]
    channel_links: list[str]
    count_like_raffle: int


@dataclass(slots=True, frozen=True)
class ConfigBot:
    tg_bot: TgBot


def load_config_bot(path: str | None = None) -> ConfigBot:
    env = Env()
    env.read_env(path)
    return ConfigBot(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            bot_link=env('BOT_LINK'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            channel_links=list(map(str, env.list('CHANNEL_LINKS'))),
            count_like_raffle=int(env('COUNT_LIKE_RAFFLE'))
        )
    )


@dataclass(slots=True, frozen=True)
class DataBase:
    dsn: str
    is_echo: bool


@dataclass(slots=True, frozen=True)
class ConfigDB:
    database: DataBase


def load_config_db(path: str | None = None) -> ConfigDB:
    env = Env()
    env.read_env(path)
    return ConfigDB(
        database=DataBase(
            dsn=env('DSN'),
            is_echo=bool(env('IS_ECHO'))
        )
    )