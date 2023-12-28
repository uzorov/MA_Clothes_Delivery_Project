# /app_printing/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@actual_pr678-rabbitmq-1:5672/"
    postgres_url: str = "postgresql://postgres:password@actual_pr678-postgres-printing-1:5433/printing"
    # port: str = 81

    # model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
