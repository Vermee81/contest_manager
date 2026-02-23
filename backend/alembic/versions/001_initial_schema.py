"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-02-23

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "game_titles",
        sa.Column("game_title_id", mysql.CHAR(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
    )

    op.create_table(
        "contests",
        sa.Column("contest_id", mysql.CHAR(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "game_title_id",
            mysql.CHAR(36),
            sa.ForeignKey("game_titles.game_title_id"),
            nullable=False,
        ),
        sa.Column("format", sa.String(50), nullable=False),
        sa.Column("best_of", sa.Integer, nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("created_at", sa.String(50), nullable=False),
    )

    op.create_table(
        "players",
        sa.Column("player_id", mysql.CHAR(36), primary_key=True),
        sa.Column(
            "contest_id",
            mysql.CHAR(36),
            sa.ForeignKey("contests.contest_id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("seed", sa.Integer, nullable=True),
    )

    op.create_table(
        "matches",
        sa.Column("match_id", mysql.CHAR(36), primary_key=True),
        sa.Column(
            "contest_id",
            mysql.CHAR(36),
            sa.ForeignKey("contests.contest_id"),
            nullable=False,
        ),
        sa.Column("player1_id", mysql.CHAR(36), nullable=False),
        sa.Column("player2_id", mysql.CHAR(36), nullable=False),
        sa.Column("player1_character", sa.String(100), nullable=True),
        sa.Column("player2_character", sa.String(100), nullable=True),
        sa.Column("player1_wins", sa.Integer, nullable=False, server_default="0"),
        sa.Column("player2_wins", sa.Integer, nullable=False, server_default="0"),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("round", sa.Integer, nullable=True),
        sa.Column("match_order", sa.Integer, nullable=False, server_default="1"),
    )


def downgrade() -> None:
    op.drop_table("matches")
    op.drop_table("players")
    op.drop_table("contests")
    op.drop_table("game_titles")
