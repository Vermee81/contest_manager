"""ブラケット生成ドメインサービス"""
from itertools import combinations
from uuid import UUID, uuid4

from src.domain.contest.contest import Contest
from src.domain.contest.player import Player
from src.domain.match.match import Match
from src.domain.match.value_objects import MatchStatus

# TBD（試合結果待ち）プレイヤーのセンチネルUUID
TBD_PLAYER_ID = UUID("00000000-0000-0000-0000-000000000000")


class BracketGenerator:
    def generate_round_robin(self, contest: Contest) -> list[Match]:
        """全プレイヤー総当たりの試合を生成する"""
        players = contest.players
        matches: list[Match] = []

        for order, (p1, p2) in enumerate(combinations(players, 2), start=1):
            match = Match(
                match_id=uuid4(),
                contest_id=contest.contest_id,
                player1_id=p1.player_id,
                player2_id=p2.player_id,
                player1_character=None,
                player2_character=None,
                player1_wins=0,
                player2_wins=0,
                comment=None,
                status=MatchStatus.PENDING,
                round=None,
                match_order=order,
            )
            matches.append(match)

        return matches

    def generate_single_elimination(self, contest: Contest) -> list[Match]:
        """シングルエリミネーション（トーナメント）ブラケットを生成する。
        全ラウンドの試合（決勝まで）を一括生成する。未確定のプレイヤーは TBD_PLAYER_ID で表現。
        """
        players = contest.players
        size = self._next_power_of_two(len(players))
        slots: list[Player | None] = self._arrange_seeds(players, size)

        all_matches: list[Match] = []
        match_order = 1
        round_num = 1

        # 第1ラウンド: スロットからペアを生成
        round1_winners: list[UUID | None] = []

        for i in range(0, size, 2):
            p1 = slots[i]
            p2 = slots[i + 1]

            if p1 is None and p2 is None:
                round1_winners.append(None)
                continue

            if p1 is None or p2 is None:
                # BYE試合
                real_player = p1 if p1 is not None else p2
                real_id = real_player.player_id  # type: ignore[union-attr]
                bye_id = uuid4()

                p1_id = real_id if p1 is not None else bye_id
                p2_id = bye_id if p1 is not None else real_id
                p1_wins = 1 if p1 is not None else 0
                p2_wins = 0 if p1 is not None else 1

                match = Match(
                    match_id=uuid4(),
                    contest_id=contest.contest_id,
                    player1_id=p1_id,
                    player2_id=p2_id,
                    player1_character=None,
                    player2_character=None,
                    player1_wins=p1_wins,
                    player2_wins=p2_wins,
                    comment="BYE",
                    status=MatchStatus.COMPLETED,
                    round=round_num,
                    match_order=match_order,
                )
                all_matches.append(match)
                round1_winners.append(real_id)
            else:
                match = Match(
                    match_id=uuid4(),
                    contest_id=contest.contest_id,
                    player1_id=p1.player_id,
                    player2_id=p2.player_id,
                    player1_character=None,
                    player2_character=None,
                    player1_wins=0,
                    player2_wins=0,
                    comment=None,
                    status=MatchStatus.PENDING,
                    round=round_num,
                    match_order=match_order,
                )
                all_matches.append(match)
                round1_winners.append(None)  # 勝者未定

            match_order += 1

        # 以降のラウンド: 全てTBD_PLAYER_IDまたは既知勝者でプレースホルダーを生成
        current_winner_slots = round1_winners
        round_num += 1

        while len(current_winner_slots) > 1:
            next_winner_slots: list[UUID | None] = []

            for i in range(0, len(current_winner_slots), 2):
                w1 = current_winner_slots[i]
                w2 = current_winner_slots[i + 1]

                p1_id = w1 if w1 is not None else TBD_PLAYER_ID
                p2_id = w2 if w2 is not None else TBD_PLAYER_ID

                # p1_idとp2_idが同じ場合（どちらもTBD）は別のTBD UUIDを割り当て
                if p1_id == p2_id:
                    p2_id = uuid4()

                match = Match(
                    match_id=uuid4(),
                    contest_id=contest.contest_id,
                    player1_id=p1_id,
                    player2_id=p2_id,
                    player1_character=None,
                    player2_character=None,
                    player1_wins=0,
                    player2_wins=0,
                    comment=None,
                    status=MatchStatus.PENDING,
                    round=round_num,
                    match_order=match_order,
                )
                all_matches.append(match)
                next_winner_slots.append(None)
                match_order += 1

            current_winner_slots = next_winner_slots
            round_num += 1

        return all_matches

    def _next_power_of_two(self, n: int) -> int:
        power = 1
        while power < n:
            power *= 2
        return power

    def _arrange_seeds(
        self, players: list[Player], size: int
    ) -> list[Player | None]:
        """シード順に従ってブラケットスロットを配置する。
        BYEはNoneで表現する。
        シード1と2を反対側のブラケットに配置する。
        """
        seeded = sorted(
            players, key=lambda p: (p.seed is None, p.seed or 0)
        )

        slots: list[Player | None] = [None] * size
        bracket_positions = self._get_bracket_positions(size)

        for i, player in enumerate(seeded):
            if i < len(bracket_positions):
                slots[bracket_positions[i]] = player

        return slots

    def _get_bracket_positions(self, size: int) -> list[int]:
        """標準的なシードブラケット配置のポジションリストを返す"""
        if size == 1:
            return [0]

        positions = [0, size - 1]
        step = size // 2
        while step > 1:
            new_positions = []
            for pos in positions:
                new_positions.append(pos)
                new_positions.append(pos + step if pos + step < size else pos - step)
            positions = new_positions[:size]
            step //= 2

        return positions
