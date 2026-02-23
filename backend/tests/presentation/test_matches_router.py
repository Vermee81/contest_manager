"""Match ルーターのテスト"""
import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.match.queries import MatchDTO
from src.domain.match.value_objects import MatchStatus


def make_match_dto(contest_id: uuid.UUID | None = None) -> MatchDTO:
    return MatchDTO(
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


class TestMatchesRouter:
    def test_試合一覧を取得できる(
        self,
        client: TestClient,
        mock_match_query_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        dto = make_match_dto(contest_id)
        mock_match_query_handler.handle_get_matches.return_value = [dto]

        response = client.get(f"/api/v1/contests/{contest_id}/matches")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_ブラケットを生成できる(
        self,
        client: TestClient,
        mock_match_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        dtos = [make_match_dto(contest_id), make_match_dto(contest_id)]
        mock_match_cmd_handler.handle_generate_bracket.return_value = dtos

        response = client.post(
            f"/api/v1/contests/{contest_id}/matches/generate"
        )

        assert response.status_code == 201
        data = response.json()
        assert len(data) == 2

    def test_試合を手動で追加できる(
        self,
        client: TestClient,
        mock_match_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        dto = make_match_dto(contest_id)
        mock_match_cmd_handler.handle_add_match.return_value = dto

        response = client.post(
            f"/api/v1/contests/{contest_id}/matches",
            json={
                "player1_id": str(uuid.uuid4()),
                "player2_id": str(uuid.uuid4()),
                "match_order": 1,
            },
        )

        assert response.status_code == 201

    def test_試合結果を更新できる(
        self,
        client: TestClient,
        mock_match_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        match_id = uuid.uuid4()
        dto = MatchDTO(
            match_id=match_id,
            contest_id=contest_id,
            player1_id=uuid.uuid4(),
            player2_id=uuid.uuid4(),
            player1_character="Ryu",
            player2_character="Ken",
            player1_wins=2,
            player2_wins=1,
            comment="GG",
            status=MatchStatus.COMPLETED,
            round=None,
            match_order=1,
        )
        mock_match_cmd_handler.handle_record_result.return_value = dto

        response = client.patch(
            f"/api/v1/contests/{contest_id}/matches/{match_id}",
            json={
                "player1_character": "Ryu",
                "player2_character": "Ken",
                "player1_wins": 2,
                "player2_wins": 1,
                "comment": "GG",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "COMPLETED"
        assert data["player1_wins"] == 2

    def test_試合を削除できる(
        self,
        client: TestClient,
        mock_match_cmd_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        match_id = uuid.uuid4()
        mock_match_cmd_handler.handle_delete_match.return_value = None

        response = client.delete(
            f"/api/v1/contests/{contest_id}/matches/{match_id}"
        )

        assert response.status_code == 204
