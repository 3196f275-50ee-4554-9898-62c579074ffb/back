from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy.sql import expression
from sqlalchemy import Integer, Float
class utcnow(expression.FunctionElement):
    type = DateTime
    inherit_cache = True
@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Penalty(Base):
    __tablename__ = "penalties"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[int] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow())

class PenaltyBuilding(Base):
    __tablename__ = "penalty_buildings"
    penalty_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("penalties.id"), primary_key=True)
    building_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buildings.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow())

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    building_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buildings.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow())


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    building_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buildings.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow())
