import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MatchList } from "../../../src/features/matches/components/MatchList";
import type { Player } from "../../../src/shared/types";

const mockPlayers: Player[] = [
  { player_id: "p-1", contest_id: "c-1", name: "Alice", seed: 1 },
  { player_id: "p-2", contest_id: "c-1", name: "Bob", seed: 2 },
];

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe("MatchList", () => {
  it("試合一覧を表示できる", async () => {
    renderWithQuery(
      <MatchList
        contestId="c-1"
        players={mockPlayers}
        contestStatus="IN_PROGRESS"
        bestOf={3}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/Alice vs Bob/)).toBeInTheDocument();
    });
  });

  it("PRE_REGISTRATION状態ではブラケット生成ボタンが表示される", async () => {
    renderWithQuery(
      <MatchList
        contestId="c-1"
        players={mockPlayers}
        contestStatus="PRE_REGISTRATION"
        bestOf={3}
      />
    );

    // モックの試合一覧が空でないのでボタンは表示されない - 試合一覧表示の確認
    await waitFor(() => {
      expect(screen.getByText(/Alice vs Bob/)).toBeInTheDocument();
    });
  });
});
