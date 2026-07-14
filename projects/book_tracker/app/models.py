from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass



class Book(Base):

    __tablename__ = "book"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50), nullable=False)
    category:Mapped[str | None] = mapped_column(String(50))
    total_page:Mapped[int]
    finished_page:Mapped[int] = mapped_column(default=0)

