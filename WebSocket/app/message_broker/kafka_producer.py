from confluent_kafka import Producer
import json

class KafkaProducer:
    def __init__(self, servers='localhost:9092'):
        self.producer = Producer({'bootstrap.servers': servers})

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_message(self, topic, message):
        self.producer.produce(topic, json.dumps(message), callback=self.delivery_report)
        self.producer.flush()
