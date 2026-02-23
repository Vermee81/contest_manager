"""GameTitle MySQL リポジトリ実装"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.game_title.game_title import GameTitle
from src.domain.game_title.repository import GameTitleRepository
from src.infrastructure.mysql.models import GameTitleModel


class MySQLGameTitleRepository(GameTitleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, game_title: GameTitle) -> None:
        model = await self._session.get(GameTitleModel, str(game_title.game_title_id))
        if model is None:
            model = self._to_model(game_title)
            self._session.add(model)
        else:
            model.name = game_title.name
        await self._session.flush()

    async def find_by_id(self, game_title_id: uuid.UUID) -> GameTitle | None:
        model = await self._session.get(GameTitleModel, str(game_title_id))
        if model is None:
            return None
        return self._to_domain(model)

    async def find_all(self) -> list[GameTitle]:
        result = await self._session.execute(select(GameTitleModel))
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: GameTitleModel) -> GameTitle:
        return GameTitle(
            game_title_id=uuid.UUID(model.game_title_id),
            name=model.name,
        )

    def _to_model(self, game_title: GameTitle) -> GameTitleModel:
        return GameTitleModel(
            game_title_id=str(game_title.game_title_id),
            name=game_title.name,
        )
