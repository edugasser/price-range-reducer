import json
import random
from dataclasses import asdict
from datetime import date, timedelta
from src.Domain.PriceRange import Price


class EventPriceProducer(object):

    def __init__(self, producer, queue_topic):
        self.producer = producer
        self.queue_topic = queue_topic

    def get_prices(self):
        start = date.today()
        end = start + timedelta(days=30)
        room_rates = ["doble-estandar"]

        delta = timedelta(days=1)
        amount = 100
        while start <= end:

            if start.day % 6 == 0:
                amount = amount + random.randint(1, 10)

            price = Price(
                room_rates[0],
                start.strftime("%Y-%m-%d"),
                amount
            )

            print(price)
            yield asdict(price)

            start += delta

    def run(self):
        prices = self.get_prices()
        print("EventPriceProducer: sending")
        self.producer.send(self.queue_topic, value=json.dumps(list(prices)))

