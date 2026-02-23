# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Contest Manager** - 仲間内で格闘ゲームのコンテスト（大会）を開催するための対戦記録管理Webサービス。

### 主な機能
- コンテスト作成・管理（ラウンドロビン / シングルエリミネーション形式）
- 参加プレイヤー登録（コンテストごとに名前のみ）
- 対戦ブラケットの自動生成と手動編集
- 対戦結果の記録（使用キャラクター、スコア、コメント）
- 対戦表（ブラケット図）・順位表・試合結果一覧の表示
- 複数ゲームタイトルに対応
- 認証なし（オープンアクセス）

---

## Technology Stack

### Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x (async)
- **DB**: MySQL 8.0
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio
- **Dependency management**: uv (pyproject.toml)

### Frontend
- **Language**: TypeScript
- **Framework**: React 18
- **Build tool**: Vite
- **HTTP client**: Axios
- **State management**: TanStack Query (React Query)
- **Testing**: Vitest + React Testing Library
- **Package manager**: npm

---

## Repository Structure

```
worktrees/main/
  backend/
    pyproject.toml
    alembic/
    src/
      domain/
        contest/
          contest.py          # Aggregate Root
          player.py           # Entity
          value_objects.py    # ContestStatus, Format, BestOf
          repository.py       # Interface (Abstract)
        match/
          match.py            # Aggregate Root
          value_objects.py    # MatchStatus, CharacterName
          repository.py       # Interface (Abstract)
        game_title/
          game_title.py       # Entity
          repository.py       # Interface (Abstract)
      application/
        contest/
          commands.py         # CreateContest, UpdateStatus, AddPlayer
          queries.py          # GetContest, ListContests
          handlers.py
        match/
          commands.py         # RecordMatchResult, GenerateBracket
          queries.py          # GetMatches
          handlers.py
        standings/
          queries.py          # GetStandings
          handlers.py
      infrastructure/
        mysql/
          models.py           # SQLAlchemy ORM models
          contest_repository.py
          match_repository.py
          game_title_repository.py
        database.py           # DB接続・セッション管理
      presentation/
        api/
          routers/
            contests.py
            matches.py
            game_titles.py
            standings.py
          schemas/
            contest.py        # Pydantic schemas
            match.py
            game_title.py
            standings.py
        main.py               # FastAPIアプリケーション起動点
    tests/
      domain/
      application/
      infrastructure/
      presentation/
  frontend/
    package.json
    vite.config.ts
    src/
      features/
        contests/
          components/
          hooks/
          api/
          types/
        matches/
          components/
          hooks/
          api/
          types/
        standings/
        game-titles/
      shared/
        components/
        hooks/
        utils/
      App.tsx
      main.tsx
    tests/
```

---

## Domain Model (DDD)

### Bounded Contexts

1. **Contest Management** - コンテストとプレイヤーの管理
2. **Match Recording** - 対戦の組み合わせと結果の記録
3. **Standings** - 対戦結果からの順位計算（読み取り専用）

### Aggregates & Entities

#### Contest (Aggregate Root)
| フィールド | 型 | 説明 |
|---|---|---|
| contest_id | UUID | 識別子 |
| name | str | コンテスト名 |
| game_title_id | UUID | 使用ゲームタイトル |
| format | ContestFormat | ROUND_ROBIN / SINGLE_ELIMINATION |
| best_of | int | 先取本数（1, 3, 5, ...） |
| status | ContestStatus | PRE_REGISTRATION / IN_PROGRESS / COMPLETED |
| created_at | datetime | 作成日時 |

#### Player (Entity, Contest内)
| フィールド | 型 | 説明 |
|---|---|---|
| player_id | UUID | 識別子 |
| contest_id | UUID | 所属コンテスト |
| name | str | プレイヤー名 |
| seed | int \| None | シード順（ブラケット生成用） |

#### Match (Aggregate Root)
| フィールド | 型 | 説明 |
|---|---|---|
| match_id | UUID | 識別子 |
| contest_id | UUID | 所属コンテスト |
| player1_id | UUID | プレイヤー1 |
| player2_id | UUID | プレイヤー2 |
| player1_character | str \| None | 使用キャラクター |
| player2_character | str \| None | 使用キャラクター |
| player1_wins | int | 勝利数 |
| player2_wins | int | 勝利数 |
| comment | str \| None | コメント・メモ |
| status | MatchStatus | PENDING / COMPLETED |
| round | int \| None | ラウンド番号（トーナメント用） |
| match_order | int | 同ラウンド内の試合順序 |

#### GameTitle (Entity)
| フィールド | 型 | 説明 |
|---|---|---|
| game_title_id | UUID | 識別子 |
| name | str | ゲームタイトル名 |

### Value Objects
- `ContestFormat`: `ROUND_ROBIN` / `SINGLE_ELIMINATION`
- `ContestStatus`: `PRE_REGISTRATION` / `IN_PROGRESS` / `COMPLETED`
- `MatchStatus`: `PENDING` / `COMPLETED`

### ビジネスルール
- コンテストは `PRE_REGISTRATION` → `IN_PROGRESS` → `COMPLETED` の順にのみ遷移する
- `PRE_REGISTRATION` 中はプレイヤーの追加・削除が可能
- `IN_PROGRESS` になるとプレイヤーの変更は不可
- `IN_PROGRESS` 移行時にブラケット（試合組み合わせ）が確定する
- ブラケットの自動生成後も手動で組み合わせを編集できる（`IN_PROGRESS` 前のみ）
- ROUND_ROBIN: 全プレイヤー総当たりの試合を生成する
- SINGLE_ELIMINATION: 2の累乗に合わせてBYEを含むブラケットを生成する
- 1度 `COMPLETED` になったコンテストは変更不可

---

## API Design

### Base URL: `/api/v1`

#### Game Titles
| Method | Path | 説明 |
|---|---|---|
| GET | `/game-titles` | ゲームタイトル一覧 |
| POST | `/game-titles` | ゲームタイトル作成 |

#### Contests
| Method | Path | 説明 |
|---|---|---|
| GET | `/contests` | コンテスト一覧 |
| POST | `/contests` | コンテスト作成 |
| GET | `/contests/{contest_id}` | コンテスト詳細 |
| PATCH | `/contests/{contest_id}/status` | ステータス更新 |

#### Players
| Method | Path | 説明 |
|---|---|---|
| GET | `/contests/{contest_id}/players` | プレイヤー一覧 |
| POST | `/contests/{contest_id}/players` | プレイヤー追加 |
| DELETE | `/contests/{contest_id}/players/{player_id}` | プレイヤー削除 |

#### Matches
| Method | Path | 説明 |
|---|---|---|
| GET | `/contests/{contest_id}/matches` | 試合一覧 |
| POST | `/contests/{contest_id}/matches/generate` | ブラケット自動生成 |
| POST | `/contests/{contest_id}/matches` | 試合手動追加 |
| PATCH | `/contests/{contest_id}/matches/{match_id}` | 試合結果更新 |
| DELETE | `/contests/{contest_id}/matches/{match_id}` | 試合削除（IN_PROGRESS前のみ） |

#### Standings
| Method | Path | 説明 |
|---|---|---|
| GET | `/contests/{contest_id}/standings` | 順位表取得 |

---

## Development Commands

### Backend

```bash
# 依存関係インストール
cd backend && uv sync

# DB起動（Docker）
docker compose up -d mysql

# マイグレーション実行
cd backend && uv run alembic upgrade head

# 開発サーバー起動
cd backend && uv run uvicorn src.presentation.main:app --reload --port 8000

# テスト実行
cd backend && uv run pytest

# テスト（カバレッジ付き）
cd backend && uv run pytest --cov=src --cov-report=term-missing
```

### Frontend

```bash
# 依存関係インストール
cd frontend && npm install

# 開発サーバー起動
cd frontend && npm run dev

# テスト実行
cd frontend && npm test

# ビルド
cd frontend && npm run build
```

### Docker（全サービス起動）

```bash
docker compose up -d
```

---

## Testing Guidelines

### TDD原則（Kent Beck式）
1. **Red**: まず失敗するテストを書く
2. **Green**: テストを通す最小限の実装をする
3. **Refactor**: コードを整理する（テストは通したまま）

### Critical Requirements
- テストは必ず実際の機能を検証すること
- `assert True` / `expect(true).toBe(true)` のような意味のないアサーションは書かない
- 各テストケースは具体的な入力と期待される出力を検証すること
- モックは必要最小限に留め、実際の動作に近い形でテストすること
- テストを通すためだけのハードコードは禁止
- 本番コードに `if test_mode:` のような条件分岐を入れない
- 境界値・異常系・エラーケースも必ずテストすること
- テスト名は何をテストしているか日本語または英語で明確に記述すること

### テスト分類（Backend）
- **Domain tests**: ビジネスロジックの単体テスト（外部依存なし）
- **Application tests**: ユースケースのテスト（Repositoryはモック）
- **Infrastructure tests**: DB操作のテスト（テスト用MySQL使用）
- **Presentation tests**: APIエンドポイントのテスト（TestClient使用）

### テスト分類（Frontend）
- **Unit tests**: hooks, utils の単体テスト
- **Component tests**: React Testing Library でUIコンポーネントをテスト
- **Integration tests**: API呼び出しを含む機能テスト（MSW でモック）

---

## Architecture Notes

- **依存関係の方向**: `Presentation` → `Application` → `Domain` ← `Infrastructure`
- `Domain` 層は外部ライブラリに依存しない純粋なPythonコード
- `Infrastructure` 層が `Domain` の Repository インターフェースを実装する（依存性逆転の原則）
- `Application` 層はコマンド（書き込み）とクエリ（読み取り）を分離する（CQRS ライト）
- FastAPIのDIシステムを使って各層の依存関係を注入する
