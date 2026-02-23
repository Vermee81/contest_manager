"""Match クエリ"""
from dataclasses import dataclass
from uuid import UUID

from src.domain.match.value_objects import MatchStatus


@dataclass(frozen=True)
class GetMatchesQuery:
    contest_id: UUID


@dataclass(frozen=True)
class MatchDTO:
    match_id: UUID
    contest_id: UUID
    player1_id: UUID
    player2_id: UUID
    player1_character: str | None
    player2_character: str | None
    player1_wins: int
    player2_wins: int
    comment: str | None
    status: MatchStatus
    round: int | None
    match_order: int
