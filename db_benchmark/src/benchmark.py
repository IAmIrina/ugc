from readwrite import write_and_read
import logging
import clickhouse.engine
import vertica.engine
from settings.config import settings

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    write_and_read(settings.read_threads,
                   settings.write_threads,
                   clickhouse.engine.DataInfo,
                   'CLICKHOUSE',
                   clickhouse.engine.BenchmarkWrite,
                   clickhouse.engine.BenchmarkRead)

    # write_and_read(settings.read_threads,
    #                settings.write_threads,
    #                vertica.engine.DataInfo,
    #                'VERTICA',
    #                vertica.engine.BenchmarkWrite,
    #                vertica.engine.BenchmarkRead)
