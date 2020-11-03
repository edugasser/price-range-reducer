class PriceRangeUnifier:

    def execute(self, prices):
        if not prices:
            return []

        prices = sorted(prices)

        previous_price = prices[0]
        start_date_range = prices[0].start
        to_unify = False

        for price in prices[1:]:
            if previous_price.is_possible_to_unify(price):
                to_unify = True
            else:
                if to_unify:
                    yield start_date_range, previous_price.end, previous_price.price # noqa
                start_date_range = price.start
                to_unify = False
            previous_price = price

        if to_unify:
            yield start_date_range, previous_price.end, previous_price.price
