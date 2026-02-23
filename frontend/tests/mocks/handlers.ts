import { http, HttpResponse } from "msw";
import type { GameTitle, Contest, Match, Standings } from "../../src/shared/types";

const mockGameTitles: GameTitle[] = [
  { game_title_id: "gt-1", name: "Street Fighter 6" },
  { game_title_id: "gt-2", name: "Tekken 8" },
];

const mockContests: Contest[] = [
  {
    contest_id: "c-1",
    name: "SF6 Tournament",
    game_title_id: "gt-1",
    format: "ROUND_ROBIN",
    best_of: 3,
    status: "PRE_REGISTRATION",
    created_at: "2026-02-23T00:00:00",
    players: [],
  },
];

const mockMatches: Match[] = [
  {
    match_id: "m-1",
    contest_id: "c-1",
    player1_id: "p-1",
    player2_id: "p-2",
    player1_character: null,
    player2_character: null,
    player1_wins: 0,
    player2_wins: 0,
    comment: null,
    status: "PENDING",
    round: null,
    match_order: 1,
  },
];

const mockStandings: Standings = {
  contest_id: "c-1",
  entries: [
    {
      player_id: "p-1",
      player_name: "Alice",
      wins: 2,
      losses: 0,
      matches_played: 2,
      game_wins: 6,
      game_losses: 2,
    },
  ],
};

export const handlers = [
  http.get("/api/v1/game-titles", () => {
    return HttpResponse.json(mockGameTitles);
  }),

  http.post("/api/v1/game-titles", async ({ request }) => {
    const body = (await request.json()) as { name: string };
    const newTitle: GameTitle = {
      game_title_id: `gt-${Date.now()}`,
      name: body.name,
    };
    return HttpResponse.json(newTitle, { status: 201 });
  }),

  http.get("/api/v1/contests", () => {
    return HttpResponse.json(mockContests);
  }),

  http.post("/api/v1/contests", async ({ request }) => {
    const body = await request.json() as Partial<Contest>;
    const newContest: Contest = {
      contest_id: `c-${Date.now()}`,
      name: (body as { name: string }).name,
      game_title_id: (body as { game_title_id: string }).game_title_id,
      format: (body as { format: Contest["format"] }).format,
      best_of: (body as { best_of: number }).best_of,
      status: "PRE_REGISTRATION",
      created_at: new Date().toISOString(),
      players: [],
    };
    return HttpResponse.json(newContest, { status: 201 });
  }),

  http.get("/api/v1/contests/:contestId", ({ params }) => {
    const contest = mockContests.find((c) => c.contest_id === params.contestId);
    if (!contest) {
      return HttpResponse.json({ detail: "Not found" }, { status: 404 });
    }
    return HttpResponse.json(contest);
  }),

  http.patch("/api/v1/contests/:contestId/status", async ({ params, request }) => {
    const body = (await request.json()) as { status: Contest["status"] };
    const contest = mockContests.find((c) => c.contest_id === params.contestId);
    if (!contest) {
      return HttpResponse.json({ detail: "Not found" }, { status: 404 });
    }
    return HttpResponse.json({ ...contest, status: body.status });
  }),

  http.post("/api/v1/contests/:contestId/players", async ({ params, request }) => {
    const body = (await request.json()) as { name: string; seed?: number };
    const contest = mockContests.find((c) => c.contest_id === params.contestId);
    if (!contest) {
      return HttpResponse.json({ detail: "Not found" }, { status: 404 });
    }
    const updatedContest: Contest = {
      ...contest,
      players: [
        ...contest.players,
        {
          player_id: `p-${Date.now()}`,
          contest_id: contest.contest_id,
          name: body.name,
          seed: body.seed ?? null,
        },
      ],
    };
    return HttpResponse.json(updatedContest, { status: 201 });
  }),

  http.get("/api/v1/contests/:contestId/matches", () => {
    return HttpResponse.json(mockMatches);
  }),

  http.post("/api/v1/contests/:contestId/matches/generate", () => {
    return HttpResponse.json(mockMatches, { status: 201 });
  }),

  http.get("/api/v1/contests/:contestId/standings", () => {
    return HttpResponse.json(mockStandings);
  }),
];
