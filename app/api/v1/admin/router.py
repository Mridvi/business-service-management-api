from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.v1.auth.dependencies import require_admin
from app.models.service_request import ServiceRequest
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.schemas.service_request import (
    ServiceRequestResponse,
    ServiceRequestStatusUpdate,
)
from app.services.service_service import ServiceService
from app.services.service_request_service import ServiceRequestService


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(require_admin)],
)

# -------------------------
# Service Management
# -------------------------

@router.post(
    "/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db),
):
    return ServiceService(db).create(data)


@router.put(
    "/services/{service_id}",
    response_model=ServiceResponse,
)
def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
):
    service = ServiceService(db).get_by_id(service_id)

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found.",
        )

    return ServiceService(db).update(service, data)


@router.delete(
    "/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = ServiceService(db).get_by_id(service_id)

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found.",
        )

    ServiceService(db).delete(service)


# -------------------------
# Service Request Management
# -------------------------

@router.get(
    "/requests",
    response_model=list[ServiceRequestResponse],
)
def list_requests(
    db: Session = Depends(get_db),
):
    return db.query(ServiceRequest).all()


@router.put(
    "/requests/{request_id}/status",
    response_model=ServiceRequestResponse,
)
def update_request_status(
    request_id: int,
    data: ServiceRequestStatusUpdate,
    db: Session = Depends(get_db),
):
    request = db.query(ServiceRequest).filter(
        ServiceRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found.",
        )

    return ServiceRequestService(db).update_status(
        request=request,
        data=data,
    )