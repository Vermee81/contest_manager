"""Standings クエリ"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetStandingsQuery:
    contest_id: UUID


@dataclass(frozen=True)
class StandingsEntryDTO:
    player_id: UUID
    player_name: str
    wins: int
    losses: int
    matches_played: int
    game_wins: int
    game_losses: int


@dataclass(frozen=True)
class StandingsDTO:
    contest_id: UUID
    entries: list[StandingsEntryDTO]
