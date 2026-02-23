"""Match Aggregate Root のテスト"""
import uuid

import pytest

from src.domain.match.match import Match
from src.domain.match.value_objects import MatchStatus


def make_match(**kwargs) -> Match:  # type: ignore[no-untyped-def]
    defaults = {
        "match_id": uuid.uuid4(),
        "contest_id": uuid.uuid4(),
        "player1_id": uuid.uuid4(),
        "player2_id": uuid.uuid4(),
        "player1_character": None,
        "player2_character": None,
        "player1_wins": 0,
        "player2_wins": 0,
        "comment": None,
        "status": MatchStatus.PENDING,
        "round": None,
        "match_order": 1,
    }
    defaults.update(kwargs)
    return Match(**defaults)


class TestMatchCreate:
    def test_matchを作成できる_PENDING状態で(self) -> None:
        match = make_match()

        assert match.status == MatchStatus.PENDING
        assert match.player1_wins == 0
        assert match.player2_wins == 0

    def test_match_両プレイヤーが同一IDのとき例外(self) -> None:
        same_id = uuid.uuid4()
        with pytest.raises(ValueError, match="player"):
            make_match(player1_id=same_id, player2_id=same_id)


class TestMatchRecordResult:
    def test_match_結果を記録できる(self) -> None:
        match = make_match()
        match.record_result(
            p1_character="Ryu",
            p2_character="Ken",
            p1_wins=2,
            p2_wins=1,
            comment="Good game",
            best_of=3,
        )

        assert match.status == MatchStatus.COMPLETED
        assert match.player1_wins == 2
        assert match.player2_wins == 1
        assert match.player1_character == "Ryu"
        assert match.player2_character == "Ken"
        assert match.comment == "Good game"

    def test_match_勝利数がbest_ofを超えると例外(self) -> None:
        match = make_match()
        with pytest.raises(ValueError, match="wins"):
            match.record_result(
                p1_character=None,
                p2_character=None,
                p1_wins=3,
                p2_wins=0,
                comment=None,
                best_of=3,
            )

    def test_match_同じ勝利数での完了は不可(self) -> None:
        match = make_match()
        with pytest.raises(ValueError, match="draw"):
            match.record_result(
                p1_character=None,
                p2_character=None,
                p1_wins=1,
                p2_wins=1,
                comment=None,
                best_of=3,
            )
