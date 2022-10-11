from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


class KafkaSettings(MainSettings):
    kafka_host: str = Field('127.0.0.1', env='KAFKA_HOST')
    kafka_port: int = 29092


class EtlSettings(MainSettings):
    batch_size: int = Field(10, env='BATCH_SIZE')


class ClickhouseSettings(MainSettings):
    host: str = Field('127.0.0.1', env='CLICKHOUSE_HOST')


kafka_settings = KafkaSettings()
etl_settings = EtlSettings()
clickhouse_settings = ClickhouseSettings()
