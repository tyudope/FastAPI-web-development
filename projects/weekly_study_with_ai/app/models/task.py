from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.routine import Routine


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)

    routine_id: Mapped[int] = mapped_column(
        ForeignKey("routines.id"),
        nullable=False
    )

    routine: Mapped[Routine] = relationship(
        "Routine",
        back_populates="tasks"
    ) 