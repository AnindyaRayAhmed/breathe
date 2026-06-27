from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.api.routes.health import router as health_router
from backend.api.routes.journal_analysis import router as journal_analysis_router
from backend.api.routes.memory_update import router as memory_update_router
from backend.api.routes.onboarding import router as onboarding_router
from backend.api.routes.weekly_reflection import router as weekly_reflection_router
from backend.core.config import get_settings
from backend.core.logging import configure_logging
from backend.middleware.error_handler import register_error_handlers

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url=None,
)

register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(onboarding_router, prefix=settings.api_prefix)
app.include_router(journal_analysis_router, prefix=settings.api_prefix)
app.include_router(weekly_reflection_router, prefix=settings.api_prefix)
app.include_router(memory_update_router, prefix=settings.api_prefix)

static_dir = Path(settings.frontend_dist_dir)
index_file = static_dir / "index.html"
assets_dir = static_dir / "assets"

if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/", include_in_schema=False, response_model=None)
def serve_root() -> FileResponse | JSONResponse:
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Breathe API is running. Build the frontend to serve the UI.",
        },
    )


@app.get("/{path:path}", include_in_schema=False, response_model=None)
def serve_frontend(path: str) -> FileResponse | JSONResponse:
    if path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    candidate = static_dir / path
    if candidate.is_file():
        return FileResponse(candidate)

    if index_file.exists():
        return FileResponse(index_file)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Breathe API is running. Build the frontend to serve the UI.",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )
