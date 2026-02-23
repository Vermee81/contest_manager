"""Standings ルーターのテスト"""
import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.standings.queries import StandingsDTO, StandingsEntryDTO


class TestStandingsRouter:
    def test_順位表を取得できる(
        self,
        client: TestClient,
        mock_standings_query_handler: AsyncMock,
    ) -> None:
        contest_id = uuid.uuid4()
        player1_id = uuid.uuid4()
        player2_id = uuid.uuid4()
        dto = StandingsDTO(
            contest_id=contest_id,
            entries=[
                StandingsEntryDTO(
                    player_id=player1_id,
                    player_name="Alice",
                    wins=2,
                    losses=0,
                    matches_played=2,
                    game_wins=6,
                    game_losses=2,
                ),
                StandingsEntryDTO(
                    player_id=player2_id,
                    player_name="Bob",
                    wins=0,
                    losses=2,
                    matches_played=2,
                    game_wins=2,
                    game_losses=6,
                ),
            ],
        )
        mock_standings_query_handler.handle_get_standings.return_value = dto

        response = client.get(f"/api/v1/contests/{contest_id}/standings")

        assert response.status_code == 200
        data = response.json()
        assert data["contest_id"] == str(contest_id)
        assert len(data["entries"]) == 2
        assert data["entries"][0]["player_name"] == "Alice"
        assert data["entries"][0]["wins"] == 2
        assert data["entries"][1]["player_name"] == "Bob"
