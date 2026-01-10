from datetime import timedelta
from enum import Enum

class CircleRole:
    Owner: int = 3
    Admin: int = 2
    Moderator: int = 1
    Member: int = 0


class MuteDuration(Enum):
    ONE_HOUR = timedelta(hours=1)
    SIX_HOURS = timedelta(hours=6)
    ONE_DAY = timedelta(days=1)
    THREE_DAYS = timedelta(days=3)
    SEVEN_DAYS = timedelta(days=7)
