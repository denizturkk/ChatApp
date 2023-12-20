from confluent_kafka import Consumer, KafkaError
import json
from ..crud.message_crud import create_message
from ..schemas.message_schema import MessageCreate
from app.db.database import SessionLocal

def consume_messages():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['MessageChannel'])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue

            # Decode the message and create a MessageCreate object
            message_data = json.loads(msg.value().decode('utf-8'))
            message_obj = MessageCreate(**message_data)

            # Use a new DB session for each message
            db = SessionLocal()
            try:
                create_message(db, message_obj)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error processing message: {e}")
            finally:
                db.close()

    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
    finally:
        consumer.close()
