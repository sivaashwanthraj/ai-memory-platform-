from typing import List
from pathlib import Path
import uuid

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.memory import Memory as MemoryModel

from app.schemas.memory import (
    Memory as MemorySchema,
    MemoryUpdate,
    MemorySearch,
)

from app.api.deps import get_current_active_user
from app.services.memory_service import MemoryService
from app.core.exceptions import NotFoundException


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)


# ============================================================
# LIST ALL MEMORIES
# ============================================================

@router.get(
    "/",
    response_model=List[MemorySchema],
)
async def list_memories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    ),
):
    result = await db.execute(
        select(MemoryModel)
        .where(
            MemoryModel.user_id == current_user.id
        )
        .offset(skip)
        .limit(limit)
    )

    memories = result.scalars().all()

    return memories


# ============================================================
# CREATE MEMORY
#
# Supports:
#
# 1. TEXT ONLY
# 2. PHOTO ONLY
# 3. TEXT + PHOTO
#
# Endpoint:
#
# POST /api/memories/
#
# ============================================================

@router.post(
    "/",
    response_model=MemorySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_memory(
    # --------------------------------------------------------
    # Text memory
    # --------------------------------------------------------

    content: str = Form(""),

    # --------------------------------------------------------
    # Optional photo name
    # --------------------------------------------------------

    image_name: str = Form(""),

    # --------------------------------------------------------
    # Optional image
    # --------------------------------------------------------

    image: UploadFile | None = File(None),

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    db: AsyncSession = Depends(get_db),

    # --------------------------------------------------------
    # Logged-in user
    # --------------------------------------------------------

    current_user: User = Depends(
        get_current_active_user
    ),
):

    print("=" * 60)
    print("CREATE MEMORY")
    print("USER ID:", current_user.id)
    print("CONTENT:", content)
    print("IMAGE NAME:", image_name)

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    if not content.strip() and image is None:

        raise HTTPException(
            status_code=400,
            detail=(
                "Please enter a memory "
                "or select a photo."
            ),
        )

    # ========================================================
    # DEFAULT IMAGE URL
    # ========================================================

    image_url = None

    # ========================================================
    # HANDLE IMAGE
    # ========================================================

    if image is not None:

        print("=" * 60)
        print("IMAGE RECEIVED")
        print("FILENAME:", image.filename)
        print("CONTENT TYPE:", image.content_type)

        # ----------------------------------------------------
        # Allowed image types
        # ----------------------------------------------------

        allowed_types = {
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/webp",
        }

        if image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, JPEG, PNG "
                    "and WEBP images are allowed."
                ),
            )

        # ----------------------------------------------------
        # Upload directory
        #
        # D:\AI-Memory-Platform\backend\uploads\memories
        # ----------------------------------------------------

        upload_directory = Path(
            "uploads/memories"
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------------------
        # Original filename
        # ----------------------------------------------------

        original_filename = (
            image.filename or ""
        )

        # ----------------------------------------------------
        # Get extension
        # ----------------------------------------------------

        extension = Path(
            original_filename
        ).suffix.lower()

        if not extension:
            extension = ".jpg"

        # ----------------------------------------------------
        # Generate unique filename
        # ----------------------------------------------------

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        # ----------------------------------------------------
        # Complete physical file path
        # ----------------------------------------------------

        file_path = (
            upload_directory
            / unique_filename
        )

        # ----------------------------------------------------
        # Save image
        # ----------------------------------------------------

        try:

            with open(
                file_path,
                "wb",
            ) as buffer:

                while True:

                    chunk = await image.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    buffer.write(chunk)

        except Exception as e:

            print(
                "IMAGE SAVE ERROR:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail="Could not save image.",
            )

        # ----------------------------------------------------
        # URL stored in database
        # ----------------------------------------------------

        image_url = (
            f"/uploads/memories/"
            f"{unique_filename}"
        )

        # ----------------------------------------------------
        # If photo name is empty,
        # use filename without extension
        # ----------------------------------------------------

        if not image_name.strip():

            image_name = Path(
                original_filename
            ).stem

        print("IMAGE SAVED:", file_path)
        print("IMAGE URL:", image_url)
        print("IMAGE NAME:", image_name)

    # ========================================================
    # CREATE MEMORY USING MEMORY SERVICE
    # ========================================================

    service = MemoryService(db)

    memory = await service.create_memory(
        content=content,
        user_id=current_user.id,
        image_url=image_url,
        image_name=(
            image_name.strip()
            if image_name.strip()
            else None
        ),
    )

    print("=" * 60)
    print("MEMORY CREATED")
    print("MEMORY ID:", memory.id)
    print("CONTENT:", memory.content)
    print("IMAGE URL:", memory.image_url)
    print("IMAGE NAME:", memory.image_name)
    print("=" * 60)

    return memory


# ============================================================
# SEARCH MEMORIES
#
# IMPORTANT:
# Keep this BEFORE /{memory_id}
#
# Endpoint:
#
# POST /api/memories/search
#
# ============================================================

@router.post(
    "/search",
    response_model=List[MemorySchema],
)
async def search_memories(
    search_in: MemorySearch,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_active_user
    ),
):

    service = MemoryService(db)

    return await service.search_memories(
        query=search_in.query,
        user_id=current_user.id,
        limit=search_in.limit,
    )


# ============================================================
# GET ONE MEMORY
#
# Endpoint:
#
# GET /api/memories/{memory_id}
#
# ============================================================

@router.get(
    "/{memory_id}",
    response_model=MemorySchema,
)
async def get_memory(
    memory_id: int,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_active_user
    ),
):

    result = await db.execute(
        select(MemoryModel).where(
            MemoryModel.id == memory_id,
            MemoryModel.user_id == current_user.id,
        )
    )

    memory = result.scalar_one_or_none()

    if memory is None:

        raise NotFoundException(
            detail="Memory not found"
        )

    return memory


# ============================================================
# UPDATE MEMORY
#
# Endpoint:
#
# PUT /api/memories/{memory_id}
#
# ============================================================

@router.put(
    "/{memory_id}",
    response_model=MemorySchema,
)
async def update_memory(
    memory_id: int,

    memory_in: MemoryUpdate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_active_user
    ),
):

    service = MemoryService(db)

    return await service.update_memory(
        memory_id=memory_id,
        memory_in=memory_in,
        user_id=current_user.id,
    )


# ============================================================
# DELETE MEMORY
#
# Endpoint:
#
# DELETE /api/memories/{memory_id}
#
# ============================================================

@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_memory(
    memory_id: int,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_active_user
    ),
):

    service = MemoryService(db)

    await service.delete_memory(
        memory_id=memory_id,
        user_id=current_user.id,
    )

    return None