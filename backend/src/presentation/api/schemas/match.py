"""Match Pydantic スキーマ"""
from uuid import UUID

from pydantic import BaseModel

from src.domain.match.value_objects import MatchStatus


class MatchCreate(BaseModel):
    player1_id: UUID
    player2_id: UUID
    round: int | None = None
    match_order: int = 1


class MatchResultUpdate(BaseModel):
    player1_character: str | None = None
    player2_character: str | None = None
    player1_wins: int
    player2_wins: int
    comment: str | None = None


class MatchResponse(BaseModel):
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
