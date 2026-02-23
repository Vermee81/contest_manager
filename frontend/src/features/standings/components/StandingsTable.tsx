import { useStandings } from "../hooks/useStandings";
import type { UUID } from "../../../shared/types";

interface Props {
  contestId: UUID;
}

export function StandingsTable({ contestId }: Props) {
  const { data: standings, isLoading, isError } = useStandings(contestId);

  if (isLoading) return <p>読み込み中...</p>;
  if (isError) return <p>エラーが発生しました</p>;
  if (!standings) return null;

  return (
    <div>
      <h3>順位表</h3>
      <table>
        <thead>
          <tr>
            <th>順位</th>
            <th>プレイヤー</th>
            <th>勝</th>
            <th>負</th>
            <th>試合数</th>
            <th>ゲーム勝</th>
            <th>ゲーム負</th>
          </tr>
        </thead>
        <tbody>
          {standings.entries.map((entry, index) => (
            <tr key={entry.player_id}>
              <td>{index + 1}</td>
              <td>{entry.player_name}</td>
              <td>{entry.wins}</td>
              <td>{entry.losses}</td>
              <td>{entry.matches_played}</td>
              <td>{entry.game_wins}</td>
              <td>{entry.game_losses}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
