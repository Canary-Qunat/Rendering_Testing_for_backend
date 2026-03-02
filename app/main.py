from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.infrastructure.database.connection import (
    connect_to_db,
    close_db_connection,
)

from app.presentation.api.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    # Startup
    await connect_to_db()
    yield
    # Shutdown
    await close_db_connection()


def create_app(use_lifespan: bool = True) -> FastAPI:
    application = FastAPI(
        title="Canary Backend",
        version="1.0.0",
        lifespan=lifespan if use_lifespan else None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(auth_router)

    return application


app = create_app()

