# Проектная работа 8 спринта

Ссылка на репо: https://github.com/IAmIrina

## API сервиса
API сервиса можно найти по адресу http://localhost:8002/api/openapi

## Авторизация
Эндпоинты в сервисе защищены через JWT токены.

Тело токена (пример)
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
## Запуск проекта
Для запуска проекта
1. Создайте файл **.env** (используйте образец **.env.example**)
2. Запустите docker-compose
```commandline
docker-compose -f docker-compose.dev.yml up --build
```
Дождитесь, пока скачаются образы и запустятся контейнеры.

## Бенчмарк OLAP баз данных
Смотрите Ридми в папке ./db_benchmark/

## UML
В папке ./uml/ хранится plantUML, описываюший структуру UGC сервиса и всего проекта Movies.

### Приложение Movies (To Be)
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/tobe.png?raw=true)

### Приложение Movies (As Is)
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/asis.png?raw=true)

### Детальная схема UGC
![alt text](https://github.com/IAmIrina/ugc/blob/main/uml/images/ugc_detailed.png?raw=true)

