"""GameTitle ハンドラ"""
from uuid import uuid4

from src.application.game_title.commands import CreateGameTitleCommand
from src.application.game_title.queries import GameTitleDTO, GetGameTitlesQuery
from src.domain.game_title.game_title import GameTitle
from src.domain.game_title.repository import GameTitleRepository


class GameTitleCommandHandler:
    def __init__(self, repository: GameTitleRepository) -> None:
        self._repository = repository

    async def handle_create(self, command: CreateGameTitleCommand) -> GameTitleDTO:
        game_title = GameTitle(game_title_id=uuid4(), name=command.name)
        await self._repository.save(game_title)
        return GameTitleDTO(
            game_title_id=game_title.game_title_id,
            name=game_title.name,
        )


class GameTitleQueryHandler:
    def __init__(self, repository: GameTitleRepository) -> None:
        self._repository = repository

    async def handle_list(self, query: GetGameTitlesQuery) -> list[GameTitleDTO]:
        game_titles = await self._repository.find_all()
        return [
            GameTitleDTO(game_title_id=gt.game_title_id, name=gt.name)
            for gt in game_titles
        ]
