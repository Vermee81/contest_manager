export type UUID = string;

export type ContestFormat = "ROUND_ROBIN" | "SINGLE_ELIMINATION";
export type ContestStatus = "PRE_REGISTRATION" | "IN_PROGRESS" | "COMPLETED";
export type MatchStatus = "PENDING" | "COMPLETED";

export interface GameTitle {
  game_title_id: UUID;
  name: string;
}

export interface Player {
  player_id: UUID;
  contest_id: UUID;
  name: string;
  seed: number | null;
}

export interface Contest {
  contest_id: UUID;
  name: string;
  game_title_id: UUID;
  format: ContestFormat;
  best_of: number;
  status: ContestStatus;
  created_at: string;
  players: Player[];
}

export interface Match {
  match_id: UUID;
  contest_id: UUID;
  player1_id: UUID;
  player2_id: UUID;
  player1_character: string | null;
  player2_character: string | null;
  player1_wins: number;
  player2_wins: number;
  comment: string | null;
  status: MatchStatus;
  round: number | null;
  match_order: number;
}

export interface StandingsEntry {
  player_id: UUID;
  player_name: string;
  wins: number;
  losses: number;
  matches_played: number;
  game_wins: number;
  game_losses: number;
}

export interface Standings {
  contest_id: UUID;
  entries: StandingsEntry[];
}
