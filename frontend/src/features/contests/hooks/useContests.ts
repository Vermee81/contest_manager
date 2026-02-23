import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { contestApi, type CreateContestInput } from "../api/contestApi";
import type { ContestStatus, UUID } from "../../../shared/types";

export const CONTESTS_QUERY_KEY = ["contests"] as const;

export function contestQueryKey(contestId: UUID) {
  return [...CONTESTS_QUERY_KEY, contestId] as const;
}

export function useContests() {
  return useQuery({
    queryKey: CONTESTS_QUERY_KEY,
    queryFn: contestApi.getAll,
  });
}

export function useContest(contestId: UUID) {
  return useQuery({
    queryKey: contestQueryKey(contestId),
    queryFn: () => contestApi.getById(contestId),
    enabled: !!contestId,
  });
}

export function useCreateContest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreateContestInput) => contestApi.create(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CONTESTS_QUERY_KEY });
    },
  });
}

export function useUpdateContestStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      contestId,
      status,
    }: {
      contestId: UUID;
      status: ContestStatus;
    }) => contestApi.updateStatus(contestId, status),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: contestQueryKey(data.contest_id) });
      queryClient.invalidateQueries({ queryKey: CONTESTS_QUERY_KEY });
    },
  });
}

export function useAddPlayer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      contestId,
      name,
      seed,
    }: {
      contestId: UUID;
      name: string;
      seed?: number;
    }) => contestApi.addPlayer(contestId, name, seed),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: contestQueryKey(data.contest_id) });
    },
  });
}

export function useRemovePlayer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ contestId, playerId }: { contestId: UUID; playerId: UUID }) =>
      contestApi.removePlayer(contestId, playerId),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: contestQueryKey(data.contest_id) });
    },
  });
}
