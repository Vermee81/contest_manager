"""Match MySQL リポジトリ実装"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.match.match import Match
from src.domain.match.repository import MatchRepository
from src.domain.match.value_objects import MatchStatus
from src.infrastructure.mysql.models import MatchModel


class MySQLMatchRepository(MatchRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, match: Match) -> None:
        model = await self._session.get(MatchModel, str(match.match_id))
        if model is None:
            model = self._to_model(match)
            self._session.add(model)
        else:
            self._update_model(model, match)
        await self._session.flush()

    async def save_all(self, matches: list[Match]) -> None:
        for match in matches:
            await self.save(match)

    async def find_by_id(self, match_id: uuid.UUID) -> Match | None:
        model = await self._session.get(MatchModel, str(match_id))
        if model is None:
            return None
        return self._to_domain(model)

    async def find_by_contest_id(self, contest_id: uuid.UUID) -> list[Match]:
        result = await self._session.execute(
            select(MatchModel)
            .where(MatchModel.contest_id == str(contest_id))
            .order_by(MatchModel.round, MatchModel.match_order)
        )
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def delete(self, match_id: uuid.UUID) -> None:
        model = await self._session.get(MatchModel, str(match_id))
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()

    def _to_domain(self, model: MatchModel) -> Match:
        return Match(
            match_id=uuid.UUID(model.match_id),
            contest_id=uuid.UUID(model.contest_id),
            player1_id=uuid.UUID(model.player1_id),
            player2_id=uuid.UUID(model.player2_id),
            player1_character=model.player1_character,
            player2_character=model.player2_character,
            player1_wins=model.player1_wins,
            player2_wins=model.player2_wins,
            comment=model.comment,
            status=MatchStatus(model.status),
            round=model.round,
            match_order=model.match_order,
        )

    def _to_model(self, match: Match) -> MatchModel:
        return MatchModel(
            match_id=str(match.match_id),
            contest_id=str(match.contest_id),
            player1_id=str(match.player1_id),
            player2_id=str(match.player2_id),
            player1_character=match.player1_character,
            player2_character=match.player2_character,
            player1_wins=match.player1_wins,
            player2_wins=match.player2_wins,
            comment=match.comment,
            status=match.status.value,
            round=match.round,
            match_order=match.match_order,
        )

    def _update_model(self, model: MatchModel, match: Match) -> None:
        model.player1_character = match.player1_character
        model.player2_character = match.player2_character
        model.player1_wins = match.player1_wins
        model.player2_wins = match.player2_wins
        model.comment = match.comment
        model.status = match.status.value
