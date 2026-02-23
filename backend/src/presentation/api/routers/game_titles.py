"""GameTitle ルーター"""
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.game_title.commands import CreateGameTitleCommand
from src.application.game_title.handlers import (
    GameTitleCommandHandler,
    GameTitleQueryHandler,
)
from src.application.game_title.queries import GetGameTitlesQuery
from src.presentation.api.schemas.game_title import GameTitleCreate, GameTitleResponse
from src.presentation.dependencies import (
    get_game_title_command_handler,
    get_game_title_query_handler,
)

router = APIRouter(prefix="/game-titles", tags=["game-titles"])


@router.get("", response_model=list[GameTitleResponse])
async def list_game_titles(
    handler: Annotated[GameTitleQueryHandler, Depends(get_game_title_query_handler)],
) -> list[GameTitleResponse]:
    dtos = await handler.handle_list(GetGameTitlesQuery())
    return [
        GameTitleResponse(game_title_id=dto.game_title_id, name=dto.name)
        for dto in dtos
    ]


@router.post("", response_model=GameTitleResponse, status_code=status.HTTP_201_CREATED)
async def create_game_title(
    body: GameTitleCreate,
    handler: Annotated[GameTitleCommandHandler, Depends(get_game_title_command_handler)],
) -> GameTitleResponse:
    dto = await handler.handle_create(CreateGameTitleCommand(name=body.name))
    return GameTitleResponse(game_title_id=dto.game_title_id, name=dto.name)
