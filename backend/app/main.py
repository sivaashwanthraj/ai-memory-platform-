from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.api import auth, memories, chatbot
from app.database import engine, Base


# ============================================================
# DATABASE LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables when application starts
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    yield

    # Application shutdown
    # Add cleanup code here if needed


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    redirect_slashes=False,
)


# ============================================================
# SERVE UPLOADED IMAGES
# ============================================================
# IMPORTANT:
# Your uploaded images are saved inside:
#
# backend/uploads/memories/
#
# This makes them accessible through:
#
# http://127.0.0.1:8000/uploads/memories/filename.jpg
#
# ============================================================

import os

os.makedirs("uploads/memories", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.cors_origins_list,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
)

app.include_router(
    memories.router,
    prefix=settings.API_V1_STR,
)

app.include_router(
    chatbot.router,
    prefix=settings.API_V1_STR,
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():

    return {
        "message": "Welcome to AI Memory Platform API"
    }