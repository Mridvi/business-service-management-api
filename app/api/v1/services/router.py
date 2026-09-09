from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.service import ServiceResponse
from app.services.service_service import ServiceService


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.get(
    "/",
    response_model=list[ServiceResponse],
)
def get_services(
    db: Session = Depends(get_db),
):
    return ServiceService(db).get_all()


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = ServiceService(db).get_by_id(service_id)

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found.",
        )

    return service