"""Contest ルーターのテスト"""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.contest.handlers import ContestNotFoundError
from src.application.contest.queries import ContestDTO, PlayerDTO
from src.domain.contest.value_objects import ContestFormat, ContestStatus


def make_contest_dto(
    status: ContestStatus = ContestStatus.PRE_REGISTRATION,
) -> ContestDTO:
    return ContestDTO(
        contest_id=uuid.uuid4(),
        name="SF6 Tournament",
        game_title_id=uuid.uuid4(),
        format=ContestFormat.ROUND_ROBIN,
        best_of=3,
        status=status,
        created_at=datetime.now(),
        players=[],
    )


class TestContestsRouter:
    def test_コンテスト一覧を取得できる(
        self,
        client: TestClient,
        mock_contest_query_handler: AsyncMock,
    ) -> None:
        dto = make_contest_dto()
        mock_contest_query_handler.handle_list.return_value = [dto]

        response = client.get("/api/v1/contests")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "SF6 Tournament"

    def test_コンテストを作成できる(
        self,
        client: TestClient,
        mock_contest_cmd_handler: AsyncMock,
    ) -> None:
        dto = make_contest_dto()
        mock_contest_cmd_handler.handle_create.return_value = dto

        response = client.post(
            "/api/v1/contests",
            json={
                "name": "SF6 Tournament",
                "game_title_id": str(uuid.uuid4()),
                "format": "ROUND_ROBIN",
                "best_of": 3,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "SF6 Tournament"

    def test_コンテスト詳細を取得できる(
        self,
        client: TestClient,
        mock_contest_query_handler: AsyncMock,
    ) -> None:
        dto = make_contest_dto()
        mock_contest_query_handler.handle_get.return_value = dto

        response = client.get(f"/api/v1/contests/{dto.contest_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["contest_id"] == str(dto.contest_id)

    def test_存在しないコンテストは404を返す(
        self,
        client: TestClient,
        mock_contest_query_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        mock_contest_query_handler.handle_get.side_effect = ContestNotFoundError(
            contest_id
        )

        response = client.get(f"/api/v1/contests/{contest_id}")

        assert response.status_code == 404

    def test_ステータスを更新できる(
        self,
        client: TestClient,
        mock_contest_cmd_handler: AsyncMock,
    ) -> None:
        dto = make_contest_dto(status=ContestStatus.IN_PROGRESS)
        mock_contest_cmd_handler.handle_update_status.return_value = dto

        response = client.patch(
            f"/api/v1/contests/{dto.contest_id}/status",
            json={"status": "IN_PROGRESS"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "IN_PROGRESS"

    def test_プレイヤーを追加できる(
        self,
        client: TestClient,
        mock_contest_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        player_id = uuid.uuid4()
        dto = ContestDTO(
            contest_id=contest_id,
            name="Tournament",
            game_title_id=uuid.uuid4(),
            format=ContestFormat.ROUND_ROBIN,
            best_of=3,
            status=ContestStatus.PRE_REGISTRATION,
            created_at=datetime.now(),
            players=[
                PlayerDTO(
                    player_id=player_id,
                    contest_id=contest_id,
                    name="Alice",
                    seed=None,
                )
            ],
        )
        mock_contest_cmd_handler.handle_add_player.return_value = dto

        response = client.post(
            f"/api/v1/contests/{contest_id}/players",
            json={"name": "Alice"},
        )

        assert response.status_code == 201
        data = response.json()
        assert len(data["players"]) == 1
        assert data["players"][0]["name"] == "Alice"

    def test_プレイヤーを削除できる(
        self,
        client: TestClient,
        mock_contest_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        player_id = uuid.uuid4()
        dto = make_contest_dto()
        mock_contest_cmd_handler.handle_remove_player.return_value = dto

        response = client.delete(
            f"/api/v1/contests/{contest_id}/players/{player_id}"
        )

        assert response.status_code == 200
