import apiClient from "../../../shared/api/client";
import type { Standings, UUID } from "../../../shared/types";

export const standingsApi = {
  getByContest: async (contestId: UUID): Promise<Standings> => {
    const { data } = await apiClient.get<Standings>(
      `/contests/${contestId}/standings`
    );
    return data;
  },
};
