from dataclasses import dataclass
from typing import List

from src.Domain.PriceRange import PriceRange


@dataclass
class Operation:
    to_create: List[PriceRange] = None
    to_delete: List[PriceRange] = None
    to_modify: List[PriceRange] = None
