from pydantic import BaseSettings
from pathlib import Path
#path = Path(__file__).parent / "../data/test.csv"

# print(my_path)
# path = os.path.join(my_path, "../data/test.csv")


class Settings(BaseSettings):

    clickhouse: str = 'localhost'
    vertica: str = 'localhost'
    read_threads: int = 3
    write_threads: int = 2
    read_itterations: int = 5
    write_itterations: int = 5
    data_file: str = 'data/frames.csv'

    limit: int = 10


settings = Settings()
settings.data_file = str(Path(__file__).parent.parent / f'{settings.data_file}')
