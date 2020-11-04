import pytest
import os
import sys
import dataclasses

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
from Domain.PriceRange import PriceRange
from Application.price_range_operations import PriceRangeOperations


@pytest.fixture(scope="function")
def first():
    return PriceRange(
        id=1,
        room="doble",
        rate="estandar",
        start=date(2025, 1, 1),
        end=date(2025, 1, 3),
        price=100,
    )


@pytest.fixture(scope="function")
def second():
    return PriceRange(
        id=1,
        room="doble",
        rate="estandar",
        start=date(2025, 1, 3),
        end=date(2025, 1, 5),
        price=200,
    )


@pytest.fixture(scope="function")
def third():
    return PriceRange(
        id=1,
        room="doble",
        rate="estandar",
        start=date(2025, 1, 5),
        end=date(2025, 1, 7),
        price=300,
    )


class TestMultipleRanges:

    def test_same_dates(self, first, second):
        u"""
        current: --1-1-2-2--
        given:   --3-3-3-3--
        """
        # Given
        new_price = dataclasses.replace(
            first,
            id=None,
            start=first.start,
            end=second.end,
            price=333
        )
        current_prices = [first, second]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = [
            new_price
        ]

        assert operations.to_create == to_create
        assert operations.to_modify is None
        assert operations.to_delete == current_prices

    def test_different_dates(self, first, second):
        """
        current: --1-1-2-2--
        given:   ----3-3-3--
        """
        # Given
        new_price = dataclasses.replace(
            first,
            id=None,
            start=first.start + timedelta(days=1),
            end=second.end,
            price=333
        )
        current_prices = [first, second]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = [
            new_price,
            dataclasses.replace(first, id=None, end=new_price.start)
        ]

        assert sorted(operations.to_create) == sorted(to_create)
        assert operations.to_modify is None
        assert operations.to_delete == current_prices

    def test_different_dates2(self, first, second):
        """
        current: --1-1-2-2--
        given:   3-3-3-3-3--
        """
        # Given
        new_price = dataclasses.replace(
            first,
            id=None,
            start=first.start - timedelta(days=1),
            end=second.end,
            price=333
        )
        current_prices = [first, second]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = [
            new_price
        ]

        assert operations.to_create == to_create
        assert operations.to_modify is None
        assert operations.to_delete == current_prices

    def test_different_dates3(self, first, second):
        """
        current: --1-1-2-2--
        given:   --3-3-3----
        """
        # Given
        new_price = dataclasses.replace(
            first,
            id=None,
            start=first.start,
            end=second.end - timedelta(days=1),
            price=333
        )
        current_prices = [first, second]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = [
            new_price,
            dataclasses.replace(second, id=None, start=new_price.end)
        ]

        assert sorted(operations.to_create) == sorted(to_create)
        assert operations.to_modify is None
        assert operations.to_delete == current_prices

    def test_process_different_price_and_dates_three_ranges(self, first, second, third):  # noqa
        """
        current: --1-1-2-2-3-3
        given:   ----4-4-4-4--
        """
        # Given
        new_price = dataclasses.replace(
            first,
            id=None,
            price=999,
            start=first.start + timedelta(days=1),
            end=third.end - timedelta(days=1)
        )
        current_prices = [first, second, third]

        # When
        operations = PriceRangeOperations.execute(new_price, current_prices)

        # Then
        to_create = sorted([
            new_price,
            dataclasses.replace(first, id=None, end=new_price.start),
            dataclasses.replace(third, id=None, start=new_price.end),
        ])

        assert sorted(operations.to_create) == to_create
        assert operations.to_modify is None
        assert operations.to_delete == current_prices
