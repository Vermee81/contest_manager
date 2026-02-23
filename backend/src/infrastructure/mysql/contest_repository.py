"""Contest MySQL リポジトリ実装"""
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.contest.contest import Contest
from src.domain.contest.player import Player
from src.domain.contest.repository import ContestRepository
from src.domain.contest.value_objects import ContestFormat, ContestStatus
from src.infrastructure.mysql.models import ContestModel, PlayerModel


class MySQLContestRepository(ContestRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, contest: Contest) -> None:
        model = await self._session.get(
            ContestModel,
            str(contest.contest_id),
            options=[selectinload(ContestModel.players)],
        )
        if model is None:
            model = ContestModel(
                contest_id=str(contest.contest_id),
                name=contest.name,
                game_title_id=str(contest.game_title_id),
                format=contest.format.value,
                best_of=contest.best_of,
                status=contest.status.value,
                created_at=contest.created_at.isoformat(),
            )
            model.players = []  # レイジーロードを防ぐため空リストで初期化
            self._session.add(model)
            await self._session.flush()

        model.name = contest.name
        model.status = contest.status.value
        model.best_of = contest.best_of

        # プレイヤーの同期
        existing_ids = {p.player_id for p in model.players}
        domain_ids = {str(p.player_id) for p in contest.players}

        # 削除
        model.players = [p for p in model.players if p.player_id in domain_ids]

        # 追加
        for player in contest.players:
            if str(player.player_id) not in existing_ids:
                player_model = PlayerModel(
                    player_id=str(player.player_id),
                    contest_id=str(player.contest_id),
                    name=player.name,
                    seed=player.seed,
                )
                model.players.append(player_model)

        await self._session.flush()

    async def find_by_id(self, contest_id: uuid.UUID) -> Contest | None:
        result = await self._session.execute(
            select(ContestModel)
            .where(ContestModel.contest_id == str(contest_id))
            .options(selectinload(ContestModel.players))
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def find_all(self) -> list[Contest]:
        result = await self._session.execute(
            select(ContestModel).options(selectinload(ContestModel.players))
        )
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def delete(self, contest_id: uuid.UUID) -> None:
        model = await self._session.get(
            ContestModel,
            str(contest_id),
            options=[
                selectinload(ContestModel.players),
                selectinload(ContestModel.matches),
            ],
        )
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()

    def _to_domain(self, model: ContestModel) -> Contest:
        players = [
            Player(
                player_id=uuid.UUID(p.player_id),
                contest_id=uuid.UUID(p.contest_id),
                name=p.name,
                seed=p.seed,
            )
            for p in model.players
        ]
        return Contest(
            contest_id=uuid.UUID(model.contest_id),
            name=model.name,
            game_title_id=uuid.UUID(model.game_title_id),
            format=ContestFormat(model.format),
            best_of=model.best_of,
            status=ContestStatus(model.status),
            created_at=datetime.fromisoformat(model.created_at),
            players=players,
        )
