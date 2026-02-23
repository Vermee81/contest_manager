import { useState } from "react";
import { useMatches, useGenerateBracket, useRecordMatchResult } from "../hooks/useMatches";
import type { Match, Player, UUID } from "../../../shared/types";

interface Props {
  contestId: UUID;
  players: Player[];
  contestStatus: string;
  bestOf: number;
}

function getPlayerName(playerId: UUID, players: Player[]): string {
  return players.find((p) => p.player_id === playerId)?.name ?? playerId.slice(0, 8);
}

function MatchResultForm({
  match,
  contestId,
  bestOf,
  players,
}: {
  match: Match;
  contestId: UUID;
  bestOf: number;
  players: Player[];
}) {
  const recordMutation = useRecordMatchResult();
  const [p1Char, setP1Char] = useState("");
  const [p2Char, setP2Char] = useState("");
  const [p1Wins, setP1Wins] = useState(0);
  const [p2Wins, setP2Wins] = useState(0);
  const [comment, setComment] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await recordMutation.mutateAsync({
      contestId,
      matchId: match.match_id,
      input: {
        player1_character: p1Char || null,
        player2_character: p2Char || null,
        player1_wins: p1Wins,
        player2_wins: p2Wins,
        comment: comment || null,
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <span>{getPlayerName(match.player1_id, players)}</span>
        <input
          type="text"
          placeholder="キャラ"
          value={p1Char}
          onChange={(e) => setP1Char(e.target.value)}
          aria-label={`${getPlayerName(match.player1_id, players)}のキャラ`}
        />
        <input
          type="number"
          min={0}
          max={(bestOf + 1) / 2}
          value={p1Wins}
          onChange={(e) => setP1Wins(Number(e.target.value))}
          aria-label={`${getPlayerName(match.player1_id, players)}の勝利数`}
        />
      </div>
      <div>
        <span>{getPlayerName(match.player2_id, players)}</span>
        <input
          type="text"
          placeholder="キャラ"
          value={p2Char}
          onChange={(e) => setP2Char(e.target.value)}
          aria-label={`${getPlayerName(match.player2_id, players)}のキャラ`}
        />
        <input
          type="number"
          min={0}
          max={(bestOf + 1) / 2}
          value={p2Wins}
          onChange={(e) => setP2Wins(Number(e.target.value))}
          aria-label={`${getPlayerName(match.player2_id, players)}の勝利数`}
        />
      </div>
      <input
        type="text"
        placeholder="コメント"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        aria-label="コメント"
      />
      <button type="submit" disabled={recordMutation.isPending}>
        記録
      </button>
    </form>
  );
}

export function MatchList({ contestId, players, contestStatus, bestOf }: Props) {
  const { data: matches, isLoading, isError } = useMatches(contestId);
  const generateMutation = useGenerateBracket();

  if (isLoading) return <p>読み込み中...</p>;
  if (isError) return <p>エラーが発生しました</p>;

  return (
    <div>
      <h3>試合一覧</h3>

      {contestStatus !== "COMPLETED" && (matches?.length ?? 0) === 0 && (
        <button
          onClick={() => generateMutation.mutate(contestId)}
          disabled={generateMutation.isPending}
        >
          ブラケット生成
        </button>
      )}

      {matches?.map((match) => (
        <div key={match.match_id} style={{ border: "1px solid #ccc", margin: "8px", padding: "8px" }}>
          <div>
            {getPlayerName(match.player1_id, players)} vs{" "}
            {getPlayerName(match.player2_id, players)}
          </div>
          {match.status === "COMPLETED" ? (
            <div>
              結果: {match.player1_wins} - {match.player2_wins}
              {match.player1_character && ` (${match.player1_character} vs ${match.player2_character})`}
              {match.comment && <span> - {match.comment}</span>}
            </div>
          ) : (
            contestStatus === "IN_PROGRESS" && (
              <MatchResultForm
                match={match}
                contestId={contestId}
                bestOf={bestOf}
                players={players}
              />
            )
          )}
        </div>
      ))}
    </div>
  );
}
