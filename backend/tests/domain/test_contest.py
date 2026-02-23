"""Contest Aggregate Root のテスト"""
import uuid
from datetime import datetime

import pytest

from src.domain.contest.contest import Contest, ContestModificationError
from src.domain.contest.value_objects import ContestFormat, ContestStatus, InvalidStatusTransitionError


def make_contest(status: ContestStatus = ContestStatus.PRE_REGISTRATION) -> Contest:
    contest = Contest(
        contest_id=uuid.uuid4(),
        name="テストコンテスト",
        game_title_id=uuid.uuid4(),
        format=ContestFormat.ROUND_ROBIN,
        best_of=3,
        status=ContestStatus.PRE_REGISTRATION,
        created_at=datetime.now(),
        players=[],
    )
    if status == ContestStatus.IN_PROGRESS:
        contest.transition_status(ContestStatus.IN_PROGRESS)
    elif status == ContestStatus.COMPLETED:
        contest.transition_status(ContestStatus.IN_PROGRESS)
        contest.transition_status(ContestStatus.COMPLETED)
    return contest


class TestContestCreate:
    def test_contestを作成できる_デフォルト状態はPRE_REGISTRATION(self) -> None:
        contest = make_contest()
        assert contest.status == ContestStatus.PRE_REGISTRATION
        assert contest.players == []


class TestContestPlayerManagement:
    def test_contest_プレイヤーを追加できる_PRE_REGISTRATION中(self) -> None:
        contest = make_contest()
        player = contest.add_player(name="Alice", seed=None)

        assert player.name == "Alice"
        assert player.contest_id == contest.contest_id
        assert len(contest.players) == 1

    def test_contest_プレイヤーを削除できる_PRE_REGISTRATION中(self) -> None:
        contest = make_contest()
        player = contest.add_player(name="Alice", seed=None)
        contest.remove_player(player.player_id)

        assert len(contest.players) == 0

    def test_contest_プレイヤーを追加できない_IN_PROGRESS中(self) -> None:
        contest = make_contest(status=ContestStatus.IN_PROGRESS)

        with pytest.raises(ContestModificationError):
            contest.add_player(name="Alice", seed=None)

    def test_contest_プレイヤーを追加できない_COMPLETED中(self) -> None:
        contest = make_contest(status=ContestStatus.COMPLETED)

        with pytest.raises(ContestModificationError):
            contest.add_player(name="Alice", seed=None)


class TestContestStatusTransition:
    def test_contest_ステータスをIN_PROGRESSに変更できる(self) -> None:
        contest = make_contest()
        contest.transition_status(ContestStatus.IN_PROGRESS)

        assert contest.status == ContestStatus.IN_PROGRESS

    def test_contest_ステータスをCOMPLETEDに変更できる(self) -> None:
        contest = make_contest()
        contest.transition_status(ContestStatus.IN_PROGRESS)
        contest.transition_status(ContestStatus.COMPLETED)

        assert contest.status == ContestStatus.COMPLETED

    def test_contest_無効なステータス遷移で例外が発生する(self) -> None:
        contest = make_contest()

        with pytest.raises(InvalidStatusTransitionError):
            contest.transition_status(ContestStatus.COMPLETED)

    def test_contest_COMPLETEDになると変更不可(self) -> None:
        contest = make_contest(status=ContestStatus.COMPLETED)

        with pytest.raises(ContestModificationError):
            contest.add_player(name="Alice", seed=None)

        with pytest.raises(InvalidStatusTransitionError):
            contest.transition_status(ContestStatus.PRE_REGISTRATION)
