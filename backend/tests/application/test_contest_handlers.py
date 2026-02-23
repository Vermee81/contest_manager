"""Contest ハンドラのテスト"""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.application.contest.commands import (
    AddPlayerCommand,
    CreateContestCommand,
    RemovePlayerCommand,
    UpdateContestStatusCommand,
)
from src.application.contest.handlers import (
    ContestCommandHandler,
    ContestNotFoundError,
    ContestQueryHandler,
)
from src.application.contest.queries import ListContestsQuery
from src.domain.contest.contest import Contest, ContestModificationError
from src.domain.contest.value_objects import ContestFormat, ContestStatus, InvalidStatusTransitionError


def make_contest(
    status: ContestStatus = ContestStatus.PRE_REGISTRATION,
) -> Contest:
    contest = Contest(
        contest_id=uuid.uuid4(),
        name="Test Contest",
        game_title_id=uuid.uuid4(),
        format=ContestFormat.ROUND_ROBIN,
        best_of=3,
        status=ContestStatus.PRE_REGISTRATION,
        created_at=datetime.now(),
        players=[],
    )
    if status == ContestStatus.IN_PROGRESS:
        contest.transition_status(ContestStatus.IN_PROGRESS)
    elif status == ContestStatus.COMPLETED:
        contest.transition_status(ContestStatus.IN_PROGRESS)
        contest.transition_status(ContestStatus.COMPLETED)
    return contest


class TestContestCommandHandler:
    def setup_method(self) -> None:
        self.mock_repo = AsyncMock()
        self.handler = ContestCommandHandler(self.mock_repo)

    async def test_コンテストを作成できる(self) -> None:
        command = CreateContestCommand(
            name="SF6 Tournament",
            game_title_id=uuid.uuid4(),
            format=ContestFormat.ROUND_ROBIN,
            best_of=3,
        )
        result = await self.handler.handle_create(command)

        assert result.name == "SF6 Tournament"
        assert result.status == ContestStatus.PRE_REGISTRATION
        assert isinstance(result.contest_id, uuid.UUID)
        self.mock_repo.save.assert_called_once()

    async def test_ステータスをIN_PROGRESSに更新できる(self) -> None:
        contest = make_contest()
        self.mock_repo.find_by_id.return_value = contest

        command = UpdateContestStatusCommand(
            contest_id=contest.contest_id,
            new_status=ContestStatus.IN_PROGRESS,
        )
        result = await self.handler.handle_update_status(command)

        assert result.status == ContestStatus.IN_PROGRESS

    async def test_コンテストが見つからない場合例外が発生する(self) -> None:
        self.mock_repo.find_by_id.return_value = None

        command = UpdateContestStatusCommand(
            contest_id=uuid.uuid4(),
            new_status=ContestStatus.IN_PROGRESS,
        )
        with pytest.raises(ContestNotFoundError):
            await self.handler.handle_update_status(command)

    async def test_プレイヤーを追加できる(self) -> None:
        contest = make_contest()
        self.mock_repo.find_by_id.return_value = contest

        command = AddPlayerCommand(
            contest_id=contest.contest_id,
            name="Alice",
            seed=None,
        )
        result = await self.handler.handle_add_player(command)

        assert len(result.players) == 1
        assert result.players[0].name == "Alice"

    async def test_プレイヤーを削除できる(self) -> None:
        contest = make_contest()
        player = contest.add_player(name="Alice", seed=None)
        self.mock_repo.find_by_id.return_value = contest

        command = RemovePlayerCommand(
            contest_id=contest.contest_id,
            player_id=player.player_id,
        )
        result = await self.handler.handle_remove_player(command)

        assert len(result.players) == 0

    async def test_IN_PROGRESS中はプレイヤーを追加できない(self) -> None:
        contest = make_contest(status=ContestStatus.IN_PROGRESS)
        self.mock_repo.find_by_id.return_value = contest

        command = AddPlayerCommand(
            contest_id=contest.contest_id,
            name="Alice",
            seed=None,
        )
        with pytest.raises(ContestModificationError):
            await self.handler.handle_add_player(command)


class TestContestQueryHandler:
    def setup_method(self) -> None:
        self.mock_repo = AsyncMock()
        self.handler = ContestQueryHandler(self.mock_repo)

    async def test_コンテスト一覧を取得できる(self) -> None:
        contests = [make_contest(), make_contest()]
        self.mock_repo.find_all.return_value = contests

        from src.application.contest.queries import ListContestsQuery
        result = await self.handler.handle_list(ListContestsQuery())

        assert len(result) == 2

    async def test_コンテストが見つからない場合例外が発生する(self) -> None:
        self.mock_repo.find_by_id.return_value = None

        from src.application.contest.queries import GetContestQuery
        with pytest.raises(ContestNotFoundError):
            await self.handler.handle_get(GetContestQuery(contest_id=uuid.uuid4()))
