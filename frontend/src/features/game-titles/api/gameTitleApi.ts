import apiClient from "../../../shared/api/client";
import type { GameTitle } from "../../../shared/types";

export const gameTitleApi = {
  getAll: async (): Promise<GameTitle[]> => {
    const { data } = await apiClient.get<GameTitle[]>("/game-titles");
    return data;
  },

  create: async (name: string): Promise<GameTitle> => {
    const { data } = await apiClient.post<GameTitle>("/game-titles", { name });
    return data;
  },
};
