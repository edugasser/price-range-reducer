from datetime import date, timedelta
from dataclasses import dataclass


@dataclass
class Price:
    room_rate: str
    day: date
    price: float
    id: int = None

    def __lt__(self, other):
        return self.day < other.day

    def is_possible_to_unify(self, other_price):
        return (
            self.day == other_price.day + timedelta(days=1) and
            self.price == other_price.price and
            self.room_rate == other_price.room_rate
        )

@dataclass
class PriceRange:
    room_rate: str
    start: date
    # NOTE: end date not included.
    end: date
    price: float
    id: int = None

    def __lt__(self, other):
        return self.start < other.start

    def same_range(self, other_price):
        return (
            self.start == other_price.start and
            self.end == other_price.end
        )

    def is_wider(self, other_price):
        return (
            self.start < other_price.start or
            self.end > other_price.end
        )

    def is_possible_to_unify(self, other_price):
        return (
            self.end == other_price.start and
            self.price == other_price.price and
            self.room_rate == other_price.room_rate
        )
