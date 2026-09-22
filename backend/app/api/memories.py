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
    Response,
)
from fastapi.responses import FileResponse
import base64
import io
import os

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
    image_data = None
    searchable_text = None

    # ========================================================
    # HANDLE IMAGE
    # ========================================================

    if image is not None:

        print("=" * 60)
        print("IMAGE RECEIVED")
        print("FILENAME:", image.filename)
        print("CONTENT TYPE:", image.content_type)

        # ----------------------------------------------------
        # Allowed file types (Images + PDF Documents)
        # ----------------------------------------------------

        allowed_types = {
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/webp",
            "application/pdf",
        }

        if image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, JPEG, PNG, WEBP images "
                    "and PDF documents are allowed."
                ),
            )

        # ----------------------------------------------------
        # Upload directory
        # ----------------------------------------------------

        upload_directory = Path(
            "uploads/memories"
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        original_filename = (
            image.filename or ""
        )

        extension = Path(
            original_filename
        ).suffix.lower()

        if not extension:
            extension = ".pdf" if image.content_type == "application/pdf" else ".jpg"

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        file_path = (
            upload_directory
            / unique_filename
        )

        # ----------------------------------------------------
        # Read and process file for persistent cloud storage
        # ----------------------------------------------------

        image_bytes = await image.read()
        is_pdf = (extension == ".pdf" or image.content_type == "application/pdf")

        if is_pdf:
            proc_bytes = image_bytes
            mime_type = "application/pdf"
            b64_str = base64.b64encode(image_bytes).decode("utf-8")
            image_data = f"data:application/pdf;base64,{b64_str}"

            # Extract text from PDF with pypdf
            extracted_pdf_text = ""
            try:
                import pypdf

                pdf_reader = pypdf.PdfReader(io.BytesIO(image_bytes))
                pdf_text_parts = []
                for page in pdf_reader.pages:
                    text_extracted = page.extract_text()
                    if text_extracted:
                        pdf_text_parts.append(text_extracted.strip())
                extracted_pdf_text = "\n".join(pdf_text_parts).strip()
                print(f"Extracted {len(extracted_pdf_text)} characters from PDF")
            except Exception as e:
                print("PDF text extraction error:", repr(e))

            # Keep memory content clean, do not dump raw words into user card!
            doc_label = image_name.strip() if image_name.strip() else Path(original_filename).stem
            if not content.strip():
                content = doc_label
            searchable_text = f"{doc_label}\n{content}\n{extracted_pdf_text[:4000]}"

        else:
            try:
                from PIL import Image

                img = Image.open(io.BytesIO(image_bytes))
                save_format = "PNG" if img.mode in ("RGBA", "P") else "JPEG"
                if save_format == "JPEG" and img.mode != "RGB":
                    img = img.convert("RGB")

                # Max dimension 1920 to keep size small (~150-300kb)
                img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)

                buf = io.BytesIO()
                if save_format == "JPEG":
                    img.save(buf, format="JPEG", quality=85, optimize=True)
                    mime_type = "image/jpeg"
                else:
                    img.save(buf, format="PNG", optimize=True)
                    mime_type = "image/png"

                proc_bytes = buf.getvalue()
                b64_str = base64.b64encode(proc_bytes).decode("utf-8")
                image_data = f"data:{mime_type};base64,{b64_str}"

            except Exception as e:
                print("Pillow processing error, fallback to raw bytes:", repr(e))
                proc_bytes = image_bytes
                mime_type = image.content_type or "image/jpeg"
                b64_str = base64.b64encode(image_bytes).decode("utf-8")
                image_data = f"data:{mime_type};base64,{b64_str}"

        # ----------------------------------------------------
        # Cache file locally on disk
        # ----------------------------------------------------

        try:
            with open(file_path, "wb") as buffer:
                buffer.write(proc_bytes)
        except Exception as e:
            print("Local cache write error (continuing with DB storage):", repr(e))

        image_url = (
            f"/uploads/memories/"
            f"{unique_filename}"
        )

        if not image_name.strip():
            image_name = Path(
                original_filename
            ).stem

        print("IMAGE SAVED:", file_path)
        print("IMAGE URL:", image_url)
        print("IMAGE NAME:", image_name)
        print("IMAGE DATA LENGTH:", len(image_data) if image_data else 0)

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
        image_data=image_data,
        searchable_text=searchable_text,
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


# ============================================================
# GET MEMORY IMAGE
# ============================================================

@router.get(
    "/{memory_id}/image",
)
async def get_memory_image(
    memory_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MemoryModel).where(MemoryModel.id == memory_id)
    )
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found",
        )

    # 1. First priority: load from database base64 (permanent, survives all server restarts)
    if memory.image_data:
        try:
            header, b64_content = memory.image_data.split(",", 1)
            media_type = header.split(";")[0].replace("data:", "")
            image_bytes = base64.b64decode(b64_content)
            resp_headers = {
                "Cache-Control": "public, max-age=31536000",
            }
            if media_type == "application/pdf":
                safe_name = (memory.image_name or "document").replace('"', '') + ".pdf"
                resp_headers["Content-Disposition"] = f'inline; filename="{safe_name}"'
            return Response(
                content=image_bytes,
                media_type=media_type,
                headers=resp_headers,
            )
        except Exception as e:
            print("Error decoding image_data:", repr(e))

    # 2. Second priority: load from local disk if present
    if memory.image_url:
        disk_path = memory.image_url.lstrip("/")
        if os.path.exists(disk_path):
            return FileResponse(disk_path)

    raise HTTPException(
        status_code=404,
        detail="Image file not found.",
    )