from sqlalchemy import String, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm  import Mapped, mapped_column

from app.db.base import Base
from enum import Enum

class PhaseOfDay(str, Enum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"


class Order(Base):

    __tablename__ = "orders"


    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    meal_name: Mapped[str] = mapped_column(String(100), nullable=False )
    phase_of_day: Mapped[PhaseOfDay] = mapped_column(SAEnum(PhaseOfDay), nullable=False)
    cuisine: Mapped[str] = mapped_column(String(50), nullable=False)
    price_level: Mapped[int] = mapped_column(Integer, nullable=False)