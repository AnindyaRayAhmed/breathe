from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    @app.middleware("http")
    async def safe_error_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled server error", extra={"path": request.url.path})
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected server error occurred."},
            )
