# /app_delivery/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@actual_pr678-rabbitmq-1:5672/"
    postgres_url: str = "postgresql://postgres:password@actual_pr678-postgres-delivery-1:5432/delivery"
    # 172.22.0.3:5432


settings = Settings()
