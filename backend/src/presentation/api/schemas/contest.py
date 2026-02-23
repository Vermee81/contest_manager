"""Contest Pydantic スキーマ"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.contest.value_objects import ContestFormat, ContestStatus


class PlayerCreate(BaseModel):
    name: str
    seed: int | None = None


class PlayerResponse(BaseModel):
    player_id: UUID
    contest_id: UUID
    name: str
    seed: int | None


class ContestCreate(BaseModel):
    name: str
    game_title_id: UUID
    format: ContestFormat
    best_of: int = 3


class ContestStatusUpdate(BaseModel):
    status: ContestStatus


class ContestResponse(BaseModel):
    contest_id: UUID
    name: str
    game_title_id: UUID
    format: ContestFormat
    best_of: int
    status: ContestStatus
    created_at: datetime
    players: list[PlayerResponse]
