import logging

import vertica_python

from utils.backoff import backoff
from utils.timers import timer


@backoff()
def copy_csv_data(connection_params):
    connection = vertica_python.connect(**connection_params)
    cursor = connection.cursor('dict')
    cursor.execute("""
    CREATE TABLE  IF NOT EXISTS metrics (
        event_time TIMESTAMP NOT NULL,
        user_id UUID NOT NULL,
        movie_id VARCHAR(256) NOT NULL,
        viewed_frame INTEGER NOT NULL
    )
    ORDER BY user_id, movie_id
    PARTITION BY ((DATE_PART('DAY', event_time))::int);
    """)

    cursor.execute("""
    SELECT count(*) as count_of_records FROM metrics;
    """)
    row = cursor.fetchone()
    print(row)
    if (row['count_of_records']) < 10000000:
        cursor.execute("""TRUNCATE TABLE metrics""")
        logging.info('Copy data to Vertica from csv')
        cursor.execute("COPY metrics(unix_timestamp FILLER VARCHAR(15), event_time as TO_TIMESTAMP(unix_timestamp), user_id, movie_id, viewed_frame) FROM"
                       " '/etc/benchmark_data/frames.csv' DELIMITER ','"
                       " REJECTED DATA '/home/dbadmin/rejects.txt'"
                       " EXCEPTIONS '/home/dbadmin/exceptions.txt'",
                       buffer_size=65536
                       )
        logging.info('Data coping is finished.')
    connection.close()


class DataInfo:

    def __init__(self, connection_params):
        copy_csv_data(connection_params)
        self.connection = vertica_python.connect(**connection_params)
        self.client = self.connection.cursor('dict')
        self.record_count = self.count_of_record()
        self.user_id = self.get_user_id()
        self.movie_id = self.get_movie_id()

    def __del__(self):
        self.connection.close()

    def get_user_id(self):
        user = self.client.execute('Select user_id FROM metrics LIMIT 1').fetchone()
        print(user)
        return user['user_id']

    def get_movie_id(self):
        movie = self.client.execute('Select movie_id FROM metrics LIMIT 1').fetchone()
        return movie['movie_id']

    def count_of_record(self):
        records = self.client.execute('Select count (*) as count_of_records FROM metrics LIMIT 1').fetchone()
        return records['count_of_records']

    def get_data(self):
        return self.record_count, self.user_id, self.movie_id


class BenchmarkRead:

    def __init__(self, connection_params, user_id, movie_id, limit):
        self.connection = vertica_python.connect(**connection_params)
        self.client = self.connection.cursor('dict')
        self.movie_id = movie_id
        self.user_id = user_id
        self.limit = limit

    @timer
    def movies_by_user(self):
        self.client.execute(
            "Select count(movie_id) FROM metrics where user_id=:user_id",
            {'user_id': self.user_id}
        )

    @timer
    def last_watched_movies_by_user(self):
        self.client.execute(
            "Select DISTINCT(movie_id) as popularity, event_time FROM metrics where user_id=:user_id ORDER BY event_time DESC LIMIT :limit",
            {'user_id': self.user_id, 'limit': self.limit}

        )

    @timer
    def most_popular_movies(self):
        self.client.execute(
            "Select movie_id, count(user_id) as popularity FROM metrics GROUP BY movie_id ORDER BY popularity DESC LIMIT :limit;",
            {'limit': self.limit}
        )

    @timer
    def last_watched_movies(self):
        self.client.execute(
            "Select DISTINCT(movie_id), event_time FROM metrics ORDER BY event_time DESC LIMIT :limit;",
            {'limit': self.limit}
        )


class BenchmarkWrite:
    def __init__(self, connection_params):
        self.connection = vertica_python.connect(**connection_params)
        self.client = self.connection.cursor('dict')

    @timer
    def write_record(self, row):
        self.client.execute(
            """INSERT INTO metrics
                (event_time, user_id, movie_id, viewed_frame)
                VALUES
                (TO_TIMESTAMP(:event_time), :user_id, :movie_id, :viewed_frame)""",
            dict(
                event_time=row[0],
                user_id=row[1],
                movie_id=row[2],
                viewed_frame=row[3],
            )
        )
