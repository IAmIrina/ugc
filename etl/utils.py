import json
import datetime as dt


def bytes_to_dict_deserializer(record: bytes) -> dict:
    """Используется для десериализации данных из формата bytes в формат dict"""
    decoded_record = json.loads(record.decode('utf-8'))
    if decoded_record.get('posted_at'):
        decoded_record["posted_at"] = dt.datetime.strptime(decoded_record["posted_at"], "%Y-%m-%dT%H:%M:%S.%f")
    return decoded_record
