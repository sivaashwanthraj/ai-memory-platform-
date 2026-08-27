from sqlalchemy.ext.asyncio import AsyncSession

from app.services.memory_service import MemoryService
from app.services.llm_service import LLMService


class ChatbotService:

    def __init__(self, db: AsyncSession):

        self.memory_service = MemoryService(db)
        self.llm_service = LLMService()

    # =========================================================
    # CHAT
    # =========================================================

    async def chat(
        self,
        message: str,
        user_id: int,
    ):

        print("=" * 60)
        print("CHATBOT")
        print("USER ID:", user_id)
        print("MESSAGE:", message)
        print("=" * 60)

        # =====================================================
        # SEARCH USER MEMORIES
        # =====================================================

        memories = await self.memory_service.search_memories(
            query=message,
            user_id=user_id,
            limit=5,
        )

        print(
            "MEMORIES FOUND:",
            len(memories)
        )

        # =====================================================
        # NO MEMORY FOUND
        # =====================================================

        if not memories:

            return {
                "answer": (
                    "I don't know because it isn't in my memory."
                ),
                "image_url": None,
                "image_name": None,
            }

        # =====================================================
        # PRINT FOUND MEMORIES
        # =====================================================

        for memory in memories:

            print(
                "MEMORY ID:",
                memory.id
            )

            print(
                "CONTENT:",
                memory.content
            )

            print(
                "IMAGE NAME:",
                memory.image_name
            )

            print(
                "IMAGE URL:",
                memory.image_url
            )

            print("-" * 40)

        # =====================================================
        # BUILD LLM CONTEXT
        # =====================================================

        context = ""

        for memory in memories:

            context += (
                f"Memory ID: {memory.id}\n"
                f"Content: {memory.content or ''}\n"
                f"Image Name: {memory.image_name or ''}\n"
                f"Image URL: {memory.image_url or ''}\n"
                f"-------------------------\n"
            )

        # =====================================================
        # FIND RELEVANT IMAGE
        # =====================================================

        image_url = None
        image_name = None

        message_lower = message.lower()

        # -----------------------------------------------------
        # First try to find an image whose name matches
        # something in the user's question.
        # -----------------------------------------------------

        for memory in memories:

            if not memory.image_url:
                continue

            memory_image_name = (
                memory.image_name or ""
            ).lower()

            if (
                memory_image_name
                and memory_image_name in message_lower
            ):

                image_url = memory.image_url
                image_name = memory.image_name

                print(
                    "MATCHING IMAGE FOUND"
                )

                print(
                    "IMAGE NAME:",
                    image_name
                )

                print(
                    "IMAGE URL:",
                    image_url
                )

                break

        # -----------------------------------------------------
        # If no exact image-name match was found,
        # use the first image returned by search.
        # -----------------------------------------------------

        if image_url is None:

            for memory in memories:

                if memory.image_url:

                    image_url = memory.image_url
                    image_name = memory.image_name

                    print(
                        "FIRST IMAGE MEMORY FOUND"
                    )

                    print(
                        "IMAGE NAME:",
                        image_name
                    )

                    print(
                        "IMAGE URL:",
                        image_url
                    )

                    break

        # =====================================================
        # QWEN3 PROMPT
        # =====================================================

        prompt = f"""
You are an intelligent AI Memory Assistant.

You have access to the user's saved memories.

Use ONLY the memories below to answer the user's question.

Do not invent information.

If the answer is not present in the memories,
reply exactly:

"I don't know because it isn't in my memory."

If the user asks about a photo or image,
use the matching memory and image name when available.

-------------------------
USER MEMORIES
-------------------------

{context}

-------------------------
USER QUESTION
-------------------------

{message}

-------------------------
ANSWER
-------------------------
"""

        # =====================================================
        # SEND TO QWEN3
        # =====================================================

        answer = await self.llm_service.generate(
            prompt
        )

        print(
            "AI ANSWER:",
            answer
        )

        print(
            "FINAL IMAGE URL:",
            image_url
        )

        print(
            "FINAL IMAGE NAME:",
            image_name
        )

        # =====================================================
        # RETURN RESPONSE
        # =====================================================

        return {

            "answer": answer,

            "image_url": image_url,

            "image_name": image_name,

        }