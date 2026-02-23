"""Standings Pydantic スキーマ"""
from uuid import UUID

from pydantic import BaseModel


class StandingsEntryResponse(BaseModel):
    player_id: UUID
    player_name: str
    wins: int
    losses: int
    matches_played: int
    game_wins: int
    game_losses: int


class StandingsResponse(BaseModel):
    contest_id: UUID
    entries: list[StandingsEntryResponse]
