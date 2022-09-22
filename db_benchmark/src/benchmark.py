import logging

import clickhouse.engine
import vertica.engine
from readwrite import load
from settings.config import settings

logging.basicConfig(level=logging.INFO)

tests = [
    (
        settings.read_threads,
        settings.write_threads,
        'CLICKHOUSE CLUSTER',
        settings.clickhouse_cluster,
        clickhouse.engine.DataInfo,
        clickhouse.engine.BenchmarkWrite,
        clickhouse.engine.BenchmarkRead
    ),
    (
        settings.read_threads,
        settings.write_threads,
        'CLICKHOUSE_SINGLE_NODE',
        settings.clickhouse_singlenode,
        clickhouse.engine.DataInfo,
        clickhouse.engine.BenchmarkWrite,
        clickhouse.engine.BenchmarkRead
    ),
    (
        settings.read_threads,
        settings.write_threads,
        'VERTICA',
        settings.vertica.dict(),
        vertica.engine.DataInfo,
        vertica.engine.BenchmarkWrite,
        vertica.engine.BenchmarkRead
    )
]


if __name__ == '__main__':

    results = []
    for test in tests:
        logging.info('Started: %s', test[3])
        results.append(load(*test))

    with open(settings.report_file, 'w') as f:
        f.write(''.join(results))
