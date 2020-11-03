from datetime import date
from dataclasses import dataclass
from typing import List

from domain.price import Price


@dataclass
class Operation:
    to_create: List[Price] = None
    to_delete: List[Price] = None
    to_modify: List[Price] = None
