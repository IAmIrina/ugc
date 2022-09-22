from pathlib import Path

from pydantic import BaseSettings


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
    host: str = 'localhost'  # '10.129.0.6'  # '10.129.0.9' - cluster


def get_params(cls, env_prefix_name: str):
    class Params(cls):
        class Config:
            env_prefix = f'{env_prefix_name}_'
    return Params()


class Settings(DotEnvMixin):

    clickhouse_singlenode: Clickhouse = get_params(Clickhouse, 'clickhouse_single')
    clickhouse_cluster: Clickhouse = get_params(Clickhouse, 'clickhouse_cluster')
    vertica: Vertica = get_params(Vertica, 'vertica')
    read_threads: int = 25
    write_threads: int = 1
    read_itterations: int = 5
    write_itterations: int = 5
    data_file: str = 'data/frames.csv'
    local_csv_file: str = '/etc/benchmark_data/frames.csv'
    report_file: str = 'report.txt'
    limit: int = 10


settings = Settings()
settings.data_file = str(Path(__file__).parent.parent / f'{settings.data_file}')
settings.report_file = str(Path(__file__).parent.parent / f'{settings.report_file}')
