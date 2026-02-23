"""Contest ルーター"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.application.contest.commands import (
    AddPlayerCommand,
    CreateContestCommand,
    RemovePlayerCommand,
    UpdateContestStatusCommand,
)
from src.application.contest.handlers import ContestCommandHandler, ContestQueryHandler
from src.application.contest.queries import GetContestQuery, ListContestsQuery
from src.presentation.api.schemas.contest import (
    ContestCreate,
    ContestResponse,
    ContestStatusUpdate,
    PlayerCreate,
    PlayerResponse,
)
from src.presentation.dependencies import (
    get_contest_command_handler,
    get_contest_query_handler,
)

router = APIRouter(prefix="/contests", tags=["contests"])


def _build_response(dto) -> ContestResponse:  # type: ignore[no-untyped-def]
    return ContestResponse(
        contest_id=dto.contest_id,
        name=dto.name,
        game_title_id=dto.game_title_id,
        format=dto.format,
        best_of=dto.best_of,
        status=dto.status,
        created_at=dto.created_at,
        players=[
            PlayerResponse(
                player_id=p.player_id,
                contest_id=p.contest_id,
                name=p.name,
                seed=p.seed,
            )
            for p in dto.players
        ],
    )


@router.get("", response_model=list[ContestResponse])
async def list_contests(
    handler: Annotated[ContestQueryHandler, Depends(get_contest_query_handler)],
) -> list[ContestResponse]:
    dtos = await handler.handle_list(ListContestsQuery())
    return [_build_response(dto) for dto in dtos]


@router.post("", response_model=ContestResponse, status_code=status.HTTP_201_CREATED)
async def create_contest(
    body: ContestCreate,
    handler: Annotated[ContestCommandHandler, Depends(get_contest_command_handler)],
) -> ContestResponse:
    dto = await handler.handle_create(
        CreateContestCommand(
            name=body.name,
            game_title_id=body.game_title_id,
            format=body.format,
            best_of=body.best_of,
        )
    )
    return _build_response(dto)


@router.get("/{contest_id}", response_model=ContestResponse)
async def get_contest(
    contest_id: UUID,
    handler: Annotated[ContestQueryHandler, Depends(get_contest_query_handler)],
) -> ContestResponse:
    dto = await handler.handle_get(GetContestQuery(contest_id=contest_id))
    return _build_response(dto)


@router.patch("/{contest_id}/status", response_model=ContestResponse)
async def update_contest_status(
    contest_id: UUID,
    body: ContestStatusUpdate,
    handler: Annotated[ContestCommandHandler, Depends(get_contest_command_handler)],
) -> ContestResponse:
    dto = await handler.handle_update_status(
        UpdateContestStatusCommand(
            contest_id=contest_id,
            new_status=body.status,
        )
    )
    return _build_response(dto)


@router.get("/{contest_id}/players", response_model=list[PlayerResponse])
async def list_players(
    contest_id: UUID,
    handler: Annotated[ContestQueryHandler, Depends(get_contest_query_handler)],
) -> list[PlayerResponse]:
    dto = await handler.handle_get(GetContestQuery(contest_id=contest_id))
    return [
        PlayerResponse(
            player_id=p.player_id,
            contest_id=p.contest_id,
            name=p.name,
            seed=p.seed,
        )
        for p in dto.players
    ]


@router.post(
    "/{contest_id}/players",
    response_model=ContestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_player(
    contest_id: UUID,
    body: PlayerCreate,
    handler: Annotated[ContestCommandHandler, Depends(get_contest_command_handler)],
) -> ContestResponse:
    dto = await handler.handle_add_player(
        AddPlayerCommand(
            contest_id=contest_id,
            name=body.name,
            seed=body.seed,
        )
    )
    return _build_response(dto)


@router.delete(
    "/{contest_id}/players/{player_id}",
    response_model=ContestResponse,
)
async def remove_player(
    contest_id: UUID,
    player_id: UUID,
    handler: Annotated[ContestCommandHandler, Depends(get_contest_command_handler)],
) -> ContestResponse:
    dto = await handler.handle_remove_player(
        RemovePlayerCommand(
            contest_id=contest_id,
            player_id=player_id,
        )
    )
    return _build_response(dto)
