import json
import os
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer

from src.Application.PriceRangeUnifier import PriceRangeUnifier
from src.Domain.PriceRange import Price

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
PRICE_TOPIC = os.environ.get("PRICE_TOPIC", "queue.prices")
PRICE_RANGE_TOPIC = os.environ.get("PRICE_RANGE_TOPIC", "queue.price_ranges")


consumer = KafkaConsumer(
    PRICE_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=json.loads,
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda value: json.dumps(value).encode()
)


def transform_prices(json_prices):
    for price in json.loads(json_prices):
        price["day"] = datetime.strptime(price["day"], '%Y-%m-%d')
        yield Price(**price)


for message in consumer:
    prices = transform_prices(message.value)
    PriceRangeUnifier(producer, PRICE_RANGE_TOPIC).execute(prices)
