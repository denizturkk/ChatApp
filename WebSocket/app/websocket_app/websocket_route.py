
from fastapi import WebSocket
from .connection_manager import ConnectionManager
from app.message_broker.kafka_producer import KafkaProducer
import json

manager = ConnectionManager()
kafka_producer = KafkaProducer()  # Assuming KafkaProducer is implemented

async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Send message to Kafka
            kafka_producer.send_message('MessageChannel', message)

            # Broadcast or send to specific user
            if message["ReceiverId"] == 1:
                await manager.broadcast(data)
            else:
                await manager.send_personal_message(data, message["ReceiverId"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(user_id)
