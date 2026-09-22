from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.memory import Memory
from app.schemas.memory import MemoryUpdate
from app.services.memory_engine import MemoryEngine


class MemoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = MemoryEngine(db)

    # =========================================================
    # CREATE MEMORY
    # =========================================================

    async def create_memory(
        self,
        content: str,
        user_id: int,
        image_url: str | None = None,
        image_name: str | None = None,
        image_data: str | None = None,
        searchable_text: str | None = None,
    ) -> Memory:

        memories = await self.engine.add_memories(
            content=content,
            user_id=user_id,
            image_url=image_url,
            image_name=image_name,
            image_data=image_data,
            searchable_text=searchable_text,
        )

        if not memories:
            raise Exception(
                "Memory could not be created."
            )

        return memories[0]

    # =========================================================
    # UPDATE MEMORY
    # =========================================================

    async def update_memory(
        self,
        memory_id: int,
        memory_in: MemoryUpdate,
        user_id: int,
    ) -> Memory:

        result = await self.db.execute(
            select(Memory).where(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
        )

        memory = result.scalar_one_or_none()

        if memory is None:
            raise NotFoundException(
                detail="Memory not found"
            )

        # -----------------------------------------------------
        # Update content
        # -----------------------------------------------------

        if memory_in.content is not None:

            embedding = (
                await self.engine.embedding_service.get_embedding(
                    memory_in.content
                )
            )

            if memory.vector_id:

                await self.engine.vector_service.update_memory(
                    vector_id=memory.vector_id,
                    embedding=embedding,
                    content=memory_in.content,
                    user_id=user_id,
                )

            memory.content = memory_in.content

        # -----------------------------------------------------
        # Update image URL
        # -----------------------------------------------------

        image_url = getattr(
            memory_in,
            "image_url",
            None
        )

        if image_url is not None:
            memory.image_url = image_url

        # -----------------------------------------------------
        # Update image name
        # -----------------------------------------------------

        image_name = getattr(
            memory_in,
            "image_name",
            None
        )

        if image_name is not None:
            memory.image_name = image_name

        # -----------------------------------------------------
        # Save changes
        # -----------------------------------------------------

        await self.db.commit()

        await self.db.refresh(memory)

        return memory

    # =========================================================
    # DELETE MEMORY
    # =========================================================

    async def delete_memory(
        self,
        memory_id: int,
        user_id: int,
    ) -> None:

        result = await self.db.execute(
            select(Memory).where(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
        )

        memory = result.scalar_one_or_none()

        if memory is None:
            raise NotFoundException(
                detail="Memory not found"
            )

        # -----------------------------------------------------
        # Delete vector from ChromaDB
        # -----------------------------------------------------

        if memory.vector_id:

            await self.engine.vector_service.delete_memory(
                memory.vector_id
            )

        # -----------------------------------------------------
        # Delete image file
        # -----------------------------------------------------

        if memory.image_url:

            import os

            image_path = memory.image_url.lstrip("/")

            if os.path.exists(image_path):

                try:

                    os.remove(image_path)

                    print(
                        "Deleted image:",
                        image_path
                    )

                except Exception as e:

                    print(
                        "Could not delete image:",
                        e
                    )

        # -----------------------------------------------------
        # Delete database record
        # -----------------------------------------------------

        await self.db.delete(memory)

        await self.db.commit()

    # =========================================================
    # SEARCH MEMORIES
    # =========================================================

    async def search_memories(
        self,
        query: str,
        user_id: int,
        limit: int = 5,
    ):

        return await self.engine.search_memories(
            query=query,
            user_id=user_id,
            limit=limit,
        )