from models import ClickhouseModel, ConsumedMessage


async def load_data_to_clickhouse(batch: list[ConsumedMessage]) -> list[ClickhouseModel]:
    """Загружает список сообщений в Clickhouse"""



    return validated_models
