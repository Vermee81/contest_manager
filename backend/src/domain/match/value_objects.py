"""Match Value Objects"""
from enum import Enum


class MatchStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
