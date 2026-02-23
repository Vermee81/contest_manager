"""Match ハンドラ"""
from uuid import uuid4

from src.application.contest.handlers import ContestNotFoundError
from src.application.match.commands import (
    AddMatchCommand,
    DeleteMatchCommand,
    GenerateBracketCommand,
    RecordMatchResultCommand,
)
from src.application.match.queries import GetMatchesQuery, MatchDTO
from src.domain.contest.contest import ContestModificationError
from src.domain.contest.repository import ContestRepository
from src.domain.contest.value_objects import ContestFormat, ContestStatus
from src.domain.match.bracket_generator import BracketGenerator
from src.domain.match.match import Match
from src.domain.match.repository import MatchRepository
from src.domain.match.value_objects import MatchStatus


class MatchNotFoundError(Exception):
    def __init__(self, match_id: object) -> None:
        super().__init__(f"Match not found: {match_id}")


class MatchCommandHandler:
    def __init__(
        self,
        contest_repository: ContestRepository,
        match_repository: MatchRepository,
        bracket_generator: BracketGenerator,
    ) -> None:
        self._contest_repository = contest_repository
        self._match_repository = match_repository
        self._bracket_generator = bracket_generator

    async def handle_generate_bracket(
        self, command: GenerateBracketCommand
    ) -> list[MatchDTO]:
        contest = await self._contest_repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)

        if contest.format == ContestFormat.ROUND_ROBIN:
            matches = self._bracket_generator.generate_round_robin(contest)
        else:
            matches = self._bracket_generator.generate_single_elimination(contest)

        await self._match_repository.save_all(matches)
        return [self._to_dto(m) for m in matches]

    async def handle_add_match(self, command: AddMatchCommand) -> MatchDTO:
        contest = await self._contest_repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)
        if contest.status == ContestStatus.COMPLETED:
            raise ContestModificationError(
                "Cannot add matches to a completed contest"
            )

        match = Match(
            match_id=uuid4(),
            contest_id=command.contest_id,
            player1_id=command.player1_id,
            player2_id=command.player2_id,
            player1_character=None,
            player2_character=None,
            player1_wins=0,
            player2_wins=0,
            comment=None,
            status=MatchStatus.PENDING,
            round=command.round,
            match_order=command.match_order,
        )
        await self._match_repository.save(match)
        return self._to_dto(match)

    async def handle_record_result(
        self, command: RecordMatchResultCommand
    ) -> MatchDTO:
        contest = await self._contest_repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)

        match = await self._match_repository.find_by_id(command.match_id)
        if match is None:
            raise MatchNotFoundError(command.match_id)

        match.record_result(
            p1_character=command.player1_character,
            p2_character=command.player2_character,
            p1_wins=command.player1_wins,
            p2_wins=command.player2_wins,
            comment=command.comment,
            best_of=contest.best_of,
        )
        await self._match_repository.save(match)
        return self._to_dto(match)

    async def handle_delete_match(self, command: DeleteMatchCommand) -> None:
        contest = await self._contest_repository.find_by_id(command.contest_id)
        if contest is None:
            raise ContestNotFoundError(command.contest_id)
        if contest.status == ContestStatus.IN_PROGRESS:
            raise ContestModificationError(
                "Cannot delete matches from an in-progress contest"
            )

        match = await self._match_repository.find_by_id(command.match_id)
        if match is None:
            raise MatchNotFoundError(command.match_id)

        await self._match_repository.delete(command.match_id)

    def _to_dto(self, match: Match) -> MatchDTO:
        return MatchDTO(
            match_id=match.match_id,
            contest_id=match.contest_id,
            player1_id=match.player1_id,
            player2_id=match.player2_id,
            player1_character=match.player1_character,
            player2_character=match.player2_character,
            player1_wins=match.player1_wins,
            player2_wins=match.player2_wins,
            comment=match.comment,
            status=match.status,
            round=match.round,
            match_order=match.match_order,
        )


class MatchQueryHandler:
    def __init__(self, match_repository: MatchRepository) -> None:
        self._match_repository = match_repository

    async def handle_get_matches(self, query: GetMatchesQuery) -> list[MatchDTO]:
        matches = await self._match_repository.find_by_contest_id(query.contest_id)
        return [
            MatchDTO(
                match_id=m.match_id,
                contest_id=m.contest_id,
                player1_id=m.player1_id,
                player2_id=m.player2_id,
                player1_character=m.player1_character,
                player2_character=m.player2_character,
                player1_wins=m.player1_wins,
                player2_wins=m.player2_wins,
                comment=m.comment,
                status=m.status,
                round=m.round,
                match_order=m.match_order,
            )
            for m in matches
        ]
