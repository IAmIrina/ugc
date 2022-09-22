# Тестирование Vertica VS Clickhouse

## Конфигурация Виртуальных машин на которых были подняты базы данных:

Платформа Intel Ice Lake
Гарантированная доля vCPU 100%
vCPU 2
RAM 8 ГБ
Объём дискового пространства 30 ГБ

## Конфигурации DB:
* Vertica Single Node 
* Clickhouse Single Node 
* Clickhouse Cluster 4 Node Dictributed Table


## Схема данных:
Таблица metrics (
    event_time DateTime, 
    user_id UUID, 
    movie_id String, 
    viewed_frame Int64) 
    Order by user_id, movie_id
    Partitions by DAY

## Данные для теста:
unique User_id = 200 000
unique movie_id = 5 000
time interval = '2022-01-01' - '2022-02-01'
Count of records = 10 000 000

## Заключение:
Недостатки Vertica:
1) Заблокирован для России
2) Требовательный к ресурсам: не прошел тест на 50 одновременных запросов - Insufficient resources to execute plan on pool general
3) Время обработки запросов драматически выше, чем Clickhouse в той же конфигурации 
3) SQL синтаксис сложнее, чем ClickHouse


На тестировании Clickhouse показал ряд преимущества:
1) менее требователь к аппаратному обеспечению 
2) Скорость чтения и записи данных на порядок выше
3) Распростаняется под лицензией Apache License 2.0:  Commercial use и  Private use 


## Результаты тестирования:

    VERTICA (10000000 records)
       Read threads: 25
       Write threads: 1
       ----------------------------------------------------------------------------
        Read all movies watched by user           52.44688866676579 
        Read 10 last watched movies by user       22.783136248372802 
        Read 10 the most popular movies           38.30867340821886 
        Read last watched movies                  109.66096787877827
       ----------------------------------------------------------------------------
        Write record                              0.2695156973621524
       ----------------------------------------------------------------------------

    CLICKHOUSE CLUSTER (10000000 records)
       Read threads: 50
       Write threads: 1
       ----------------------------------------------------------------------------
        Read all movies watched by user           0.23722820949554443 
        Read 10 last watched movies by user       0.32258679771423354 
        Read 10 the most popular movies           23.087147801399247 
        Read last watched movies                  20.13218543495411
       ----------------------------------------------------------------------------
        Write record                              0.06829080141690604
       ----------------------------------------------------------------------------
  
  
    CLICKHOUSE_SINGLE_NODE (10000000 records)
       Read threads: 50
       Write threads: 1
       ----------------------------------------------------------------------------
        Read all movies watched by user           8.595622915744785 
        Read 10 last watched movies by user       9.576598540782927 
        Read 10 the most popular movies           21.673601531505586 
        Read last watched movies                  17.666613566141038
       ----------------------------------------------------------------------------
        Write record                              0.029419162049572727
       ----------------------------------------------------------------------------



