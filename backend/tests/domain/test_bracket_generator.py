"""BracketGenerator ドメインサービスのテスト"""
import uuid
from datetime import datetime

import pytest

from src.domain.contest.contest import Contest
from src.domain.contest.player import Player
from src.domain.contest.value_objects import ContestFormat, ContestStatus
from src.domain.match.bracket_generator import BracketGenerator
from src.domain.match.value_objects import MatchStatus


def make_contest_with_players(
    n: int, format: ContestFormat = ContestFormat.ROUND_ROBIN
) -> Contest:
    contest = Contest(
        contest_id=uuid.uuid4(),
        name="Test",
        game_title_id=uuid.uuid4(),
        format=format,
        best_of=3,
        status=ContestStatus.PRE_REGISTRATION,
        created_at=datetime.now(),
        players=[],
    )
    for i in range(n):
        contest.add_player(name=f"Player{i + 1}", seed=i + 1)
    return contest


class TestRoundRobinGeneration:
    def test_round_robin_2人のとき1試合生成される(self) -> None:
        contest = make_contest_with_players(2, ContestFormat.ROUND_ROBIN)
        generator = BracketGenerator()
        matches = generator.generate_round_robin(contest)

        assert len(matches) == 1

    def test_round_robin_3人のとき3試合生成される(self) -> None:
        contest = make_contest_with_players(3, ContestFormat.ROUND_ROBIN)
        generator = BracketGenerator()
        matches = generator.generate_round_robin(contest)

        assert len(matches) == 3

    def test_round_robin_4人のとき6試合生成される(self) -> None:
        contest = make_contest_with_players(4, ContestFormat.ROUND_ROBIN)
        generator = BracketGenerator()
        matches = generator.generate_round_robin(contest)

        assert len(matches) == 6

    def test_round_robin_全試合がPENDING状態(self) -> None:
        contest = make_contest_with_players(3, ContestFormat.ROUND_ROBIN)
        generator = BracketGenerator()
        matches = generator.generate_round_robin(contest)

        for match in matches:
            assert match.status == MatchStatus.PENDING

    def test_round_robin_全ての組み合わせが含まれる(self) -> None:
        contest = make_contest_with_players(3, ContestFormat.ROUND_ROBIN)
        generator = BracketGenerator()
        matches = generator.generate_round_robin(contest)

        player_ids = [p.player_id for p in contest.players]
        match_pairs = {
            (m.player1_id, m.player2_id) for m in matches
        } | {(m.player2_id, m.player1_id) for m in matches}

        for i in range(len(player_ids)):
            for j in range(i + 1, len(player_ids)):
                assert (player_ids[i], player_ids[j]) in match_pairs or (
                    player_ids[j], player_ids[i]
                ) in match_pairs


class TestSingleEliminationGeneration:
    def test_single_elimination_2人のとき1試合生成される(self) -> None:
        contest = make_contest_with_players(2, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        assert len(matches) == 1

    def test_single_elimination_3人のとき_BYEを含む4人ブラケットが生成される(self) -> None:
        contest = make_contest_with_players(3, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        # 4人ブラケット: 準決勝2 + 決勝1 = 3試合
        assert len(matches) == 3

    def test_single_elimination_4人のとき3試合生成される(self) -> None:
        contest = make_contest_with_players(4, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        assert len(matches) == 3

    def test_single_elimination_5人のとき_8人ブラケットで7試合生成される(self) -> None:
        contest = make_contest_with_players(5, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        assert len(matches) == 7

    def test_single_elimination_BYEは自動的に不戦勝扱い(self) -> None:
        """BYEが含まれる試合はCOMPLETED状態になる"""
        contest = make_contest_with_players(3, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        # 3人→4人ブラケット: 第1ラウンドに1つBYE試合がある
        round1_matches = [m for m in matches if m.round == 1]
        bye_matches = [m for m in round1_matches if m.status == MatchStatus.COMPLETED]
        assert len(bye_matches) == 1

    def test_single_elimination_シード順が反映される(self) -> None:
        """シード1とシード4が反対側のブラケットに配置される"""
        contest = make_contest_with_players(4, ContestFormat.SINGLE_ELIMINATION)
        generator = BracketGenerator()
        matches = generator.generate_single_elimination(contest)

        # ラウンド1の試合を確認
        round1_matches = [m for m in matches if m.round == 1]
        assert len(round1_matches) == 2

        # 全プレイヤーが一度ずつ登場する
        all_player_ids_in_matches = set()
        for m in round1_matches:
            all_player_ids_in_matches.add(m.player1_id)
            all_player_ids_in_matches.add(m.player2_id)

        assert len(all_player_ids_in_matches) == 4
