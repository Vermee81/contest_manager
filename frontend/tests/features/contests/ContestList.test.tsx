import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ContestList } from "../../../src/features/contests/components/ContestList";

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

describe("ContestList", () => {
  it("コンテスト一覧を表示できる", async () => {
    const onSelect = vi.fn();
    renderWithQuery(<ContestList onSelectContest={onSelect} />);

    await waitFor(() => {
      expect(screen.getByText(/SF6 Tournament/)).toBeInTheDocument();
    });
  });

  it("コンテストをクリックするとコールバックが呼ばれる", async () => {
    const onSelect = vi.fn();
    renderWithQuery(<ContestList onSelectContest={onSelect} />);
    const user = userEvent.setup();

    await waitFor(() => {
      expect(screen.getByText(/SF6 Tournament/)).toBeInTheDocument();
    });

    await user.click(screen.getByText(/SF6 Tournament/));
    expect(onSelect).toHaveBeenCalledWith("c-1");
  });
});
