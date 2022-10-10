import os
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING


class Settings(BaseSettings):
    project_name: str = 'UGC films events'
    ugc_default_topic: str = 'views'
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'
    kafka_host: str = 'kafka'
    kafka_port: int = 9092

    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
abspath = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(abspath))
