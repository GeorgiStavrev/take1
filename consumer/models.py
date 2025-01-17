from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "user_events"
    __table_args__ = None
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[str] = mapped_column(String(80))
    user_id: Mapped[str] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[DateTime] = mapped_column(DateTime())
    processed_at: Mapped[DateTime] = mapped_column(DateTime(), default=func.now())
    properties: Mapped[List["EventProperty"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, client_id={self.client_id!r}, user_id={self.user_id!r}, name={self.name!r})"


class EventProperty(Base):
    __tablename__ = "user_event_properties"
    __table_args__ = None
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(80))
    event_id: Mapped[int] = mapped_column(ForeignKey("user_events.id"))
    event: Mapped["Event"] = relationship(back_populates="properties")

    def __repr__(self) -> str:
        return (
            f"EventProperty(id={self.id!r}, name={self.name!r}, value={self.value!r})"
        )


class UserProperty(Base):
    __tablename__ = "user_properties"
    __table_args__ = (
        UniqueConstraint("client_id", "user_id", "name", name="uc__user_prop"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[str] = mapped_column(String(80))
    user_id: Mapped[str] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(80))

    def __repr__(self) -> str:
        return f"UserProperty(id={self.id!r}, client_id={self.client_id!r}, user_id={self.user_id!r}, name={self.name!r}, value={self.value!r})"
