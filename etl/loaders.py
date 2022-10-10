from utils import backoff
from models import ConsumedMessage
from clickhouse_driver import Client

from settings import clickhouse_settings


@backoff()
def clickhouse_connect():
    return Client(host=clickhouse_settings.host)


@backoff()
def load_data_to_clickhouse(batch: list[ConsumedMessage], clickhouse_client: Client) -> None:
    """Загружает список сообщений в Clickhouse."""
    # Формируем данные для вставки
    inserting_data = []
    for message in batch:
        inserting_data.append(
            [
                round(message.posted_at.timestamp()),
                message.user_id,
                message.movie_id,
                message.movie_sec,
            ],
        )
    # Вставляем данные
    sql = 'INSERT INTO default.metrics (event_time, user_id, movie_id, viewed_frame) VALUES'
    clickhouse_client.execute(sql, inserting_data)
