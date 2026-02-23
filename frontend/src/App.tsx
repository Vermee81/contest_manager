import { useState } from "react";
import { ContestList } from "./features/contests/components/ContestList";
import { ContestDetail } from "./features/contests/components/ContestDetail";
import { ContestCreateForm } from "./features/contests/components/ContestCreateForm";
import { MatchList } from "./features/matches/components/MatchList";
import { StandingsTable } from "./features/standings/components/StandingsTable";
import { GameTitleList } from "./features/game-titles/components/GameTitleList";
import { useContest } from "./features/contests/hooks/useContests";
import type { UUID } from "./shared/types";

type Page = "contests" | "contest-detail" | "game-titles";

function ContestPage({ contestId, onBack }: { contestId: UUID; onBack: () => void }) {
  const { data: contest } = useContest(contestId);

  return (
    <div>
      <button onClick={onBack}>← 一覧に戻る</button>
      <ContestDetail contestId={contestId} />
      {contest && (
        <>
          <MatchList
            contestId={contestId}
            players={contest.players}
            contestStatus={contest.status}
            bestOf={contest.best_of}
          />
          <StandingsTable contestId={contestId} />
        </>
      )}
    </div>
  );
}

export function App() {
  const [page, setPage] = useState<Page>("contests");
  const [selectedContestId, setSelectedContestId] = useState<UUID | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  if (page === "contest-detail" && selectedContestId) {
    return (
      <ContestPage
        contestId={selectedContestId}
        onBack={() => {
          setPage("contests");
          setSelectedContestId(null);
        }}
      />
    );
  }

  if (page === "game-titles") {
    return (
      <div>
        <button onClick={() => setPage("contests")}>← コンテスト一覧</button>
        <GameTitleList />
      </div>
    );
  }

  return (
    <div>
      <h1>Contest Manager</h1>
      <nav>
        <button onClick={() => setPage("game-titles")}>ゲームタイトル管理</button>
      </nav>

      <button onClick={() => setShowCreateForm((v) => !v)}>
        {showCreateForm ? "キャンセル" : "コンテスト作成"}
      </button>

      {showCreateForm && (
        <ContestCreateForm
          onCreated={() => setShowCreateForm(false)}
        />
      )}

      <ContestList
        onSelectContest={(contestId) => {
          setSelectedContestId(contestId);
          setPage("contest-detail");
        }}
      />
    </div>
  );
}
