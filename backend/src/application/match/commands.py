"""Match コマンド"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GenerateBracketCommand:
    contest_id: UUID


@dataclass(frozen=True)
class AddMatchCommand:
    contest_id: UUID
    player1_id: UUID
    player2_id: UUID
    round: int | None
    match_order: int


@dataclass(frozen=True)
class RecordMatchResultCommand:
    contest_id: UUID
    match_id: UUID
    player1_character: str | None
    player2_character: str | None
    player1_wins: int
    player2_wins: int
    comment: str | None


@dataclass(frozen=True)
class DeleteMatchCommand:
    contest_id: UUID
    match_id: UUID
