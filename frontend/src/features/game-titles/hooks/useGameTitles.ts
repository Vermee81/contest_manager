import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { gameTitleApi } from "../api/gameTitleApi";

export const GAME_TITLES_QUERY_KEY = ["game-titles"] as const;

export function useGameTitles() {
  return useQuery({
    queryKey: GAME_TITLES_QUERY_KEY,
    queryFn: gameTitleApi.getAll,
  });
}

export function useCreateGameTitle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (name: string) => gameTitleApi.create(name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: GAME_TITLES_QUERY_KEY });
    },
  });
}
