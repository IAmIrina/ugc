from pydantic import BaseSettings
from pathlib import Path


class DotEnvMixin(BaseSettings):
    class Config:
        env_file = '.env'


class Vertica(DotEnvMixin):
    host: str = '10.129.0.21'
    port: int = 5433
    user: str = 'dbadmin'
    password: str = ''
    database: str = 'docker'
    autocommit: bool = True


class Clickhouse(DotEnvMixin):
    host: str = 'localhost'


def get_params(cls, env_prefix_name: str):
    class Params(cls):
        class Config:
            env_prefix = f'{env_prefix_name}_'
    return Params()


class Settings(DotEnvMixin):

    clickhouse: Clickhouse = get_params(Clickhouse, 'clickhouse')
    vertica: Vertica = get_params(Vertica, 'vertica')
    read_threads: int = 3
    write_threads: int = 1
    read_itterations: int = 10
    write_itterations: int = 10
    data_file: str = 'data/frames.csv'
    local_csv_file: str = '/etc/benchmark_data/frames.csv'

    limit: int = 10


settings = Settings()
settings.data_file = str(Path(__file__).parent.parent / f'{settings.data_file}')
