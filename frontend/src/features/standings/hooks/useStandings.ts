import { useQuery } from "@tanstack/react-query";
import { standingsApi } from "../api/standingsApi";
import type { UUID } from "../../../shared/types";

export function standingsQueryKey(contestId: UUID) {
  return ["contests", contestId, "standings"] as const;
}

export function useStandings(contestId: UUID) {
  return useQuery({
    queryKey: standingsQueryKey(contestId),
    queryFn: () => standingsApi.getByContest(contestId),
    enabled: !!contestId,
  });
}
