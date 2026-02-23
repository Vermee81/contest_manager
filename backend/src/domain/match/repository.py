"""Match リポジトリインターフェース"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.match.match import Match


class MatchRepository(ABC):
    @abstractmethod
    async def save(self, match: Match) -> None: ...

    @abstractmethod
    async def save_all(self, matches: list[Match]) -> None: ...

    @abstractmethod
    async def find_by_id(self, match_id: UUID) -> Match | None: ...

    @abstractmethod
    async def find_by_contest_id(self, contest_id: UUID) -> list[Match]: ...

    @abstractmethod
    async def delete(self, match_id: UUID) -> None: ...
