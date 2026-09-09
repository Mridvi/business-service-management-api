from pydantic import BaseModel

from app.models.service_request import (
    ServiceRequestPriority,
    ServiceRequestStatus,
)


class ServiceRequestCreate(BaseModel):
    service_id: int
    description: str | None = None
    priority: ServiceRequestPriority = ServiceRequestPriority.MEDIUM


class ServiceRequestStatusUpdate(BaseModel):
    status: ServiceRequestStatus


class ServiceRequestResponse(BaseModel):
    id: int
    customer_id: int
    service_id: int
    description: str | None
    status: ServiceRequestStatus
    priority: ServiceRequestPriority

    class Config:
        from_attributes = True