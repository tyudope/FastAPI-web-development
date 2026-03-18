from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.task import Task


class Routine(Base):
    __tablename__ = "routines"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    goal_id: Mapped[int] = mapped_column(
        ForeignKey("goals.id"),
        unique=True,
        nullable=False
    )

    goal: Mapped[Goal] = relationship(
        "Goal",
        back_populates="routine"
    )

    tasks: Mapped[list[Task]] = relationship(
        "Task",
        back_populates="routine",
        cascade="all, delete-orphan"
    )