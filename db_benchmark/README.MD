# Benchmark Vertica VS Clickhouse

## Virtual machine config with Databases

* Platform Intel Ice Lake
* vCPU 100%
* vCPU 2 Core
* RAM 8 ГБ
* SSD 30 ГБ

## DB Configuration:
* Vertica Single Node 
* Clickhouse Single Node 
* Clickhouse Cluster 4 Node Dictributed Table


## DB Schema:
Table metrics (
    event_time DateTime, 
    user_id UUID, 
    movie_id String, 
    viewed_frame Int64) 
    Order by user_id, movie_id
    Partitions by DAY

## Test data:
unique User_id = 200 000
unique movie_id = 5 000
time interval = '2022-01-01' - '2022-02-01'
Count of records = 10 000 000

## Conclusion:
Vertical cons:
1) Blocked for Russia
2) Needs a lot of resources: test for 50 simultaneous queries was failed: "Insufficient resources to execute plan on pool general"
3) Process query time dramatic upper than Clickhouse on the same configuration.
4) SQL syntacs more difficult than ClickHouse

ClickHouse pros:
1) Needs less hardware
2) Read/Write speed much more upper 
3) Distributed under the Apache License 2.0: Commercial Use and Private Use

## Results (seconds):

|   | VERTICA | CLICKHOUSE CLUSTER | CLICKHOUSE SINGLE NODE|
|  :--- |  :---: |  :---: |  :---: |
| **Read/Write threads** | **25/1** | **50/1** | **50/1** |
| Read all movies watched by user  |  52.44688866676579  | 0.23722820949554443| 8.595622915744785|
| Read 10 last watched movies by user  | 22.783136248372802  | 0.32258679771423354| 9.576598540782927|
| Read 10 the most popular movies  | 38.30867340821886   | 23.087147801399247 | 21.673601531505586|
| Read last watched movies  | 109.66096787877827 | 20.13218543495411 | 17.666613566141038|
| Write record  |  0.2695156973621524  | 0.06829080141690604| 0.029419162049572727|

