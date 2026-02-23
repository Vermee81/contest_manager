"""Contest ハンドラ"""
from datetime import datetime
from uuid import uuid4

from src.application.contest.commands import (
    AddPlayerCommand,
    CreateContestCommand,
    RemovePlayerCommand,
    UpdateContestStatusCommand,
)
from src.application.contest.queries import (
    ContestDTO,
    GetContestQuery,
    ListContestsQuery,
    PlayerDTO,
)
from src.domain.contest.contest import Contest
from src.domain.contest.repository import ContestRepository
from src.domain.contest.value_objects import ContestStatus


class ContestNotFoundError(Exception):
    def __init__(self, contest_id: object) -> None:
        super().__init__(f"Contest not found: {contest_id}")


class ContestCommandHandler:
    def __init__(self, repository: ContestRepository) -> None:
        self._repository = repository

    async def handle_create(self, command: CreateContestCommand) -> ContestDTO:
        contest = Contest(
            contest_id=uuid4(),
            name=command.name,
            game_title_id=command.game_title_id,
            format=command.format,
            best_of=command.best_of,
            status=ContestStatus.PRE_REGISTRATION,
            created_at=datetime.now(),
            players=[],
        )
        await self._repository.save(contest)
        return self._to_dto(contest)

    async def handle_update_status(
        self, command: UpdateContestStatusCommand
    ) -> ContestDTO:
        contest = await self._repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)
        contest.transition_status(command.new_status)
        await self._repository.save(contest)
        return self._to_dto(contest)

    async def handle_add_player(self, command: AddPlayerCommand) -> ContestDTO:
        contest = await self._repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)
        contest.add_player(name=command.name, seed=command.seed)
        await self._repository.save(contest)
        return self._to_dto(contest)

    async def handle_remove_player(self, command: RemovePlayerCommand) -> ContestDTO:
        contest = await self._repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)
        contest.remove_player(command.player_id)
        await self._repository.save(contest)
        return self._to_dto(contest)

    def _to_dto(self, contest: Contest) -> ContestDTO:
        return ContestDTO(
            contest_id=contest.contest_id,
            name=contest.name,
            game_title_id=contest.game_title_id,
            format=contest.format,
            best_of=contest.best_of,
            status=contest.status,
            created_at=contest.created_at,
            players=[
                PlayerDTO(
                    player_id=p.player_id,
                    contest_id=p.contest_id,
                    name=p.name,
                    seed=p.seed,
                )
                for p in contest.players
            ],
        )


class ContestQueryHandler:
    def __init__(self, repository: ContestRepository) -> None:
        self._repository = repository

    async def handle_get(self, query: GetContestQuery) -> ContestDTO:
        contest = await self._repository.find_by_id(query.contest_id)
        if contest is None:
            raise ContestNotFoundError(query.contest_id)
        return ContestCommandHandler(self._repository)._to_dto(contest)

    async def handle_list(self, query: ListContestsQuery) -> list[ContestDTO]:
        contests = await self._repository.find_all()
        handler = ContestCommandHandler(self._repository)
        return [handler._to_dto(c) for c in contests]
