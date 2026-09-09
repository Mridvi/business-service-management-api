from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth.dependencies import get_current_customer
from app.database.session import get_db
from app.models.customer import Customer
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestResponse,
)
from app.services.service_request_service import ServiceRequestService


router = APIRouter(
    prefix="/requests",
    tags=["Service Requests"],
)


@router.post(
    "/",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    data: ServiceRequestCreate,
    db: Session = Depends(get_db),
    customer: Customer = Depends(get_current_customer),
):
    try:
        return ServiceRequestService(db).create(
            customer_id=customer.id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[ServiceRequestResponse],
)
def get_my_requests(
    db: Session = Depends(get_db),
    customer: Customer = Depends(get_current_customer),
):
    return ServiceRequestService(db).get_customer_requests(
        customer_id=customer.id
    )


@router.get(
    "/{request_id}",
    response_model=ServiceRequestResponse,
)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    customer: Customer = Depends(get_current_customer),
):
    request = ServiceRequestService(db).get_by_id(
        request_id=request_id,
        customer_id=customer.id,
    )

    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found.",
        )

    return request