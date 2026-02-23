import { useContest, useUpdateContestStatus } from "../hooks/useContests";
import type { UUID } from "../../../shared/types";
import { PlayerList } from "./PlayerList";

interface Props {
  contestId: UUID;
}

export function ContestDetail({ contestId }: Props) {
  const { data: contest, isLoading, isError } = useContest(contestId);
  const updateStatusMutation = useUpdateContestStatus();

  if (isLoading) return <p>読み込み中...</p>;
  if (isError || !contest) return <p>コンテストが見つかりません</p>;

  return (
    <div>
      <h2>{contest.name}</h2>
      <p>ステータス: {contest.status}</p>
      <p>形式: {contest.format}</p>
      <p>先取本数: {contest.best_of}</p>

      {contest.status === "PRE_REGISTRATION" && (
        <button
          onClick={() =>
            updateStatusMutation.mutate({
              contestId,
              status: "IN_PROGRESS",
            })
          }
          disabled={updateStatusMutation.isPending}
        >
          開始する
        </button>
      )}
      {contest.status === "IN_PROGRESS" && (
        <button
          onClick={() =>
            updateStatusMutation.mutate({
              contestId,
              status: "COMPLETED",
            })
          }
          disabled={updateStatusMutation.isPending}
        >
          終了する
        </button>
      )}

      <PlayerList contest={contest} />
    </div>
  );
}
