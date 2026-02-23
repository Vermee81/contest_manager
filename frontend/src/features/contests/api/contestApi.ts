import apiClient from "../../../shared/api/client";
import type { Contest, ContestFormat, ContestStatus, Player, UUID } from "../../../shared/types";

export interface CreateContestInput {
  name: string;
  game_title_id: UUID;
  format: ContestFormat;
  best_of: number;
}

export const contestApi = {
  getAll: async (): Promise<Contest[]> => {
    const { data } = await apiClient.get<Contest[]>("/contests");
    return data;
  },

  getById: async (contestId: UUID): Promise<Contest> => {
    const { data } = await apiClient.get<Contest>(`/contests/${contestId}`);
    return data;
  },

  create: async (input: CreateContestInput): Promise<Contest> => {
    const { data } = await apiClient.post<Contest>("/contests", input);
    return data;
  },

  updateStatus: async (contestId: UUID, status: ContestStatus): Promise<Contest> => {
    const { data } = await apiClient.patch<Contest>(`/contests/${contestId}/status`, { status });
    return data;
  },

  getPlayers: async (contestId: UUID): Promise<Player[]> => {
    const { data } = await apiClient.get<Player[]>(`/contests/${contestId}/players`);
    return data;
  },

  addPlayer: async (contestId: UUID, name: string, seed?: number): Promise<Contest> => {
    const { data } = await apiClient.post<Contest>(`/contests/${contestId}/players`, {
      name,
      seed: seed ?? null,
    });
    return data;
  },

  removePlayer: async (contestId: UUID, playerId: UUID): Promise<Contest> => {
    const { data } = await apiClient.delete<Contest>(
      `/contests/${contestId}/players/${playerId}`
    );
    return data;
  },
};
