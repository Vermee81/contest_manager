"""GameTitle エンティティ"""
from dataclasses import dataclass
from uuid import UUID


@dataclass
class GameTitle:
    game_title_id: UUID
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name must not be empty")
