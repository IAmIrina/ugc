# cat etc/clickhouse-server/init.ddl | clickhouse-client -nm
# 88628947-e235-4e97-8000-1550084c38fc
#from clickhouse_driver import Client
from clickhouse.engine import DataInfo, BenchmarkQueries, BenchmarkWrite
import threading
from clickhouse.template import REPORT
import logging
from clickhouse.schemas.results import ReadResults, average
from settings.config import settings


lock = threading.Lock()

DATABASE = 'CLICKHOUSE'


record_count, user_id, movie_id = DataInfo().get_data()

read_results = []
write_results = [{'write_time': 0}]


def benchmark_reading():
    reader = BenchmarkQueries(user_id, movie_id, settings.limit)
    res = ReadResults()
    for _ in range(settings.read_itterations):
        res.user_movies.append(reader.movies_by_user())
        res.last_user_movies.append(reader.last_watched_movies_by_user())
        res.popular.append(reader.most_popular_movies())
        res.last_watched.append(reader.last_watched_movies())
    with lock:
        read_results.append(res.get_average())


def benchmark_writing(iternal: bool = False):
    writer = BenchmarkWrite(source=settings.data_file)
    res = []
    if iternal:
        current_thread = threading.currentThread()
        while getattr(current_thread, "stop_writing", True):
            res.append(writer.write_records(limit=1))
    else:
        for _ in range(settings.write_itterations):
            res.append(writer.write_records(limit=1))
    with lock:
        write_results.append({'write_time': sum(res) / len(res)})


def write_and_read(read_treads: int, count_write_threads: int = 0):
    global read_results
    global write_results

    read_results = []
    write_results = [{'write_time': 0}]

    write_threads = list()
    if count_write_threads > 0:
        for index in range(count_write_threads):
            logging.info("Main    : create and start thread %d.", index)
            writing_thread = threading.Thread(target=benchmark_writing, args=(True,))
            write_threads.append(writing_thread)
            writing_thread.start()

    threads = list()
    for index in range(read_treads):
        x = threading.Thread(target=benchmark_reading, args=())
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

    for index, thread in enumerate(write_threads):

        thread.stop_writing = False
        thread.join()

    read_time = average(read_results)
    write_time = average(write_results)

    print(REPORT.format(
        database=DATABASE,
        read_threads=read_treads,
        write_threads=count_write_threads,
        record_count=record_count,
        **read_time,
        **write_time,
    ))
