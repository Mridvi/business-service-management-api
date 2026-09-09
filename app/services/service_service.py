from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ServiceCreate) -> Service:
        service = Service(
            name=data.name,
            description=data.description,
            price=data.price,
            is_active=data.is_active,
        )

        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)

        return service

    def get_all(self) -> list[Service]:
        return (
            self.db.query(Service)
            .filter(Service.is_active == True)
            .all()
        )

    def get_by_id(self, service_id: int) -> Service | None:
        return (
            self.db.query(Service)
            .filter(Service.id == service_id)
            .first()
        )

    def update(
        self,
        service: Service,
        data: ServiceUpdate,
    ) -> Service:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(service, field, value)

        self.db.commit()
        self.db.refresh(service)

        return service

    def delete(self, service: Service) -> None:
        service.is_active = False
        self.db.commit()