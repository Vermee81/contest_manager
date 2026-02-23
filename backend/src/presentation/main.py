"""FastAPI アプリケーション起動点"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.application.contest.handlers import ContestNotFoundError
from src.domain.contest.contest import ContestModificationError
from src.domain.contest.value_objects import InvalidStatusTransitionError
from src.presentation.api.routers import contests, game_titles, matches, standings

app = FastAPI(title="Contest Manager API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_titles.router, prefix="/api/v1")
app.include_router(contests.router, prefix="/api/v1")
app.include_router(matches.router, prefix="/api/v1")
app.include_router(standings.router, prefix="/api/v1")


@app.exception_handler(ContestNotFoundError)
async def contest_not_found_handler(
    request: Request, exc: ContestNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidStatusTransitionError)
async def invalid_transition_handler(
    request: Request, exc: InvalidStatusTransitionError
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(ContestModificationError)
async def modification_error_handler(
    request: Request, exc: ContestModificationError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
