import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StandingsTable } from "../../../src/features/standings/components/StandingsTable";

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

describe("StandingsTable", () => {
  it("順位表を表示できる", async () => {
    renderWithQuery(<StandingsTable contestId="c-1" />);

    await waitFor(() => {
      expect(screen.getByText("順位表")).toBeInTheDocument();
      expect(screen.getByText("Alice")).toBeInTheDocument();
    });

    // 順位列のヘッダーを確認
    expect(screen.getByText("勝")).toBeInTheDocument();
    expect(screen.getByText("負")).toBeInTheDocument();
  });

  it("Aliceの勝利数が正しく表示される", async () => {
    renderWithQuery(<StandingsTable contestId="c-1" />);

    await waitFor(() => {
      expect(screen.getByText("Alice")).toBeInTheDocument();
    });

    const rows = screen.getAllByRole("row");
    // ヘッダー行を除くデータ行
    const aliceRow = rows[1];
    expect(aliceRow).toHaveTextContent("Alice");
    expect(aliceRow).toHaveTextContent("2"); // wins
    expect(aliceRow).toHaveTextContent("0"); // losses
  });
});
