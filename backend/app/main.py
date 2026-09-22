import os
import base64
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from sqlalchemy import select

from app.config import settings
from app.api import auth, memories, chatbot
from app.database import engine, Base, AsyncSessionLocal
from app.models.memory import Memory


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

os.makedirs("uploads/memories", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)


@app.get("/uploads/memories/{filename}")
async def serve_memory_image_by_filename(filename: str):
    """
    Serve uploaded images:
    1. If file exists on disk, serve directly via FileResponse.
    2. If file was deleted by Render restart, load permanently from Neon DB!
    """
    file_path = os.path.join("uploads", "memories", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Memory).where(Memory.image_url.like(f"%{filename}%"))
            )
            memory = result.scalars().first()
            if memory and memory.image_data:
                header, b64_content = memory.image_data.split(",", 1)
                media_type = header.split(";")[0].replace("data:", "")
                image_bytes = base64.b64decode(b64_content)
                resp_headers = {"Cache-Control": "public, max-age=31536000"}
                if media_type == "application/pdf" or filename.lower().endswith(".pdf"):
                    resp_headers["Content-Disposition"] = f'inline; filename="{filename}"'
                return Response(
                    content=image_bytes,
                    media_type=media_type,
                    headers=resp_headers,
                )
    except Exception as e:
        print("Error serving image/PDF from DB fallback:", repr(e))

    return Response(
        content='{"detail":"Not Found"}',
        status_code=404,
        media_type="application/json",
    )


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