"""FastAPI 依存性注入設定"""
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.contest.handlers import ContestCommandHandler, ContestQueryHandler
from src.application.game_title.handlers import (
    GameTitleCommandHandler,
    GameTitleQueryHandler,
)
from src.application.match.handlers import MatchCommandHandler, MatchQueryHandler
from src.application.standings.handlers import StandingsQueryHandler
from src.domain.match.bracket_generator import BracketGenerator
from src.infrastructure.database import get_db_session
from src.infrastructure.mysql.contest_repository import MySQLContestRepository
from src.infrastructure.mysql.game_title_repository import MySQLGameTitleRepository
from src.infrastructure.mysql.match_repository import MySQLMatchRepository

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


async def get_game_title_repo(
    session: DbSession,
) -> MySQLGameTitleRepository:
    return MySQLGameTitleRepository(session)


async def get_contest_repo(
    session: DbSession,
) -> MySQLContestRepository:
    return MySQLContestRepository(session)


async def get_match_repo(
    session: DbSession,
) -> MySQLMatchRepository:
    return MySQLMatchRepository(session)


async def get_game_title_command_handler(
    repo: Annotated[MySQLGameTitleRepository, Depends(get_game_title_repo)],
) -> GameTitleCommandHandler:
    return GameTitleCommandHandler(repo)


async def get_game_title_query_handler(
    repo: Annotated[MySQLGameTitleRepository, Depends(get_game_title_repo)],
) -> GameTitleQueryHandler:
    return GameTitleQueryHandler(repo)


async def get_contest_command_handler(
    repo: Annotated[MySQLContestRepository, Depends(get_contest_repo)],
) -> ContestCommandHandler:
    return ContestCommandHandler(repo)


async def get_contest_query_handler(
    repo: Annotated[MySQLContestRepository, Depends(get_contest_repo)],
) -> ContestQueryHandler:
    return ContestQueryHandler(repo)


async def get_match_command_handler(
    contest_repo: Annotated[MySQLContestRepository, Depends(get_contest_repo)],
    match_repo: Annotated[MySQLMatchRepository, Depends(get_match_repo)],
) -> MatchCommandHandler:
    return MatchCommandHandler(contest_repo, match_repo, BracketGenerator())


async def get_match_query_handler(
    match_repo: Annotated[MySQLMatchRepository, Depends(get_match_repo)],
) -> MatchQueryHandler:
    return MatchQueryHandler(match_repo)


async def get_standings_query_handler(
    contest_repo: Annotated[MySQLContestRepository, Depends(get_contest_repo)],
    match_repo: Annotated[MySQLMatchRepository, Depends(get_match_repo)],
) -> StandingsQueryHandler:
    return StandingsQueryHandler(contest_repo, match_repo)
