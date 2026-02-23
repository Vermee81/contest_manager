"""GameTitle ルーターのテスト"""
import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.game_title.queries import GameTitleDTO


class TestGameTitlesRouter:
    def test_ゲームタイトル一覧を取得できる(
        self,
        client: TestClient,
        mock_game_title_query_handler: AsyncMock,
    ) -> None:
        game_title_id = uuid.uuid4()
        mock_game_title_query_handler.handle_list.return_value = [
            GameTitleDTO(game_title_id=game_title_id, name="SF6")
        ]

        response = client.get("/api/v1/game-titles")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "SF6"
        assert data[0]["game_title_id"] == str(game_title_id)

    def test_ゲームタイトルを作成できる(
        self,
        client: TestClient,
        mock_game_title_cmd_handler: AsyncMock,
    ) -> None:
        game_title_id = uuid.uuid4()
        mock_game_title_cmd_handler.handle_create.return_value = GameTitleDTO(
            game_title_id=game_title_id, name="Tekken 8"
        )

        response = client.post("/api/v1/game-titles", json={"name": "Tekken 8"})

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tekken 8"
        assert data["game_title_id"] == str(game_title_id)

    def test_ゲームタイトルが存在しない場合は空リストを返す(
        self,
        client: TestClient,
        mock_game_title_query_handler: AsyncMock,
    ) -> None:
        mock_game_title_query_handler.handle_list.return_value = []

        response = client.get("/api/v1/game-titles")

        assert response.status_code == 200
        assert response.json() == []
