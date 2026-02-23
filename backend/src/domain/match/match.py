"""Match Aggregate Root"""
from dataclasses import dataclass
from uuid import UUID

from src.domain.match.value_objects import MatchStatus


@dataclass
class Match:
    match_id: UUID
    contest_id: UUID
    player1_id: UUID
    player2_id: UUID
    player1_character: str | None
    player2_character: str | None
    player1_wins: int
    player2_wins: int
    comment: str | None
    status: MatchStatus
    round: int | None
    match_order: int

    def __post_init__(self) -> None:
        if self.player1_id == self.player2_id:
            raise ValueError("player1_id and player2_id must be different")

    def record_result(
        self,
        p1_character: str | None,
        p2_character: str | None,
        p1_wins: int,
        p2_wins: int,
        comment: str | None,
        best_of: int,
    ) -> None:
        max_wins = (best_of + 1) // 2
        if p1_wins > max_wins or p2_wins > max_wins:
            raise ValueError(
                f"wins cannot exceed {max_wins} for best_of={best_of}"
            )
        if p1_wins == p2_wins:
            raise ValueError("draw is not allowed: wins must differ")

        self.player1_character = p1_character
        self.player2_character = p2_character
        self.player1_wins = p1_wins
        self.player2_wins = p2_wins
        self.comment = comment
        self.status = MatchStatus.COMPLETED
