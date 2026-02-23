"""SQLAlchemy ORM モデル"""
import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class GameTitleModel(Base):
    __tablename__ = "game_titles"

    game_title_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=uuid_str
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    contests: Mapped[list["ContestModel"]] = relationship(
        "ContestModel", back_populates="game_title"
    )


class ContestModel(Base):
    __tablename__ = "contests"

    contest_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=uuid_str
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    game_title_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("game_titles.game_title_id"), nullable=False
    )
    format: Mapped[str] = mapped_column(String(50), nullable=False)
    best_of: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)

    game_title: Mapped["GameTitleModel"] = relationship(
        "GameTitleModel", back_populates="contests"
    )
    players: Mapped[list["PlayerModel"]] = relationship(
        "PlayerModel", back_populates="contest", cascade="all, delete-orphan"
    )
    matches: Mapped[list["MatchModel"]] = relationship(
        "MatchModel", back_populates="contest", cascade="all, delete-orphan"
    )


class PlayerModel(Base):
    __tablename__ = "players"

    player_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=uuid_str
    )
    contest_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("contests.contest_id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)

    contest: Mapped["ContestModel"] = relationship(
        "ContestModel", back_populates="players"
    )


class MatchModel(Base):
    __tablename__ = "matches"

    match_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=uuid_str
    )
    contest_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("contests.contest_id"), nullable=False
    )
    player1_id: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    player2_id: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    player1_character: Mapped[str | None] = mapped_column(String(100), nullable=True)
    player2_character: Mapped[str | None] = mapped_column(String(100), nullable=True)
    player1_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    player2_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    round: Mapped[int | None] = mapped_column(Integer, nullable=True)
    match_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    contest: Mapped["ContestModel"] = relationship(
        "ContestModel", back_populates="matches"
    )
