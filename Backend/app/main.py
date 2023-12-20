from fastapi import FastAPI
from app.api.endpoints import user_api, message_api
from app.message_broker.kafka_consumer import consume_messages
import asyncio
import logging

app = FastAPI()

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

async def start_kafka_consumer():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, consume_messages)

app.add_event_handler("startup", start_kafka_consumer)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the ChatApp API"}

app.include_router(user_api.router)
app.include_router(message_api.router)
