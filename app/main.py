import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1 import events, grades, bookmarks, reviews
from src.core.config import settings
from src.db import kafka, mongo

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=settings.sentry_traces_sample_rate,
)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
)


@app.on_event('startup')
async def startup():
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}')
    await kafka.kafka.start()

    MONGODB_URL = "mongodb://localhost:27017/myFirstDatabase"
    mongo.mongo = AsyncIOMotorClient(MONGODB_URL)


@app.on_event('shutdown')
async def shutdown():
    await kafka.kafka.stop()


app.include_router(events.router, prefix='/ugc/v1/events', tags=['events'])
app.include_router(grades.router, prefix='/ugc/v1/grades', tags=['grades'])
app.include_router(bookmarks.router, prefix='/ugc/v1/bookmarks', tags=['bookmarks'])
app.include_router(reviews.router, prefix='/ugc/v1/reviews', tags=['reviews'])

if __name__ == '__main__':
    port = 8000
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=port,
    )
