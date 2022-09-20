from clickhouse.readwrite import write_and_read
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # for i in range(1, 5):
    #     only_reading(i)

    for write in range(0, 2):
        for read in range(1, 6):
            write_and_read(read, write)
