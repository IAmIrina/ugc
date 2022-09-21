from clickhouse_driver import Client
from utils.timers import timer
from utils.backoff import backoff
import logging
from settings.config import settings


@backoff()
def connect():
    client = Client(host=settings.clickhouse.host)
    count = client.execute('Select count (*) FROM default.metrics LIMIT 1')[0][0]
    if count < 10000000:
        logging.info('Datacount less than minimum number')
        raise
    return client


class DataInfo:

    def __init__(self):
        self.client = connect()
        self.record_count = self.count_of_record()
        self.user_id = self.get_user_id()
        self.movie_id = self.get_movie_id()

    def get_user_id(self):
        return self.client.execute('Select user_id FROM default.metrics LIMIT 1')[0][0]

    def get_movie_id(self):
        return self.client.execute('Select movie_id FROM default.metrics LIMIT 1')[0][0]

    def count_of_record(self):
        return self.client.execute('Select count (*) FROM default.metrics LIMIT 1')[0][0]

    def get_data(self):
        return self.record_count, self.user_id, self.movie_id


class BenchmarkRead:

    def __init__(self, user_id, movie_id, limit):
        self.client = connect()
        self.user_id = user_id
        self.movie_id = movie_id
        self.limit = limit

    @timer
    def movies_by_user(self):
        self.client.execute(
            "Select count(movie_id) FROM default.metrics where user_id=%(user_id)s",
            {'user_id': self.user_id}
        )

    @timer
    def last_watched_movies_by_user(self):
        self.client.execute(
            """Select DISTINCT(movie_id) as popularity
            FROM default.metrics where user_id=%(user_id)s ORDER BY event_time DESC LIMIT %(limit)s""",
            {'user_id': self.user_id, 'limit': self.limit}

        )

    @timer
    def most_popular_movies(self):
        self.client.execute(
            """Select movie_id, count(user_id) as popularity
            FROM default.metrics GROUP BY movie_id ORDER BY popularity DESC LIMIT %(limit)s;""",
            {'limit': self.limit}
        )

    @timer
    def last_watched_movies(self):
        self.client.execute(
            "Select DISTINCT(movie_id) FROM default.metrics ORDER BY event_time DESC LIMIT %(limit)s;",
            {'limit': self.limit}
        )


class BenchmarkWrite:
    def __init__(self):
        self.client = connect()

    @timer
    def write_record(self, row):
        self.client.execute(
            """INSERT INTO default.metrics
                (event_time, user_id, movie_id, viewed_frame)
                VALUES
                (%(event_time)s, %(user_id)s, %(movie_id)s, %(viewed_frame)s)""",
            dict(
                event_time=row[0],
                user_id=row[1],
                movie_id=row[2],
                viewed_frame=row[3],
            )
        )
