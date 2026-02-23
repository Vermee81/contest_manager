import apiClient from "../../../shared/api/client";
import type { Match, UUID } from "../../../shared/types";

export interface RecordMatchResultInput {
  player1_character?: string | null;
  player2_character?: string | null;
  player1_wins: number;
  player2_wins: number;
  comment?: string | null;
}

export interface AddMatchInput {
  player1_id: UUID;
  player2_id: UUID;
  round?: number | null;
  match_order: number;
}

export const matchApi = {
  getByContest: async (contestId: UUID): Promise<Match[]> => {
    const { data } = await apiClient.get<Match[]>(
      `/contests/${contestId}/matches`
    );
    return data;
  },

  generateBracket: async (contestId: UUID): Promise<Match[]> => {
    const { data } = await apiClient.post<Match[]>(
      `/contests/${contestId}/matches/generate`
    );
    return data;
  },

  addMatch: async (contestId: UUID, input: AddMatchInput): Promise<Match> => {
    const { data } = await apiClient.post<Match>(
      `/contests/${contestId}/matches`,
      input
    );
    return data;
  },

  recordResult: async (
    contestId: UUID,
    matchId: UUID,
    input: RecordMatchResultInput
  ): Promise<Match> => {
    const { data } = await apiClient.patch<Match>(
      `/contests/${contestId}/matches/${matchId}`,
      input
    );
    return data;
  },

  deleteMatch: async (contestId: UUID, matchId: UUID): Promise<void> => {
    await apiClient.delete(`/contests/${contestId}/matches/${matchId}`);
  },
};
