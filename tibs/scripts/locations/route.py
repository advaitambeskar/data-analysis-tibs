from dataclasses import dataclass
from collections import namedtuple

Hub = namedtuple("Hub", "id name lat lon")

@dataclass
class Route:
    start: Hub
    dest: Hub
    award: int