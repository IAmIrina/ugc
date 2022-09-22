import csv
import os
import time
import uuid
from datetime import datetime
from random import randint

COUNT_OF_USERS = 200000
COUNT_OF_MOVIES = 5000
COUNT_OF_RECORDS = 10000000
BATCH_SIZE = 100000

MAX_MOVIE_DURATION_FRAMES = 10800
START_DATE = '2022-01-01'
STOP_DATE = '2022-02-01'
START_TIME_INTERVAL = time.mktime(datetime.strptime(START_DATE, "%Y-%d-%m").timetuple())
STOP_TIME_INTERVAL = time.mktime(datetime.strptime(STOP_DATE, "%Y-%d-%m").timetuple())

DATA_FILE = os.getenv('LOCAL_CSV_FILE', 'src/data/frames.csv')

users = [str(uuid.uuid4()) for _ in range(COUNT_OF_USERS)]

movies = list({f"{'tt'}{randint(100000, 999999)}" for _ in range(COUNT_OF_MOVIES)})

max_user_idx = len(users) - 1
max_movies_idx = len(movies) - 1

try:
    os.remove(DATA_FILE)
except OSError:
    pass

for batch_num in range(0, COUNT_OF_RECORDS // BATCH_SIZE):
    batch = []
    for i in range(0, BATCH_SIZE):
        row = {
            'event_time': str(randint(START_TIME_INTERVAL, STOP_TIME_INTERVAL)),
            'user_id': users[randint(0, max_user_idx)],
            'movie_id': movies[randint(0, max_movies_idx)],
            'viewed_frame': str(randint(1, MAX_MOVIE_DURATION_FRAMES)),
        }
        batch.append(row.values())
    print(batch_num)
    with open(DATA_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(batch)
