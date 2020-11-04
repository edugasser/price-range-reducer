import json
import os
from datetime import datetime

from kafka import KafkaConsumer

from Application.PriceRangeOperations import PriceRangeOperations
from Application.PriceRangeUnifier import PriceRangeUnifier
from Domain.PriceRange import PriceRange

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
PRICE_TOPIC = os.environ.get("PRICE_RANGE_TOPIC", "queue.price_ranges")


consumer = KafkaConsumer(
    PRICE_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=json.loads,
)


def transform_prices(json_prices):
    for price in json.loads(json_prices):
        price["start"] = datetime.strptime(price["start"], '%Y-%m-%d')
        price["end"] = datetime.strptime(price["end"], '%Y-%m-%d')
        yield PriceRange(**price)


for message in consumer:
    price_range = transform_prices(message.value)
    # TODO: create a price pipeline processor
    # PriceRangeOperations().execute(price_range)
