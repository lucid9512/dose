from datetime import datetime
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_mixin, declared_attr
from app.models import Base


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


@declarative_mixin
class BaseMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"  # 예: User → users, Post → posts


# 모든 모델에서 상속할 BaseModel
class BaseModel(Base, BaseMixin, TimestampMixin):
    __abstract__ = True
