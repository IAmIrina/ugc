# Project work "UGC for Online cinema". 
Yandex Praktikum: 8 sprint, teamwork.

## DB Benchmark OLAP DB
  Before developing of the service,  to choose storage for UGC we made DB benchmark.  db_benchmark folder contains source code of the benchmark for Clickhouse claster and Vertica. The result showed us that Clickhouse is more suitable for the our task.
  [The result of the benchmark](https://github.com/IAmIrina/ugc/blob/main/db_benchmark/README.MD)


## Stack
- ClickHouse
- Kafka
- ELK
- Sentry
- FastAPI

## API сервиса
API of the service http://localhost:8002/api/openapi

## Authorization

We use JWT to protect endpoints.

Token body (example)
```
{
  "sub": "16168708-f1c0-4767-9b6d-8601d396fd91",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 2000000000,
  "roles": [
    "Standart"
  ]
}
```
## Deploy

1. Create file **.env** (use example **.env.example**)
2. Run docker-compose
```commandline
docker-compose -f docker-compose.dev.yml up --build
```

## UML
uml folder contains plantUML which describes the structure of the UGC service and the whole Movies project.

### APP Movies (To Be)
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/tobe.png?raw=true)

### APP Movies (As Is)
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/asis.png?raw=true)

### UGC figure
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/ugc_detailed.png?raw=true)

