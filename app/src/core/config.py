import os
from logging import config as logging_config

from pydantic import BaseSettings

from app.src.core.logger import LOGGING


class MainSettings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


class ApiSettings(MainSettings):
    project_name: str = 'UGC films events'
    ugc_default_topic: str = 'views'
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'


class KafkaSettings(MainSettings):
    kafka_host: str = '127.0.0.1'
    kafka_port: int = 9092


kafka_settings = KafkaSettings()
api_settings = ApiSettings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
