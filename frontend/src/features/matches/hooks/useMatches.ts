import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { matchApi, type RecordMatchResultInput } from "../api/matchApi";
import type { UUID } from "../../../shared/types";

export function matchesQueryKey(contestId: UUID) {
  return ["contests", contestId, "matches"] as const;
}

export function useMatches(contestId: UUID) {
  return useQuery({
    queryKey: matchesQueryKey(contestId),
    queryFn: () => matchApi.getByContest(contestId),
    enabled: !!contestId,
  });
}

export function useGenerateBracket() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (contestId: UUID) => matchApi.generateBracket(contestId),
    onSuccess: (_data, contestId) => {
      queryClient.invalidateQueries({ queryKey: matchesQueryKey(contestId) });
    },
  });
}

export function useRecordMatchResult() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      contestId,
      matchId,
      input,
    }: {
      contestId: UUID;
      matchId: UUID;
      input: RecordMatchResultInput;
    }) => matchApi.recordResult(contestId, matchId, input),
    onSuccess: (_data, { contestId }) => {
      queryClient.invalidateQueries({ queryKey: matchesQueryKey(contestId) });
    },
  });
}

export function useDeleteMatch() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ contestId, matchId }: { contestId: UUID; matchId: UUID }) =>
      matchApi.deleteMatch(contestId, matchId),
    onSuccess: (_data, { contestId }) => {
      queryClient.invalidateQueries({ queryKey: matchesQueryKey(contestId) });
    },
  });
}
