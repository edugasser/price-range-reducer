from datetime import date
from dataclasses import dataclass


@dataclass
class Price:
    id: int
    room: str
    rate: str
    start: date
    # NOTE: end date not included.
    end: date
    price: float

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
            self.room == other_price.room and
            self.rate == other_price.rate
        )
