# /app_printing/app/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Определяем путь к .env файлу относительно расположения settings.py
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Is .env file present: {os.path.isfile(env_path)}")
print(f"env_path: {env_path}")


class Settings(BaseSettings):
    amqp_url: str = os.getenv("AMQP_URL")
    print(f"\n\n AMQP_URL: {amqp_url}\n\n")

    postgres_url: str = os.getenv("POSTGRES_URL_ORDER")
    print(f"\n\n POSTGRES_URL: {postgres_url}\n\n")

    host_ip: str = os.getenv("HOST_IP")
    print(f"\n\n HOST_IP: {host_ip}\n\n")


settings = Settings()
