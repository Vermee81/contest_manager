"""Player エンティティのテスト"""
import uuid

import pytest

from src.domain.contest.player import Player


class TestPlayerCreate:
    def test_playerを作成できる(self) -> None:
        player_id = uuid.uuid4()
        contest_id = uuid.uuid4()
        player = Player(player_id=player_id, contest_id=contest_id, name="Alice", seed=1)

        assert player.player_id == player_id
        assert player.contest_id == contest_id
        assert player.name == "Alice"
        assert player.seed == 1

    def test_player_名前が空文字のとき例外(self) -> None:
        with pytest.raises(ValueError, match="name"):
            Player(player_id=uuid.uuid4(), contest_id=uuid.uuid4(), name="", seed=None)

    def test_player_seedはNoneが許容される(self) -> None:
        player = Player(player_id=uuid.uuid4(), contest_id=uuid.uuid4(), name="Bob", seed=None)
        assert player.seed is None

    def test_player_seedは正の整数のみ有効(self) -> None:
        with pytest.raises(ValueError, match="seed"):
            Player(player_id=uuid.uuid4(), contest_id=uuid.uuid4(), name="Alice", seed=0)

        with pytest.raises(ValueError, match="seed"):
            Player(player_id=uuid.uuid4(), contest_id=uuid.uuid4(), name="Alice", seed=-1)
