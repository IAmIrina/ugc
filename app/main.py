import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import events
from src.core.config import settings
from src.db import kafka

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}')
    await kafka.kafka.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka.kafka.stop()


app.include_router(events.router, prefix='/ugc/v1/events', tags=['events'])

if __name__ == '__main__':
    port = 8000
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=port,
    )
