"""Standings ハンドラ"""
from uuid import UUID

from src.application.contest.handlers import ContestNotFoundError
from src.application.standings.queries import (
    GetStandingsQuery,
    StandingsDTO,
    StandingsEntryDTO,
)
from src.domain.contest.contest import Contest
from src.domain.contest.player import Player
from src.domain.contest.repository import ContestRepository
from src.domain.contest.value_objects import ContestFormat
from src.domain.match.match import Match
from src.domain.match.repository import MatchRepository
from src.domain.match.value_objects import MatchStatus


class StandingsQueryHandler:
    def __init__(
        self,
        contest_repository: ContestRepository,
        match_repository: MatchRepository,
    ) -> None:
        self._contest_repository = contest_repository
        self._match_repository = match_repository

    async def handle_get_standings(self, query: GetStandingsQuery) -> StandingsDTO:
        contest = await self._contest_repository.find_by_id(query.contest_id)
        if contest is None:
            raise ContestNotFoundError(query.contest_id)

        matches = await self._match_repository.find_by_contest_id(query.contest_id)
        completed_matches = [m for m in matches if m.status == MatchStatus.COMPLETED]

        if contest.format == ContestFormat.ROUND_ROBIN:
            entries = self._calculate_round_robin_standings(
                contest, completed_matches
            )
        else:
            entries = self._calculate_elimination_standings(
                contest, completed_matches
            )

        return StandingsDTO(contest_id=query.contest_id, entries=entries)

    def _calculate_round_robin_standings(
        self, contest: Contest, completed_matches: list[Match]
    ) -> list[StandingsEntryDTO]:
        player_map = {p.player_id: p for p in contest.players}
        stats: dict[UUID, dict[str, int]] = {
            p.player_id: {
                "wins": 0,
                "losses": 0,
                "matches_played": 0,
                "game_wins": 0,
                "game_losses": 0,
            }
            for p in contest.players
        }

        for match in completed_matches:
            p1_id = match.player1_id
            p2_id = match.player2_id

            if p1_id not in stats or p2_id not in stats:
                continue  # BYE試合など

            stats[p1_id]["game_wins"] += match.player1_wins
            stats[p1_id]["game_losses"] += match.player2_wins
            stats[p2_id]["game_wins"] += match.player2_wins
            stats[p2_id]["game_losses"] += match.player1_wins
            stats[p1_id]["matches_played"] += 1
            stats[p2_id]["matches_played"] += 1

            if match.player1_wins > match.player2_wins:
                stats[p1_id]["wins"] += 1
                stats[p2_id]["losses"] += 1
            else:
                stats[p2_id]["wins"] += 1
                stats[p1_id]["losses"] += 1

        entries = [
            StandingsEntryDTO(
                player_id=pid,
                player_name=player_map[pid].name,
                wins=s["wins"],
                losses=s["losses"],
                matches_played=s["matches_played"],
                game_wins=s["game_wins"],
                game_losses=s["game_losses"],
            )
            for pid, s in stats.items()
            if pid in player_map
        ]

        entries.sort(
            key=lambda e: (-e.wins, -(e.game_wins - e.game_losses)),
        )
        return entries

    def _calculate_elimination_standings(
        self, contest: Contest, completed_matches: list[Match]
    ) -> list[StandingsEntryDTO]:
        player_map = {p.player_id: p for p in contest.players}
        stats: dict[UUID, dict[str, int]] = {
            p.player_id: {
                "wins": 0,
                "losses": 0,
                "matches_played": 0,
                "game_wins": 0,
                "game_losses": 0,
            }
            for p in contest.players
        }

        for match in completed_matches:
            p1_id = match.player1_id
            p2_id = match.player2_id

            if p1_id not in stats and p2_id not in stats:
                continue

            if p1_id in stats:
                stats[p1_id]["game_wins"] += match.player1_wins
                stats[p1_id]["game_losses"] += match.player2_wins
                stats[p1_id]["matches_played"] += 1

            if p2_id in stats:
                stats[p2_id]["game_wins"] += match.player2_wins
                stats[p2_id]["game_losses"] += match.player1_wins
                stats[p2_id]["matches_played"] += 1

            if match.player1_wins > match.player2_wins:
                if p1_id in stats:
                    stats[p1_id]["wins"] += 1
                if p2_id in stats:
                    stats[p2_id]["losses"] += 1
            else:
                if p2_id in stats:
                    stats[p2_id]["wins"] += 1
                if p1_id in stats:
                    stats[p1_id]["losses"] += 1

        entries = [
            StandingsEntryDTO(
                player_id=pid,
                player_name=player_map[pid].name,
                wins=s["wins"],
                losses=s["losses"],
                matches_played=s["matches_played"],
                game_wins=s["game_wins"],
                game_losses=s["game_losses"],
            )
            for pid, s in stats.items()
            if pid in player_map
        ]

        entries.sort(key=lambda e: (-e.wins, -e.matches_played))
        return entries
