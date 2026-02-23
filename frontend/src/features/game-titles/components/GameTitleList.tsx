import { useState } from "react";
import { useGameTitles, useCreateGameTitle } from "../hooks/useGameTitles";

export function GameTitleList() {
  const { data: gameTitles, isLoading, isError } = useGameTitles();
  const createMutation = useCreateGameTitle();
  const [newName, setNewName] = useState("");

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    await createMutation.mutateAsync(newName.trim());
    setNewName("");
  };

  if (isLoading) return <p>読み込み中...</p>;
  if (isError) return <p>エラーが発生しました</p>;

  return (
    <div>
      <h2>ゲームタイトル一覧</h2>
      <form onSubmit={handleCreate}>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="ゲームタイトル名"
          aria-label="ゲームタイトル名"
        />
        <button type="submit" disabled={createMutation.isPending}>
          追加
        </button>
      </form>
      <ul>
        {gameTitles?.map((gt) => (
          <li key={gt.game_title_id}>{gt.name}</li>
        ))}
      </ul>
    </div>
  );
}
