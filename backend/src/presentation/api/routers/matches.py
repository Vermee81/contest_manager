"""Match ルーター"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.application.match.commands import (
    AddMatchCommand,
    DeleteMatchCommand,
    GenerateBracketCommand,
    RecordMatchResultCommand,
)
from src.application.match.handlers import MatchCommandHandler, MatchQueryHandler
from src.application.match.queries import GetMatchesQuery
from src.presentation.api.schemas.match import (
    MatchCreate,
    MatchResponse,
    MatchResultUpdate,
)
from src.presentation.dependencies import (
    get_match_command_handler,
    get_match_query_handler,
)

router = APIRouter(prefix="/contests/{contest_id}/matches", tags=["matches"])


def _build_response(dto) -> MatchResponse:  # type: ignore[no-untyped-def]
    return MatchResponse(
        match_id=dto.match_id,
        contest_id=dto.contest_id,
        player1_id=dto.player1_id,
        player2_id=dto.player2_id,
        player1_character=dto.player1_character,
        player2_character=dto.player2_character,
        player1_wins=dto.player1_wins,
        player2_wins=dto.player2_wins,
        comment=dto.comment,
        status=dto.status,
        round=dto.round,
        match_order=dto.match_order,
    )


@router.get("", response_model=list[MatchResponse])
async def list_matches(
    contest_id: UUID,
    handler: Annotated[MatchQueryHandler, Depends(get_match_query_handler)],
) -> list[MatchResponse]:
    dtos = await handler.handle_get_matches(GetMatchesQuery(contest_id=contest_id))
    return [_build_response(dto) for dto in dtos]


@router.post(
    "/generate",
    response_model=list[MatchResponse],
    status_code=status.HTTP_201_CREATED,
)
async def generate_bracket(
    contest_id: UUID,
    handler: Annotated[MatchCommandHandler, Depends(get_match_command_handler)],
) -> list[MatchResponse]:
    dtos = await handler.handle_generate_bracket(
        GenerateBracketCommand(contest_id=contest_id)
    )
    return [_build_response(dto) for dto in dtos]


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def add_match(
    contest_id: UUID,
    body: MatchCreate,
    handler: Annotated[MatchCommandHandler, Depends(get_match_command_handler)],
) -> MatchResponse:
    dto = await handler.handle_add_match(
        AddMatchCommand(
            contest_id=contest_id,
            player1_id=body.player1_id,
            player2_id=body.player2_id,
            round=body.round,
            match_order=body.match_order,
        )
    )
    return _build_response(dto)


@router.patch("/{match_id}", response_model=MatchResponse)
async def record_match_result(
    contest_id: UUID,
    match_id: UUID,
    body: MatchResultUpdate,
    handler: Annotated[MatchCommandHandler, Depends(get_match_command_handler)],
) -> MatchResponse:
    dto = await handler.handle_record_result(
        RecordMatchResultCommand(
            contest_id=contest_id,
            match_id=match_id,
            player1_character=body.player1_character,
            player2_character=body.player2_character,
            player1_wins=body.player1_wins,
            player2_wins=body.player2_wins,
            comment=body.comment,
        )
    )
    return _build_response(dto)


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    contest_id: UUID,
    match_id: UUID,
    handler: Annotated[MatchCommandHandler, Depends(get_match_command_handler)],
) -> None:
    await handler.handle_delete_match(
        DeleteMatchCommand(contest_id=contest_id, match_id=match_id)
    )
