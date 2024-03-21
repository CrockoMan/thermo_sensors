import os

from dotenv import load_dotenv
from dotenv.variables import Literal
from pydantic_settings import BaseSettings

load_dotenv()

MODE: str = os.getenv('MODE', 'DEV')
DB_HOST: str = os.getenv('DB_HOST', 'localhost')

class Settings(BaseSettings):
    """Загрузка переменных конфигурации из .env"""
    DB_HOST: str
    # MODE: Literal['DEV', 'PROD', 'TEST']
    # APPLICATION_MODE: str = 'DEV'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
