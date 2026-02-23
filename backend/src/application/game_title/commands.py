"""GameTitle コマンド"""
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateGameTitleCommand:
    name: str
