import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.memory import Memory
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class MemoryEngine:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    # =========================================================
    # CREATE MEMORY
    # =========================================================

    async def add_memories(
        self,
        content: str,
        user_id: int,
        image_url: Optional[str] = None,
        image_name: Optional[str] = None,
    ):

        print("=" * 60)
        print("CREATE MEMORY ENGINE")
        print("Content:", content)
        print("Image name:", image_name)
        print("Image URL:", image_url)
        print("=" * 60)

        # -----------------------------------------------------
        # Create searchable content
        # -----------------------------------------------------

        searchable_content = (
            content.strip()
            if content
            else ""
        )

        # Add image name to searchable text
        if image_name:

            if searchable_content:

                searchable_content = (
                    f"{image_name} "
                    f"{searchable_content}"
                )

            else:

                searchable_content = image_name

        # Fallback for completely empty memory
        if not searchable_content:

            searchable_content = "Image memory"

        print(
            "SEARCHABLE CONTENT:",
            searchable_content
        )

        # -----------------------------------------------------
        # Generate embedding
        # -----------------------------------------------------

        print(
            "STEP 1 - Generating embedding"
        )

        embedding = (
            await self.embedding_service.get_embedding(
                searchable_content
            )
        )

        print(
            "STEP 2 - Embedding generated"
        )

        # -----------------------------------------------------
        # Create vector ID
        # -----------------------------------------------------

        vector_id = str(
            uuid.uuid4()
        )

        print(
            "VECTOR ID:",
            vector_id
        )

        # -----------------------------------------------------
        # Store in ChromaDB
        # -----------------------------------------------------

        print(
            "STEP 3 - Adding to vector database"
        )

        await self.vector_service.add_memory(
            vector_id=vector_id,
            embedding=embedding,
            content=searchable_content,
            user_id=user_id,
        )

        print(
            "STEP 4 - Added to vector database"
        )

        # -----------------------------------------------------
        # Create PostgreSQL memory
        # -----------------------------------------------------

        memory = Memory(
            content=content or searchable_content,
            user_id=user_id,
            vector_id=vector_id,
            image_url=image_url,
            image_name=image_name,
        )

        self.db.add(memory)

        print(
            "STEP 5 - Committing to PostgreSQL"
        )

        await self.db.commit()

        print(
            "STEP 6 - Refreshing object"
        )

        await self.db.refresh(memory)

        print(
            "STEP 7 - Memory created successfully"
        )

        print(
            "MEMORY ID:",
            memory.id
        )

        print("=" * 60)

        return [memory]

    # =========================================================
    # SEARCH MEMORIES
    # =========================================================

    async def search_memories(
        self,
        query: str,
        user_id: int,
        limit: int = 5,
    ):

        print("=" * 60)
        print("MEMORY SEARCH")
        print("QUERY:", query)
        print("USER ID:", user_id)
        print("=" * 60)

        # -----------------------------------------------------
        # Common words to ignore
        # -----------------------------------------------------

        stop_words = {
            "what",
            "which",
            "who",
            "where",
            "when",
            "is",
            "are",
            "am",
            "my",
            "your",
            "the",
            "a",
            "an",
            "do",
            "does",
            "did",
            "favorite",
            "favourite",
            "tell",
            "me",
            "about",
            "show",
            "give",
            "find",
            "photo",
            "photos",
            "picture",
            "pictures",
            "image",
            "images",
            "pic",
            "pics",
            "display",
            "see",
            "view",
        }

        # -----------------------------------------------------
        # Extract keywords
        # -----------------------------------------------------

        keywords = []

        for word in query.split():

            cleaned_word = (
                word
                .lower()
                .strip("?,.!'\"")
            )

            if (
                cleaned_word
                and cleaned_word not in stop_words
            ):
                keywords.append(
                    cleaned_word
                )

        print(
            "KEYWORDS:",
            keywords
        )

        # -----------------------------------------------------
        # Get user's memories
        # -----------------------------------------------------

        db_result = await self.db.execute(
            select(Memory).where(
                Memory.user_id == user_id
            )
        )

        all_memories = (
            db_result.scalars().all()
        )

        print(
            "TOTAL MEMORIES:",
            len(all_memories)
        )

        # -----------------------------------------------------
        # Keyword search
        # -----------------------------------------------------

        keyword_matches = []

        for memory in all_memories:

            content = (
                memory.content or ""
            ).lower()

            image_name = (
                memory.image_name or ""
            ).lower()

            searchable_text = (
                f"{content} {image_name}"
            )

            score = 0

            for keyword in keywords:

                if keyword in searchable_text:

                    score += 1

            if score > 0:

                keyword_matches.append(
                    (
                        score,
                        memory
                    )
                )

        # -----------------------------------------------------
        # Return keyword matches
        # -----------------------------------------------------

        if keyword_matches:

            keyword_matches.sort(
                key=lambda x: x[0],
                reverse=True
            )

            print(
                "KEYWORD MATCHES:",
                len(keyword_matches)
            )

            memories = [
                memory
                for _, memory
                in keyword_matches[:limit]
            ]

            for memory in memories:

                print(
                    "MATCH:",
                    memory.id,
                    memory.image_name,
                    memory.image_url
                )

            return memories

        # -----------------------------------------------------
        # Semantic search
        # -----------------------------------------------------

        print(
            "NO KEYWORD MATCHES"
        )

        print(
            "Using semantic search..."
        )

        embedding = (
            await self.embedding_service.get_embedding(
                query
            )
        )

        results = await self.vector_service.search(
            query_embedding=embedding,
            user_id=user_id,
            limit=limit,
        )

        print(
            "VECTOR RESULTS:",
            len(results)
        )

        memories = []

        for result in results:

            vector_id = result["id"]

            db_result = await self.db.execute(
                select(Memory).where(
                    Memory.vector_id == vector_id,
                    Memory.user_id == user_id,
                )
            )

            memory = (
                db_result.scalar_one_or_none()
            )

            if memory:

                memories.append(
                    memory
                )

        print(
            "SEMANTIC MEMORIES:",
            len(memories)
        )

        for memory in memories:

            print(
                "SEMANTIC MATCH:",
                memory.id,
                memory.image_name,
                memory.image_url
            )

        print("=" * 60)

        return memories