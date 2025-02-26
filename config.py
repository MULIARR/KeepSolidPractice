from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database_url: str

    @staticmethod
    def from_env(env: Env) -> "DatabaseConfig":
        """
        postgresql+asyncpg://{user}:{password}@{host}/{database}
        """

        host = env.str("DB_HOST")
        password = env.str("DB_PASSWORD")
        user = env.str("DB_USER")
        database = env.str("DB_NAME")
        port = env.int("DB_PORT", 5432)

        database_url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'

        return DatabaseConfig(database_url=database_url)


@dataclass
class AppConfig:
    server_url: str

    @staticmethod
    def from_env(env: Env) -> "AppConfig":
        server_url = env.str("SERVER_URL")

        return AppConfig(server_url=server_url)


@dataclass
class Config:
    db: DatabaseConfig
    app: AppConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DatabaseConfig.from_env(env),
        app=AppConfig.from_env(env),
    )


config = load_config(".env")
