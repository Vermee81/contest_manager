import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GameTitleList } from "../../../src/features/game-titles/components/GameTitleList";

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

describe("GameTitleList", () => {
  it("ゲームタイトル一覧を表示できる", async () => {
    renderWithQuery(<GameTitleList />);

    await waitFor(() => {
      expect(screen.getByText("Street Fighter 6")).toBeInTheDocument();
      expect(screen.getByText("Tekken 8")).toBeInTheDocument();
    });
  });

  it("新しいゲームタイトルを追加できる", async () => {
    renderWithQuery(<GameTitleList />);
    const user = userEvent.setup();

    // データ読み込み完了を待つ
    await waitFor(() => {
      expect(screen.getByText("Street Fighter 6")).toBeInTheDocument();
    });

    const input = screen.getByLabelText("ゲームタイトル名");
    const button = screen.getByRole("button", { name: "追加" });

    await user.type(input, "Guilty Gear");
    await user.click(button);

    // フォームがクリアされる
    await waitFor(() => {
      expect(input).toHaveValue("");
    });
  });
});
