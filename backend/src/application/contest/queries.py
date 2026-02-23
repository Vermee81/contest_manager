"""Contest クエリ"""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.contest.value_objects import ContestFormat, ContestStatus


@dataclass(frozen=True)
class GetContestQuery:
    contest_id: UUID


@dataclass(frozen=True)
class ListContestsQuery:
    pass


@dataclass(frozen=True)
class PlayerDTO:
    player_id: UUID
    contest_id: UUID
    name: str
    seed: int | None


@dataclass(frozen=True)
class ContestDTO:
    contest_id: UUID
    name: str
    game_title_id: UUID
    format: ContestFormat
    best_of: int
    status: ContestStatus
    created_at: datetime
    players: list[PlayerDTO]
