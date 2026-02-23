"""Player エンティティ"""
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Player:
    player_id: UUID
    contest_id: UUID
    name: str
    seed: int | None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name must not be empty")
        if self.seed is not None and self.seed <= 0:
            raise ValueError(f"seed must be a positive integer, got {self.seed}")
