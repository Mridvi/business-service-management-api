from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.role import Role


class CustomerRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )

    def get_by_id(self, customer_id: int) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update(self, customer: Customer) -> Customer:
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_all_admin(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> list[Customer]:
        query = (
            self.db.query(Customer)
            .options(joinedload(Customer.role))
            .order_by(Customer.created_at.desc())
        )

        if search:
            term = f"%{search}%"
            query = query.filter(
                or_(
                    Customer.email.ilike(term),
                    Customer.first_name.ilike(term),
                    Customer.last_name.ilike(term),
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_by_id_with_role(self, customer_id: int) -> Customer | None:
        return (
            self.db.query(Customer)
            .options(joinedload(Customer.role))
            .filter(Customer.id == customer_id)
            .first()
        )

    def count_all(self) -> int:
        return self.db.query(func.count(Customer.id)).scalar() or 0

    def count_admins(self) -> int:
        return (
            self.db.query(func.count(Customer.id))
            .join(Role)
            .filter(Role.name == "Administrator")
            .scalar()
            or 0
        )