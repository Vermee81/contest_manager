import { useState } from "react";
import { useAddPlayer, useRemovePlayer } from "../hooks/useContests";
import type { Contest } from "../../../shared/types";

interface Props {
  contest: Contest;
}

export function PlayerList({ contest }: Props) {
  const addPlayerMutation = useAddPlayer();
  const removePlayerMutation = useRemovePlayer();
  const [newPlayerName, setNewPlayerName] = useState("");

  const canModify = contest.status === "PRE_REGISTRATION";

  const handleAddPlayer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPlayerName.trim()) return;
    await addPlayerMutation.mutateAsync({
      contestId: contest.contest_id,
      name: newPlayerName.trim(),
    });
    setNewPlayerName("");
  };

  return (
    <div>
      <h3>プレイヤー ({contest.players.length}人)</h3>

      {canModify && (
        <form onSubmit={handleAddPlayer}>
          <input
            type="text"
            value={newPlayerName}
            onChange={(e) => setNewPlayerName(e.target.value)}
            placeholder="プレイヤー名"
            aria-label="プレイヤー名"
          />
          <button type="submit" disabled={addPlayerMutation.isPending}>
            追加
          </button>
        </form>
      )}

      <ul>
        {contest.players.map((player) => (
          <li key={player.player_id}>
            {player.name}
            {player.seed != null && ` (シード ${player.seed})`}
            {canModify && (
              <button
                onClick={() =>
                  removePlayerMutation.mutate({
                    contestId: contest.contest_id,
                    playerId: player.player_id,
                  })
                }
                disabled={removePlayerMutation.isPending}
              >
                削除
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
