# Ecommerce API

REST E-commerce API built with **FastAPI**. It exposes authentication, user profile, catalog, cart, orders, addresses, payment methods, and an admin panel.

Designed to be consumed by any HTTP client: Swagger UI, Postman, mobile apps, or future frontends.

---

## Features

- User registration, JWT login (access + refresh), and password reset
- Authenticated user profile (`/users/profile` and `/auth/me`)
- Public product and category catalog
- Authenticated shopping cart
- Order lifecycle with stock control (reserve, confirm, rollback)
- Shipping address CRUD
- Saved payment methods (Card, Bank Transfer, Cash)
- Admin panel: dashboard, customers, products, orders, and categories
- Local product image storage (`/media`)
- CORS configurable for frontends (e.g. `http://localhost:3000`)
- Interactive OpenAPI documentation (`/docs`)

---

## Tech stack

| Layer | Technology | Notes |
|-------|------------|-------|
| **Language** | Python | 3.11+ |
| **API framework** | FastAPI | REST + OpenAPI |
| **ASGI server** | Uvicorn | Hot reload in development |
| **Validation** | Pydantic v2 | Request/response schemas |
| **ORM** | SQLAlchemy 2 | Models and queries |
| **Migrations** | Alembic | Versioned schema |
| **Database** | PostgreSQL 15 | Primary persistence |
| **Cache / sessions** | Redis 7 | Refresh tokens and password reset |
| **Authentication** | JWT + bcrypt | Access + refresh tokens |
| **Rate limiting** | SlowAPI | Auth endpoint protection |
| **Storage** | Local filesystem | Images in `uploads/` |
| **Containers** | Docker Compose | API + PostgreSQL + Redis |
| **Testing** | pytest, pytest-cov, fakeredis | 44 tests, 88% coverage |
| **CI** | GitHub Actions | Automated tests on push/PR |

No cloud, payment processor, or external email dependencies. Runs locally with Docker.

---

## Architecture

```
HTTP Client
     │
     ▼
FastAPI  (/api/v1/*)
     │
     ├── Router  →  Service  →  Repository  →  PostgreSQL
     │
     ├── Redis (auth tokens)
     └── uploads/ → /media (images)
```

Layered pattern: **Router → Service → Repository → Model**.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

---

## Getting started

```bash
git clone https://github.com/Donovan-Nudrak/E_commerce.git
cd E_commerce
cp .env.example .env

# Set SECRET_KEY and POSTGRES_PASSWORD in .env

docker compose up -d
docker compose exec api alembic upgrade head
docker compose exec api python -m app.database.seed
```

### Local URLs

| Resource | URL |
|----------|-----|
| API | http://localhost:8000 |
| Health check | http://localhost:8000/ |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Uploaded images | http://localhost:8000/media/products/… |

**Seed admin credentials:** `admin@ecommerce.com` / `admin1234`

### Docker commands

```bash
docker compose up -d      # Start services
docker compose stop       # Stop services
docker compose down       # Stop and remove containers
docker compose ps         # Check status
docker compose logs -f    # Tail logs
```

| Service | Host port |
|---------|-----------|
| API | 8000 |
| PostgreSQL | 5433 |
| Redis | 6379 |

---

## API modules

All routes are under the `/api/v1` prefix:

| Prefix | Description | Auth |
|--------|-------------|------|
| `/auth` | Register, login, refresh, logout, password reset, `GET /me` | Mixed |
| `/users` | Profile read, update, and account deletion | Customer |
| `/categories` | Public category listing | Public |
| `/products` | Catalog, search, offers, featured | Public |
| `/cart` | Shopping cart | Customer |
| `/orders` | Create, list, detail, cancel orders | Customer |
| `/payments` | Saved payment methods (CRUD) | Customer |
| `/addresses` | Shipping addresses (CRUD) | Customer |
| `/payment-types` | Available payment types | Public |
| `/admin` | Dashboard, orders, customers, products, categories | Admin |

Product and category write operations are available only under `/admin/*`.

### User profile

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/users/profile` | Current customer profile |
| `PUT` | `/api/v1/users/profile` | Update `first_name`, `last_name`, `phone` |
| `DELETE` | `/api/v1/users/profile` | Delete account (204) |

`GET /api/v1/auth/me` returns the same `UserProfileResponse` schema as `/users/profile`.

Account deletion removes cart, addresses, and payment methods. It is blocked if the customer has order history (`400`).

---

## Order flow

```
PENDING  →  PAID  →  SHIPPED  →  DELIVERED
    │
    └── CANCELLED (stock restored)
```

1. Customer creates an order from the cart → `PENDING` (stock reserved).
2. Admin confirms payment → `PUT /admin/orders/{id}/status` with `PAID`.
3. Admin manages fulfillment → `SHIPPED` → `DELIVERED`.

---

## Business rules

- Account deletion is blocked if the customer has order history.
- Stock is reserved on order creation and restored on cancellation.
- Soft delete on products — inactive products are hidden from the public catalog but preserved in order history.
- Discount price must be lower than the original price (validated on the backend).
- Password reset token expires in 30 minutes and is single-use.

---

## Environment variables

Copy `.env.example` to `.env`:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | JWT signing key (required; change for any shared environment) |
| `POSTGRES_*` | PostgreSQL connection |
| `REDIS_*` | Redis connection |
| `UPLOAD_DIR` | Image directory (default: `uploads`) |
| `MEDIA_URL_PREFIX` | Media URL prefix (default: `/media`) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins (e.g. `http://localhost:3000`). Empty = CORS disabled |
| `PASSWORD_RESET_BASE_URL` | Optional; reset link/token is written to application logs |

---

## Testing

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest

# With coverage (70% minimum threshold)
pytest tests/ --cov=app --cov-fail-under=70
```

Current status: **44 passing tests**, **88% coverage**.

Integration tests cover auth, users, cart, categories, products, addresses, orders, and payments:

```
tests/
├── conftest.py
├── integration/
│   ├── test_auth_api.py
│   ├── test_users_api.py
│   ├── test_cart_api.py
│   ├── test_categories_api.py
│   ├── test_products_api.py
│   ├── test_addresses_api.py
│   ├── test_orders_lifecycle.py
│   └── test_payments_api.py
└── unit/
    └── test_admin_service.py
```

CI runs on every push/PR to `main` or `develop` via `.github/workflows/ci.yml`.

---

## Project structure

```
E_commerce/
├── app/
│   ├── api/v1/          # HTTP routers (auth,users,cart,orders,admin,…)
│   ├── core/            # Config, security, constants
│   ├── database/        # Session, seed, base migrations
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access (incl. role, customer, product, …)
│   ├── schemas/         # Pydantic DTOs (auth, user, cart, …)
│   ├── services/        # Business logic (UserService, AuthService, …)
│   └── utils/           # Storage, password reset logging
├── alembic/             # Database migrations
├── tests/               # Unit and integration tests
├── docker-compose.yml
├── Dockerfile
├── main.py              # FastAPI entry point
└── requirements.txt
```

---
