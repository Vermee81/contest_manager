"""プレゼンテーション層テスト用設定"""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.contest.handlers import ContestCommandHandler, ContestQueryHandler
from src.application.game_title.handlers import (
    GameTitleCommandHandler,
    GameTitleQueryHandler,
)
from src.application.match.handlers import MatchCommandHandler, MatchQueryHandler
from src.application.standings.handlers import StandingsQueryHandler
from src.presentation.main import app
from src.presentation.dependencies import (
    get_contest_command_handler,
    get_contest_query_handler,
    get_game_title_command_handler,
    get_game_title_query_handler,
    get_match_command_handler,
    get_match_query_handler,
    get_standings_query_handler,
)


@pytest.fixture
def mock_game_title_cmd_handler() -> AsyncMock:
    return AsyncMock(spec=GameTitleCommandHandler)


@pytest.fixture
def mock_game_title_query_handler() -> AsyncMock:
    return AsyncMock(spec=GameTitleQueryHandler)


@pytest.fixture
def mock_contest_cmd_handler() -> AsyncMock:
    return AsyncMock(spec=ContestCommandHandler)


@pytest.fixture
def mock_contest_query_handler() -> AsyncMock:
    return AsyncMock(spec=ContestQueryHandler)


@pytest.fixture
def mock_match_cmd_handler() -> AsyncMock:
    return AsyncMock(spec=MatchCommandHandler)


@pytest.fixture
def mock_match_query_handler() -> AsyncMock:
    return AsyncMock(spec=MatchQueryHandler)


@pytest.fixture
def mock_standings_query_handler() -> AsyncMock:
    return AsyncMock(spec=StandingsQueryHandler)


@pytest.fixture
def client(
    mock_game_title_cmd_handler: AsyncMock,
    mock_game_title_query_handler: AsyncMock,
    mock_contest_cmd_handler: AsyncMock,
    mock_contest_query_handler: AsyncMock,
    mock_match_cmd_handler: AsyncMock,
    mock_match_query_handler: AsyncMock,
    mock_standings_query_handler: AsyncMock,
) -> TestClient:
    app.dependency_overrides[get_game_title_command_handler] = (
        lambda: mock_game_title_cmd_handler
    )
    app.dependency_overrides[get_game_title_query_handler] = (
        lambda: mock_game_title_query_handler
    )
    app.dependency_overrides[get_contest_command_handler] = (
        lambda: mock_contest_cmd_handler
    )
    app.dependency_overrides[get_contest_query_handler] = (
        lambda: mock_contest_query_handler
    )
    app.dependency_overrides[get_match_command_handler] = (
        lambda: mock_match_cmd_handler
    )
    app.dependency_overrides[get_match_query_handler] = (
        lambda: mock_match_query_handler
    )
    app.dependency_overrides[get_standings_query_handler] = (
        lambda: mock_standings_query_handler
    )

    yield TestClient(app)

    app.dependency_overrides.clear()
