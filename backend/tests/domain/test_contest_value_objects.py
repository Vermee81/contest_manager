"""Contest Value Objects のテスト"""
import pytest

from src.domain.contest.value_objects import (
    ContestStatus,
    InvalidStatusTransitionError,
    validate_status_transition,
)


class TestContestStatusTransition:
    def test_ContestStatus_PRE_REGISTRATIONからIN_PROGRESSへ遷移できる(self) -> None:
        validate_status_transition(ContestStatus.PRE_REGISTRATION, ContestStatus.IN_PROGRESS)

    def test_ContestStatus_IN_PROGRESSからCOMPLETEDへ遷移できる(self) -> None:
        validate_status_transition(ContestStatus.IN_PROGRESS, ContestStatus.COMPLETED)

    def test_ContestStatus_PRE_REGISTRATIONからCOMPLETEDへ直接遷移できない(self) -> None:
        with pytest.raises(InvalidStatusTransitionError):
            validate_status_transition(ContestStatus.PRE_REGISTRATION, ContestStatus.COMPLETED)

    def test_ContestStatus_COMPLETEDから他のステータスへ遷移できない(self) -> None:
        with pytest.raises(InvalidStatusTransitionError):
            validate_status_transition(ContestStatus.COMPLETED, ContestStatus.PRE_REGISTRATION)

        with pytest.raises(InvalidStatusTransitionError):
            validate_status_transition(ContestStatus.COMPLETED, ContestStatus.IN_PROGRESS)

    def test_ContestStatus_同一ステータスへの遷移は不可(self) -> None:
        with pytest.raises(InvalidStatusTransitionError):
            validate_status_transition(ContestStatus.IN_PROGRESS, ContestStatus.IN_PROGRESS)


class TestBestOf:
    def test_BestOf_は奇数のみ有効(self) -> None:
        from src.domain.contest.value_objects import validate_best_of

        validate_best_of(1)
        validate_best_of(3)
        validate_best_of(5)

        with pytest.raises(ValueError, match="best_of"):
            validate_best_of(2)

        with pytest.raises(ValueError, match="best_of"):
            validate_best_of(4)

    def test_BestOf_は1以上(self) -> None:
        from src.domain.contest.value_objects import validate_best_of

        with pytest.raises(ValueError, match="best_of"):
            validate_best_of(0)

        with pytest.raises(ValueError, match="best_of"):
            validate_best_of(-1)
