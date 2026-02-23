"""Contest Value Objects"""
from enum import Enum


class ContestFormat(str, Enum):
    ROUND_ROBIN = "ROUND_ROBIN"
    SINGLE_ELIMINATION = "SINGLE_ELIMINATION"


class ContestStatus(str, Enum):
    PRE_REGISTRATION = "PRE_REGISTRATION"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class InvalidStatusTransitionError(Exception):
    def __init__(self, current: ContestStatus, next_status: ContestStatus) -> None:
        super().__init__(
            f"Cannot transition from {current.value} to {next_status.value}"
        )


VALID_TRANSITIONS: dict[ContestStatus, set[ContestStatus]] = {
    ContestStatus.PRE_REGISTRATION: {ContestStatus.IN_PROGRESS},
    ContestStatus.IN_PROGRESS: {ContestStatus.COMPLETED},
    ContestStatus.COMPLETED: set(),
}


def validate_status_transition(
    current: ContestStatus, next_status: ContestStatus
) -> None:
    allowed = VALID_TRANSITIONS.get(current, set())
    if next_status not in allowed:
        raise InvalidStatusTransitionError(current, next_status)


def validate_best_of(best_of: int) -> None:
    if best_of <= 0:
        raise ValueError(f"best_of must be a positive integer, got {best_of}")
    if best_of % 2 == 0:
        raise ValueError(f"best_of must be an odd number, got {best_of}")
