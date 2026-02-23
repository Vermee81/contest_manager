"""Contest リポジトリインターフェース"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.contest.contest import Contest


class ContestRepository(ABC):
    @abstractmethod
    async def save(self, contest: Contest) -> None: ...

    @abstractmethod
    async def find_by_id(self, contest_id: UUID) -> Contest | None: ...

    @abstractmethod
    async def find_all(self) -> list[Contest]: ...

    @abstractmethod
    async def delete(self, contest_id: UUID) -> None: ...
