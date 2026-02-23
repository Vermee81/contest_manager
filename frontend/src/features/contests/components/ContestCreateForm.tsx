import { useState } from "react";
import { useCreateContest } from "../hooks/useContests";
import { useGameTitles } from "../../game-titles/hooks/useGameTitles";
import type { ContestFormat } from "../../../shared/types";

interface Props {
  onCreated?: () => void;
}

export function ContestCreateForm({ onCreated }: Props) {
  const createMutation = useCreateContest();
  const { data: gameTitles } = useGameTitles();
  const [name, setName] = useState("");
  const [gameTitleId, setGameTitleId] = useState("");
  const [format, setFormat] = useState<ContestFormat>("ROUND_ROBIN");
  const [bestOf, setBestOf] = useState(3);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !gameTitleId) return;
    await createMutation.mutateAsync({
      name: name.trim(),
      game_title_id: gameTitleId,
      format,
      best_of: bestOf,
    });
    setName("");
    onCreated?.();
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>コンテスト作成</h3>
      <div>
        <label>
          名前:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            aria-label="コンテスト名"
          />
        </label>
      </div>
      <div>
        <label>
          ゲームタイトル:
          <select
            value={gameTitleId}
            onChange={(e) => setGameTitleId(e.target.value)}
            required
            aria-label="ゲームタイトル"
          >
            <option value="">選択してください</option>
            {gameTitles?.map((gt) => (
              <option key={gt.game_title_id} value={gt.game_title_id}>
                {gt.name}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>
          形式:
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value as ContestFormat)}
            aria-label="形式"
          >
            <option value="ROUND_ROBIN">総当たり</option>
            <option value="SINGLE_ELIMINATION">シングルエリミネーション</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          先取本数:
          <input
            type="number"
            value={bestOf}
            onChange={(e) => setBestOf(Number(e.target.value))}
            min={1}
            step={2}
            aria-label="先取本数"
          />
        </label>
      </div>
      <button type="submit" disabled={createMutation.isPending}>
        作成
      </button>
    </form>
  );
}
