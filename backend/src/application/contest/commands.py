"""Contest コマンド"""
from dataclasses import dataclass
from uuid import UUID

from src.domain.contest.value_objects import ContestFormat, ContestStatus


@dataclass(frozen=True)
class CreateContestCommand:
    name: str
    game_title_id: UUID
    format: ContestFormat
    best_of: int


@dataclass(frozen=True)
class UpdateContestStatusCommand:
    contest_id: UUID
    new_status: ContestStatus


@dataclass(frozen=True)
class AddPlayerCommand:
    contest_id: UUID
    name: str
    seed: int | None


@dataclass(frozen=True)
class RemovePlayerCommand:
    contest_id: UUID
    player_id: UUID
