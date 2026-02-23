"""Match ハンドラのテスト"""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.application.match.commands import (
    DeleteMatchCommand,
    GenerateBracketCommand,
    RecordMatchResultCommand,
)
from src.application.match.handlers import (
    MatchCommandHandler,
    MatchNotFoundError,
    MatchQueryHandler,
)
from src.application.match.queries import GetMatchesQuery, MatchDTO
from src.domain.contest.contest import Contest, ContestModificationError
from src.domain.contest.value_objects import ContestFormat, ContestStatus
from src.domain.match.bracket_generator import BracketGenerator
from src.domain.match.match import Match
from src.domain.match.value_objects import MatchStatus


def make_contest(
    status: ContestStatus = ContestStatus.PRE_REGISTRATION,
    format: ContestFormat = ContestFormat.ROUND_ROBIN,
) -> Contest:
    contest = Contest(
        contest_id=uuid.uuid4(),
        name="Test Contest",
        game_title_id=uuid.uuid4(),
        format=format,
        best_of=3,
        status=ContestStatus.PRE_REGISTRATION,
        created_at=datetime.now(),
        players=[],
    )
    contest.add_player(name="Alice", seed=1)
    contest.add_player(name="Bob", seed=2)
    if status == ContestStatus.IN_PROGRESS:
        contest.transition_status(ContestStatus.IN_PROGRESS)
    return contest


def make_match(contest_id: uuid.UUID | None = None) -> Match:
    return Match(
        match_id=uuid.uuid4(),
        contest_id=contest_id or uuid.uuid4(),
        player1_id=uuid.uuid4(),
        player2_id=uuid.uuid4(),
        player1_character=None,
        player2_character=None,
        player1_wins=0,
        player2_wins=0,
        comment=None,
        status=MatchStatus.PENDING,
        round=None,
        match_order=1,
    )


class TestMatchCommandHandler:
    def setup_method(self) -> None:
        self.mock_contest_repo = AsyncMock()
        self.mock_match_repo = AsyncMock()
        self.bracket_generator = BracketGenerator()
        self.handler = MatchCommandHandler(
            self.mock_contest_repo,
            self.mock_match_repo,
            self.bracket_generator,
        )

    async def test_ブラケットを生成できる_ROUND_ROBIN(self) -> None:
        contest = make_contest()
        self.mock_contest_repo.find_by_id.return_value = contest

        command = GenerateBracketCommand(contest_id=contest.contest_id)
        result = await self.handler.handle_generate_bracket(command)

        assert len(result) == 1  # 2人なので1試合
        assert all(isinstance(dto, MatchDTO) for dto in result)
        self.mock_match_repo.save_all.assert_called_once()

    async def test_ブラケット生成時にコンテストが見つからない場合例外(self) -> None:
        from src.application.contest.handlers import ContestNotFoundError
        self.mock_contest_repo.find_by_id.return_value = None

        command = GenerateBracketCommand(contest_id=uuid.uuid4())
        with pytest.raises(ContestNotFoundError):
            await self.handler.handle_generate_bracket(command)

    async def test_試合結果を記録できる(self) -> None:
        contest = make_contest(status=ContestStatus.IN_PROGRESS)
        match = make_match(contest_id=contest.contest_id)
        self.mock_contest_repo.find_by_id.return_value = contest
        self.mock_match_repo.find_by_id.return_value = match

        command = RecordMatchResultCommand(
            contest_id=contest.contest_id,
            match_id=match.match_id,
            player1_character="Ryu",
            player2_character="Ken",
            player1_wins=2,
            player2_wins=1,
            comment="Good game",
        )
        result = await self.handler.handle_record_result(command)

        assert result.status == MatchStatus.COMPLETED
        assert result.player1_wins == 2
        assert result.player2_wins == 1
        assert result.player1_character == "Ryu"

    async def test_試合結果記録時に試合が見つからない場合例外(self) -> None:
        contest = make_contest()
        self.mock_contest_repo.find_by_id.return_value = contest
        self.mock_match_repo.find_by_id.return_value = None

        command = RecordMatchResultCommand(
            contest_id=contest.contest_id,
            match_id=uuid.uuid4(),
            player1_character=None,
            player2_character=None,
            player1_wins=2,
            player2_wins=1,
            comment=None,
        )
        with pytest.raises(MatchNotFoundError):
            await self.handler.handle_record_result(command)

    async def test_IN_PROGRESS中は試合を削除できない(self) -> None:
        contest = make_contest(status=ContestStatus.IN_PROGRESS)
        self.mock_contest_repo.find_by_id.return_value = contest

        command = DeleteMatchCommand(
            contest_id=contest.contest_id,
            match_id=uuid.uuid4(),
        )
        with pytest.raises(ContestModificationError):
            await self.handler.handle_delete_match(command)


class TestMatchQueryHandler:
    def setup_method(self) -> None:
        self.mock_match_repo = AsyncMock()
        self.handler = MatchQueryHandler(self.mock_match_repo)

    async def test_コンテストの試合一覧を取得できる(self) -> None:
        contest_id = uuid.uuid4()
        matches = [make_match(contest_id), make_match(contest_id)]
        self.mock_match_repo.find_by_contest_id.return_value = matches

        result = await self.handler.handle_get_matches(
            GetMatchesQuery(contest_id=contest_id)
        )

        assert len(result) == 2
        assert all(isinstance(dto, MatchDTO) for dto in result)
