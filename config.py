from pydantic  import BaseSettings


class Settings(BaseSettings):
    """Загрузка переменных конфигурации из .env"""
    DB_HOST: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
