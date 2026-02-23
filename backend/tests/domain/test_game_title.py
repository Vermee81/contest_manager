"""GameTitle エンティティのテスト"""
import uuid

import pytest

from src.domain.game_title.game_title import GameTitle


class TestGameTitleCreate:
    def test_game_titleを作成できる(self) -> None:
        game_title_id = uuid.uuid4()
        game_title = GameTitle(game_title_id=game_title_id, name="Street Fighter 6")

        assert game_title.game_title_id == game_title_id
        assert game_title.name == "Street Fighter 6"

    def test_game_title_名前が空文字のとき例外が発生する(self) -> None:
        with pytest.raises(ValueError, match="name"):
            GameTitle(game_title_id=uuid.uuid4(), name="")

    def test_game_title_名前が空白のみのとき例外が発生する(self) -> None:
        with pytest.raises(ValueError, match="name"):
            GameTitle(game_title_id=uuid.uuid4(), name="   ")
