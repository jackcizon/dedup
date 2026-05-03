from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Dedup(Base):
    hashed_data: Mapped[str] = mapped_column(String(32), primary_key=True)

    __tablename__ = "dedup"