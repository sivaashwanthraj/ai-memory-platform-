from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    vector_id = Column(
        String,
        unique=True,
        nullable=True
    )

    # =========================
    # PHOTO MEMORY SUPPORT
    # =========================

    image_url = Column(
        String,
        nullable=True
    )

    image_name = Column(
        String,
        nullable=True
    )

    image_data = Column(
        Text,
        nullable=True
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # =========================
    # USER RELATIONSHIP
    # =========================

    owner = relationship(
        "User",
        back_populates="memories"
    )