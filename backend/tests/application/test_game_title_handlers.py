"""GameTitle ハンドラのテスト"""
import uuid
from unittest.mock import AsyncMock

import pytest

from src.application.game_title.commands import CreateGameTitleCommand
from src.application.game_title.handlers import (
    GameTitleCommandHandler,
    GameTitleQueryHandler,
)
from src.application.game_title.queries import GameTitleDTO, GetGameTitlesQuery
from src.domain.game_title.game_title import GameTitle


class TestGameTitleCommandHandler:
    def setup_method(self) -> None:
        self.mock_repo = AsyncMock()
        self.handler = GameTitleCommandHandler(self.mock_repo)

    async def test_ゲームタイトルを作成できる(self) -> None:
        command = CreateGameTitleCommand(name="Street Fighter 6")
        result = await self.handler.handle_create(command)

        assert result.name == "Street Fighter 6"
        assert isinstance(result.game_title_id, uuid.UUID)
        self.mock_repo.save.assert_called_once()

    async def test_ゲームタイトル作成時にリポジトリのsaveが呼ばれる(self) -> None:
        command = CreateGameTitleCommand(name="Tekken 8")
        await self.handler.handle_create(command)

        saved_entity = self.mock_repo.save.call_args[0][0]
        assert isinstance(saved_entity, GameTitle)
        assert saved_entity.name == "Tekken 8"


class TestGameTitleQueryHandler:
    def setup_method(self) -> None:
        self.mock_repo = AsyncMock()
        self.handler = GameTitleQueryHandler(self.mock_repo)

    async def test_ゲームタイトル一覧を取得できる(self) -> None:
        game_titles = [
            GameTitle(game_title_id=uuid.uuid4(), name="SF6"),
            GameTitle(game_title_id=uuid.uuid4(), name="Tekken 8"),
        ]
        self.mock_repo.find_all.return_value = game_titles

        result = await self.handler.handle_list(GetGameTitlesQuery())

        assert len(result) == 2
        assert all(isinstance(dto, GameTitleDTO) for dto in result)
        assert result[0].name == "SF6"
        assert result[1].name == "Tekken 8"

    async def test_ゲームタイトルが存在しないとき空リストを返す(self) -> None:
        self.mock_repo.find_all.return_value = []

        result = await self.handler.handle_list(GetGameTitlesQuery())

        assert result == []
