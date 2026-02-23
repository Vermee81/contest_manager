"""Standings ハンドラのテスト"""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.application.standings.handlers import StandingsQueryHandler
from src.application.standings.queries import GetStandingsQuery
from src.domain.contest.contest import Contest
from src.domain.contest.value_objects import ContestFormat, ContestStatus
from src.domain.match.match import Match
from src.domain.match.value_objects import MatchStatus


def make_contest(format: ContestFormat = ContestFormat.ROUND_ROBIN) -> Contest:
    contest = Contest(
        contest_id=uuid.uuid4(),
        name="Test",
        game_title_id=uuid.uuid4(),
        format=format,
        best_of=3,
        status=ContestStatus.IN_PROGRESS,
        created_at=datetime.now(),
        players=[],
    )
    contest.status = ContestStatus.PRE_REGISTRATION
    player_a = contest.add_player(name="Alice", seed=1)
    player_b = contest.add_player(name="Bob", seed=2)
    player_c = contest.add_player(name="Charlie", seed=3)
    contest.status = ContestStatus.IN_PROGRESS
    return contest


class TestStandingsQueryHandler:
    def setup_method(self) -> None:
        self.mock_contest_repo = AsyncMock()
        self.mock_match_repo = AsyncMock()
        self.handler = StandingsQueryHandler(
            self.mock_contest_repo,
            self.mock_match_repo,
        )

    async def test_順位表を取得できる_ROUND_ROBIN(self) -> None:
        contest = make_contest(ContestFormat.ROUND_ROBIN)
        players = contest.players  # Alice, Bob, Charlie

        # Alice 2勝, Bob 1勝1負, Charlie 2負
        matches = [
            Match(
                match_id=uuid.uuid4(),
                contest_id=contest.contest_id,
                player1_id=players[0].player_id,  # Alice
                player2_id=players[1].player_id,  # Bob
                player1_character=None,
                player2_character=None,
                player1_wins=2,
                player2_wins=1,
                comment=None,
                status=MatchStatus.COMPLETED,
                round=None,
                match_order=1,
            ),
            Match(
                match_id=uuid.uuid4(),
                contest_id=contest.contest_id,
                player1_id=players[0].player_id,  # Alice
                player2_id=players[2].player_id,  # Charlie
                player1_character=None,
                player2_character=None,
                player1_wins=2,
                player2_wins=0,
                comment=None,
                status=MatchStatus.COMPLETED,
                round=None,
                match_order=2,
            ),
            Match(
                match_id=uuid.uuid4(),
                contest_id=contest.contest_id,
                player1_id=players[1].player_id,  # Bob
                player2_id=players[2].player_id,  # Charlie
                player1_character=None,
                player2_character=None,
                player1_wins=2,
                player2_wins=1,
                comment=None,
                status=MatchStatus.COMPLETED,
                round=None,
                match_order=3,
            ),
        ]

        self.mock_contest_repo.find_by_id.return_value = contest
        self.mock_match_repo.find_by_contest_id.return_value = matches

        result = await self.handler.handle_get_standings(
            GetStandingsQuery(contest_id=contest.contest_id)
        )

        assert len(result.entries) == 3
        # Alice が1位（2勝）
        assert result.entries[0].player_name == "Alice"
        assert result.entries[0].wins == 2
        assert result.entries[0].losses == 0
        # Bob が2位（1勝1負）
        assert result.entries[1].player_name == "Bob"
        assert result.entries[1].wins == 1
        assert result.entries[1].losses == 1
        # Charlie が3位（2負）
        assert result.entries[2].player_name == "Charlie"
        assert result.entries[2].wins == 0
        assert result.entries[2].losses == 2

    async def test_試合が0件のとき全プレイヤーが0勝(self) -> None:
        contest = make_contest()
        self.mock_contest_repo.find_by_id.return_value = contest
        self.mock_match_repo.find_by_contest_id.return_value = []

        result = await self.handler.handle_get_standings(
            GetStandingsQuery(contest_id=contest.contest_id)
        )

        assert len(result.entries) == 3
        assert all(e.wins == 0 for e in result.entries)

    async def test_コンテストが見つからない場合例外(self) -> None:
        from src.application.contest.handlers import ContestNotFoundError
        self.mock_contest_repo.find_by_id.return_value = None

        with pytest.raises(ContestNotFoundError):
            await self.handler.handle_get_standings(
                GetStandingsQuery(contest_id=uuid.uuid4())
            )
