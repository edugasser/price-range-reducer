import json
from datetime import timedelta


class PriceRangeUnifier:
    ONE_DAY = timedelta(days=1)

    def __init__(self, producer, queue_topic):
        self.producer = producer
        self.queue_topic = queue_topic

    def unify(self, prices):
        prices = sorted(prices)

        previous_price = prices[0]
        start_date_range = prices[0].day

        for price in prices[1:]:
            if not price.is_possible_to_unify(previous_price):
                yield start_date_range, previous_price.day + self.ONE_DAY, previous_price.price  # noqa
                start_date_range = price.day

            previous_price = price

        yield start_date_range, previous_price.day + self.ONE_DAY, previous_price.price

    def execute(self, prices):
         if not prices:
            return []

         for price_range in self.unify(prices):
             print("PriceRangeUnifier sending {}".format(price_range))
             self.producer.send(
                 self.queue_topic,
                 value=json.dumps(price_range, default=str)
             )
