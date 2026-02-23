"""GameTitle リポジトリインターフェース"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.game_title.game_title import GameTitle


class GameTitleRepository(ABC):
    @abstractmethod
    async def save(self, game_title: GameTitle) -> None: ...

    @abstractmethod
    async def find_by_id(self, game_title_id: UUID) -> GameTitle | None: ...

    @abstractmethod
    async def find_all(self) -> list[GameTitle]: ...
