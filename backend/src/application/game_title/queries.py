"""GameTitle クエリ"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetGameTitlesQuery:
    pass


@dataclass(frozen=True)
class GetGameTitleQuery:
    game_title_id: UUID


@dataclass(frozen=True)
class GameTitleDTO:
    game_title_id: UUID
    name: str
