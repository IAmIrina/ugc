from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


class KafkaSettings(MainSettings):
    kafka_host: str = Field("0.0.0.0", env='KAFKA_HOST')
    kafka_port: int = Field(9092, env='KAFKA_PORT')


kafka_settings = KafkaSettings()