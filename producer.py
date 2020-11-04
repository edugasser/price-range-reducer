import json
import os

from kafka import KafkaProducer
from Application.EventPriceProducer import EventPriceProducer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
PRICE_TOPIC = "queue.prices"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda value: json.dumps(value).encode()
)

p = EventPriceProducer(producer, PRICE_TOPIC)
p.run()

while True:
    pass
