from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.config import settings
from app.core.exceptions import ConflictException, CredentialsException
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    User as UserSchema,
    Token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# -----------------------------
# Register
# -----------------------------
@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == user_in.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ConflictException(detail="Email already registered")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


# -----------------------------
# Login
# -----------------------------
@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise CredentialsException()

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise CredentialsException()

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# -----------------------------
# Current User
# -----------------------------
@router.get(
    "/me",
    response_model=UserSchema,
)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user