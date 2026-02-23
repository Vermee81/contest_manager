"""Contest Aggregate Root"""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.contest.player import Player
from src.domain.contest.value_objects import (
    ContestFormat,
    ContestStatus,
    validate_status_transition,
)


class ContestModificationError(Exception):
    pass


@dataclass
class Contest:
    contest_id: UUID
    name: str
    game_title_id: UUID
    format: ContestFormat
    best_of: int
    status: ContestStatus
    created_at: datetime
    players: list[Player] = field(default_factory=list)

    def add_player(self, name: str, seed: int | None) -> Player:
        self._validate_modifiable()
        player = Player(
            player_id=uuid4(),
            contest_id=self.contest_id,
            name=name,
            seed=seed,
        )
        self.players.append(player)
        return player

    def remove_player(self, player_id: UUID) -> None:
        self._validate_modifiable()
        self.players = [p for p in self.players if p.player_id != player_id]

    def transition_status(self, new_status: ContestStatus) -> None:
        validate_status_transition(self.status, new_status)
        self.status = new_status

    def _validate_modifiable(self) -> None:
        if self.status != ContestStatus.PRE_REGISTRATION:
            raise ContestModificationError(
                f"Contest cannot be modified in status {self.status.value}"
            )
