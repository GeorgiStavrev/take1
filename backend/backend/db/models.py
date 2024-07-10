from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Event(Base):
    __tablename__ = "user_events"
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
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[str] = mapped_column(String(80))
    user_id: Mapped[str] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(80))

    def __repr__(self) -> str:
        return f"UserProperty(id={self.id!r}, client_id={self.client_id!r}, user_id={self.user_id!r}, name={self.name!r}, value={self.value!r})"
