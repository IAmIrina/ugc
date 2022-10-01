# Проектная работа 8 спринта

Ссылка на репо: https://github.com/AlexRussianPyth/ugc_sprint_1

## API сервиса
API сервиса можно найти по адресу http://localhost:8002/api/openapi

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

