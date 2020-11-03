import dataclasses
from typing import List
from domain.operation import Operation
from domain.price import Price


class PriceRangeOperations:

    @classmethod
    def execute(cls, new_price: Price, current_prices: List[Price]) -> Operation:  # noqa

        if not current_prices:
            result = Operation(to_create=[new_price])

        elif len(current_prices) == 1 and cls.same_range_or_price(current_prices[0], new_price):  # noqa
            result = cls.process_one_range(new_price, current_prices[0])

        else:
            first, last = current_prices[0], current_prices[-1]
            result = cls.process_different_price_and_range(
                first,
                last,
                new_price,
                current_prices
            )

        return result

    @staticmethod
    def same_range_or_price(current_price, new_price):
        return (
            new_price.same_range(current_price)
            or new_price.price == current_price.price
        )

    @classmethod
    def process_one_range(cls, new_price: Price, current_price: Price):
        same_price = current_price.price == new_price.price
        same_range = new_price.same_range(current_price)
        new_price_is_wider = new_price.is_wider(current_price)

        if (same_price and same_range) or (same_price and not new_price_is_wider):  # noqa
            result = Operation()
        elif not same_price and same_range:
            current_price.price = new_price.price
            result = Operation(to_modify=[current_price])
        elif same_price and new_price_is_wider:
            current_price.start = min(new_price.start, current_price.start)
            current_price.end = max(new_price.end, current_price.end)
            result = Operation(to_modify=[current_price])
        else:
            raise ValueError("Unsupported case!")

        return result

    @classmethod
    def process_different_price_and_range(
        cls,
        first,
        last,
        new_price,
        current_prices
    ):
        prices_to_create = []
        if first.start < new_price.start:
            if first.price != new_price.price:
                new_first = cls.split_start(first, new_price)
                prices_to_create.append(new_first)
            else:
                new_price.start = first.start

        if last.end > new_price.end:
            if last.price != new_price.price:
                new_end = cls.split_end(last, new_price)
                prices_to_create.append(new_end)
            else:
                new_price.end = last.end

        prices_to_create.append(new_price)
        result = Operation(
            to_create=prices_to_create,
            to_delete=current_prices
        )
        return result

    @staticmethod
    def split_start(start, new_price):
        return dataclasses.replace(start, id=None, end=new_price.start)

    @staticmethod
    def split_end(end, new_price):
        return dataclasses.replace(end, id=None, start=new_price.end)
