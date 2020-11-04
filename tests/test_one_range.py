import pytest
import os
import sys
import dataclasses

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
from Domain.PriceRange import PriceRange
from Application.price_range_operations import PriceRangeOperations


@pytest.fixture(scope="function")
def price():
    return PriceRange(
        id=1,
        room="doble",
        rate="estandar",
        start=date(2025, 1, 1),
        end=date(2025, 1, 5),
        price=100,
    )


class TestOneRange:

    def test_no_intersected_ranges(self, price):
        current_prices = []
        operations = PriceRangeOperations.execute(price, current_prices)
        to_create = [price]

        assert operations.to_create == to_create
        assert operations.to_modify is None
        assert operations.to_delete is None

    def test_process_same_price_and_dates(self, price):
        """
        current: --1-1-1-1--
        given:   --1-1-1-1--
        """
        # Given
        existed_price = dataclasses.replace(price, id=123)
        current_prices = [existed_price]

        # When
        operations = PriceRangeOperations.execute(price, current_prices)

        # Then
        assert operations.to_create is None
        assert operations.to_modify is None
        assert operations.to_delete is None

    def test_process_same_dates_but_different_price(self, price):
        """
        current: --1-1-1-1--
        given:   --2-2-2-2--
        """
        # Given
        existed_price = dataclasses.replace(price, price=999)
        current_prices = [existed_price]

        # When
        operations = PriceRangeOperations.execute(price, current_prices)
        to_modify = [price]

        # Then
        assert operations.to_create is None
        assert operations.to_modify == to_modify
        assert operations.to_delete is None

    def test_process_same_price_but_different_dates(self, price):
        """
        current: --1-1-1-1--
        given:   ----1-1----
        """
        # Given
        new_price = dataclasses.replace(
            price,
            id=None,
            start=price.start + timedelta(days=1),
            end=price.end - timedelta(days=1)
        )
        current_prices = [price]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        assert operations.to_create is None
        assert operations.to_modify is None
        assert operations.to_delete is None

    def test_process_same_price_but_different_dates2(self, price):
        """
        current: ----1-1----
        given:   --1-1-1-1--
        """
        # Given
        new_price = dataclasses.replace(
            price,
            id=None,
            start=price.start - timedelta(days=1),
            end=price.end + timedelta(days=1)
        )
        current_prices = [price]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        price.start = new_price.start
        price.end = new_price.end
        assert operations.to_create is None
        assert operations.to_modify == [price]
        assert operations.to_delete is None

    def test_process_different_price_and_dates(self, price):
        """
        current: --1-1-1-1--
        given:   ----2-2----
        """
        # Given
        new_price = dataclasses.replace(
            price,
            id=None,
            price=999,
            start=price.start + timedelta(days=1),
            end=price.end - timedelta(days=1)
        )
        current_prices = [price]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = sorted([
            new_price,
            dataclasses.replace(price, id=None, end=new_price.start),
            dataclasses.replace(price, id=None, start=new_price.end),
        ])

        assert sorted(operations.to_create) == to_create
        assert operations.to_modify is None
        assert operations.to_delete == [price]

    def test_process_different_price_and_dates2(self, price):
        u"""
        current: -1-1-1-
        given:   ---2-2-
        """
        # Given
        new_price = dataclasses.replace(
            price,
            id=None,
            price=999,
            start=price.start + timedelta(days=1)
        )
        current_prices = [price]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = sorted([
            new_price,
            dataclasses.replace(price, id=None, end=new_price.start)
        ])

        assert sorted(operations.to_create) == to_create
        assert operations.to_modify is None
        assert operations.to_delete == [price]

    def test_process_different_price_and_dates3(self, price):
        u"""
        current: -1-1-1-
        given:   -2-2--
        """
        # Given
        new_price = dataclasses.replace(
            price,
            id=None,
            price=999,
            end=price.end - timedelta(days=1)
        )
        current_prices = [price]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = sorted([
            new_price,
            dataclasses.replace(price, id=None, start=new_price.end)
        ])

        assert sorted(operations.to_create) == to_create
        assert operations.to_modify is None
        assert operations.to_delete == [price]
