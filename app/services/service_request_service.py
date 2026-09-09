from sqlalchemy.orm import Session

from app.models.service import Service
from app.models.service_request import ServiceRequest, ServiceRequestStatus
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestStatusUpdate,
)


class ServiceRequestService:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        customer_id: int,
        data: ServiceRequestCreate,
    ) -> ServiceRequest:

        service = (
            self.db.query(Service)
            .filter(
                Service.id == data.service_id,
                Service.is_active == True,
            )
            .first()
        )

        if not service:
            raise ValueError("Service not found or inactive.")

        request = ServiceRequest(
        customer_id=customer_id,
        service_id=data.service_id,
        description=data.description,
        status=ServiceRequestStatus.PENDING,
        priority=data.priority,
    )

        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)

        return request

    def get_customer_requests(
        self,
        customer_id: int,
    ) -> list[ServiceRequest]:

        return (
            self.db.query(ServiceRequest)
            .filter(ServiceRequest.customer_id == customer_id)
            .all()
        )

    def get_by_id(
        self,
        request_id: int,
        customer_id: int,
    ) -> ServiceRequest | None:

        return (
            self.db.query(ServiceRequest)
            .filter(
                ServiceRequest.id == request_id,
                ServiceRequest.customer_id == customer_id,
            )
            .first()
        )

    def update_status(
        self,
        request: ServiceRequest,
        data: ServiceRequestStatusUpdate,
    ) -> ServiceRequest:

        request.status = data.status

        self.db.commit()
        self.db.refresh(request)

        return request