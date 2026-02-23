import { useContests } from "../hooks/useContests";
import type { UUID } from "../../../shared/types";

interface Props {
  onSelectContest: (contestId: UUID) => void;
}

export function ContestList({ onSelectContest }: Props) {
  const { data: contests, isLoading, isError } = useContests();

  if (isLoading) return <p>読み込み中...</p>;
  if (isError) return <p>エラーが発生しました</p>;

  return (
    <div>
      <h2>コンテスト一覧</h2>
      {contests?.length === 0 && <p>コンテストがありません</p>}
      <ul>
        {contests?.map((contest) => (
          <li key={contest.contest_id}>
            <button onClick={() => onSelectContest(contest.contest_id)}>
              {contest.name} [{contest.status}]
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
