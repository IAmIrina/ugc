
import csv
import threading

from schemas.results import ReadResults, average
from settings.config import settings
from settings.template import REPORT

lock = threading.Lock()


read_results = []
write_results = [{'write_time': 0}]


def benchmark_reading(BenchmarkRead, conn_params, user_id, movie_id):
    reader = BenchmarkRead(conn_params, user_id, movie_id, settings.limit)
    res = ReadResults()
    for _ in range(settings.read_itterations):
        res.user_movies.append(reader.movies_by_user())
        res.last_user_movies.append(reader.last_watched_movies_by_user())
        res.popular.append(reader.most_popular_movies())
        res.last_watched.append(reader.last_watched_movies())
    with lock:
        read_results.append(res.get_average())


def benchmark_writing(BenchmarkWrite, conn_params):
    writer = BenchmarkWrite(conn_params)
    res = []
    current_thread = threading.currentThread()
    with open(settings.data_file) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            if getattr(current_thread, "stop_writing", True):
                res.append(writer.write_record(row))
            else:
                break
    with lock:
        write_results.append({'write_time': sum(res) / len(res)})


def load(read_treads: int, count_write_threads: int, description, conn_params, datainfo, benchmark_write,
         benchmark_read):
    global read_results
    global write_results

    record_count, user_id, movie_id = datainfo(conn_params).get_data()

    read_results = []
    write_results = [{'write_time': 0}]

    write_threads = list()
    if count_write_threads > 0:
        for index in range(count_write_threads):
            writing_thread = threading.Thread(target=benchmark_writing, args=(benchmark_write, conn_params))
            write_threads.append(writing_thread)
            writing_thread.start()

    threads = list()
    for index in range(read_treads):
        x = threading.Thread(target=benchmark_reading, args=(benchmark_read, conn_params, user_id, movie_id))
        threads.append(x)
        x.start()

    for _, thread in enumerate(threads):
        thread.join()

    for _, thread in enumerate(write_threads):

        thread.stop_writing = False
        thread.join()

    read_time = average(read_results)
    write_time = average(write_results)
    report = REPORT.format(
        database=description,
        read_threads=read_treads,
        write_threads=count_write_threads,
        record_count=record_count,
        **read_time,
        **write_time,
    )

    print(report)
    return report
