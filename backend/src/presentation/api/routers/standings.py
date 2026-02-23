"""Standings ルーター"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.standings.handlers import StandingsQueryHandler
from src.application.standings.queries import GetStandingsQuery
from src.presentation.api.schemas.standings import StandingsEntryResponse, StandingsResponse
from src.presentation.dependencies import get_standings_query_handler

router = APIRouter(prefix="/contests/{contest_id}/standings", tags=["standings"])


@router.get("", response_model=StandingsResponse)
async def get_standings(
    contest_id: UUID,
    handler: Annotated[StandingsQueryHandler, Depends(get_standings_query_handler)],
) -> StandingsResponse:
    dto = await handler.handle_get_standings(GetStandingsQuery(contest_id=contest_id))
    return StandingsResponse(
        contest_id=dto.contest_id,
        entries=[
            StandingsEntryResponse(
                player_id=e.player_id,
                player_name=e.player_name,
                wins=e.wins,
                losses=e.losses,
                matches_played=e.matches_played,
                game_wins=e.game_wins,
                game_losses=e.game_losses,
            )
            for e in dto.entries
        ],
    )
