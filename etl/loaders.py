from models import ConsumedMessage
from clickhouse_driver import Client

from settings import clickhouse_settings

def clickhouse_connect():
    client = Client(host=clickhouse_settings.host)

    return client

def load_data_to_clickhouse(batch: list[ConsumedMessage], clickhouse_client: Client) -> None:
    """Загружает список сообщений в Clickhouse"""
    # Формируем данные для вставки
    inserting_data = []
    for i, message in enumerate(batch):
        inserting_data.append(
            [
                round(message.posted_at.timestamp()),
                message.user_id,
                message.movie_id,
                message.movie_sec
             ])
    # Вставляем данные
    sql = f'''INSERT INTO default.metrics (event_time, user_id, movie_id, viewed_frame) VALUES'''
    clickhouse_client.execute(sql, inserting_data)

    return None
