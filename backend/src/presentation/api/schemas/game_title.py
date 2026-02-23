"""GameTitle Pydantic スキーマ"""
from uuid import UUID

from pydantic import BaseModel


class GameTitleCreate(BaseModel):
    name: str


class GameTitleResponse(BaseModel):
    game_title_id: UUID
    name: str
