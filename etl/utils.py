import json
import datetime as dt
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def bytes_to_dict_deserializer(record: bytes) -> dict:
    """Используется для десериализации данных из формата bytes в формат dict."""
    decoded_record = json.loads(record.decode('utf-8'))
    if decoded_record.get('posted_at'):
        decoded_record['posted_at'] = dt.datetime.strptime(decoded_record['posted_at'], '%Y-%m-%dT%H:%M:%S.%f')
    return decoded_record


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Функция для повторного выполнения функции через некоторое время, если возникла ошибка."""

    def func_wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            next_sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.debug('Connection error. Use Backoff_________________________________________________')
                    logging.debug(e)
                    time.sleep(next_sleep_time)
                    if next_sleep_time >= border_sleep_time:
                        next_sleep_time = border_sleep_time
                    else:
                        next_sleep_time *= factor

        return inner

    return func_wrapper
