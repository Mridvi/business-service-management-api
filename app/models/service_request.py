import enum

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import TimestampMixin


class ServiceRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ServiceRequestPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class ServiceRequest(Base, TimestampMixin):
    __tablename__ = "service_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ServiceRequestStatus] = mapped_column(
        Enum(ServiceRequestStatus),
        default=ServiceRequestStatus.PENDING,
        nullable=False,
    )

    priority: Mapped[ServiceRequestPriority] = mapped_column(
        Enum(ServiceRequestPriority),
        default=ServiceRequestPriority.MEDIUM,
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="service_requests"
    )

    service: Mapped["Service"] = relationship(
        back_populates="requests"
    )