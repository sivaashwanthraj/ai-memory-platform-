from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chatbot_service import ChatbotService
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    chatbot_service = ChatbotService(db)

    response = await chatbot_service.chat(
        message=request.message,
        user_id=current_user.id,
    )

    print("=" * 60)
    print("CHATBOT RESPONSE:")
    print(response)
    print("=" * 60)

    return ChatResponse(
        answer=response.get(
            "answer",
            "I don't know because it isn't in my memory."
        ),
        image_url=response.get("image_url"),
        image_name=response.get("image_name"),
    )