import os
import sys
import dataclasses

import pytest

from price_range_unifier import PriceRangeUnifier

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
from domain.price import Price


@pytest.fixture(scope="function")
def price():
    return Price(
        id=1,
        room="doble",
        rate="estandar",
        start=date(2025, 1, 1),
        end=date(2025, 1, 5),
        price=100,
    )


class TestPriceRangeUnifier:

    def test_no_prices(self, price):
        to_create = PriceRangeUnifier().execute([])
        assert list(to_create) == []

    def test_no_prices_to_unify(self, price):
        prices = [
            price,
            dataclasses.replace(price, price=200),
            dataclasses.replace(price, price=300),
        ]
        to_create = PriceRangeUnifier().execute(prices)
        assert list(to_create) == []

    def test_no_prices_to_unify(self, price):
        """
        given: [(1->3) 100, (3 -> 5) 200]
        """
        prices = [
            price,
            dataclasses.replace(
                price,
                start=price.end,
                end=price.end + timedelta(days=2),
                price=200
            )
        ]
        to_create = PriceRangeUnifier().execute(prices)
        assert list(to_create) == []

    def test_unify_the_two_first_prices(self, price):
        """
        given: [(1->3) 100, (3 -> 5) 100]
        """
        prices = [
            price,
            dataclasses.replace(
                price,
                start=price.end,
                end=price.end + timedelta(days=2),
                price=100
            )
        ]
        to_create = sorted(list(PriceRangeUnifier().execute(prices)))
        expected = sorted([(price.start, prices[-1].end, 100)])

        assert to_create == expected

    def test_unify_the_two_last_prices(self, price):
        """
        given: [(1->3) 100, (3 -> 5) 200, (5-8) 200]
        """
        second = dataclasses.replace(
            price,
            start=price.end,
            end=price.end + timedelta(days=2),
            price=200
        )
        prices = [
            price,
            second,
            dataclasses.replace(
                price,
                start=second.end,
                end=second.end + timedelta(days=2),
                price=200
            )
        ]
        to_create = sorted(list(PriceRangeUnifier().execute(prices)))
        expected = [(second.start, prices[-1].end, 200)]

        assert to_create == expected

    def test_unconsecutive_prices_same_price(self, price):
        """
        given: [(1->3) 100, (4 -> 5) 100]
        """
        second = dataclasses.replace(
            price,
            start=price.end + timedelta(days=1),
            end=price.end + timedelta(days=2),
        )
        prices = [
            price,
            second
        ]

        to_create = list(PriceRangeUnifier().execute(prices))
        assert to_create == []

    def test_unify_two_ranges(self, price):
        """
        given: [(1->3) 100, (3 -> 5) 100, (5 -> 6) 200, (6 -> 7) 200]
        """
        second = dataclasses.replace(
            price,
            start=price.end,
            end=price.end + timedelta(days=2),
        )
        third = dataclasses.replace(
            price,
            start=second.end,
            end=second.end + timedelta(days=2),
            price=200
        )
        prices = [
            price,
            second,
            third,
            dataclasses.replace(
                third,
                start=third.end,
                end=third.end + timedelta(days=2),
                price=200
            )
        ]

        to_create = sorted(list(PriceRangeUnifier().execute(prices)))
        expected = sorted([
            (price.start, second.end, price.price),
            (third.start, prices[-1].end, third.price)
        ])

        assert to_create == expected
