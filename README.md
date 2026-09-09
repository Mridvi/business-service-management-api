# Business Service Management Platform

A production-style backend platform for managing business services, customer service requests, administrative workflows, and request lifecycles through a secure REST API.

The system provides separate customer and administrator workflows, allowing businesses to publish and manage service offerings while customers can submit and track service requests. Administrators can manage the service catalog and control request processing through role-based access.

## Features

### 🔐 Authentication & Authorization

- JWT-based user authentication
- Secure password hashing
- Login and authenticated user sessions
- Role-based access control
- Customer and Administrator roles
- Protected API endpoints
- Current-user profile endpoint
- Admin-only operations

### 🏢 Business Service Catalog

- Create and manage business services
- Service name and description
- Service pricing
- Active/inactive service status
- Public service listing
- Retrieve individual service details
- Update service information
- Soft-delete/deactivate services
- Prevent customers from requesting inactive services

### 📋 Service Request Management

Customers can submit requests for available business services.

Each request contains:

- Customer information
- Selected business service
- Request description
- Request priority
- Request status
- Creation timestamp

Supported request priorities:

- LOW
- MEDIUM
- HIGH
- URGENT

Supported request lifecycle states:

- PENDING
- IN_PROGRESS
- COMPLETED
- CANCELLED

Customers can:

- Submit service requests
- View their own requests
- View individual request details
- Track request status and priority

Administrators can:

- View service requests
- Review customer requests
- Update request status
- Manage the request lifecycle

### 👥 Role-Based Business Workflows

The API separates functionality based on user roles.

**Customers**

- Access available services
- Create service requests
- View their own requests
- Track request progress

**Administrators**

- Manage the service catalog
- Create new services
- Update service information
- Activate/deactivate services
- Review customer requests
- Update request statuses

### 🗄️ Database Management

- PostgreSQL relational database
- SQLAlchemy ORM
- Structured relational models
- Foreign-key relationships
- Customer-service-request relationships
- Role-based user relationships
- Database-backed business workflows

### ⚡ Redis Integration

Redis is integrated into the backend infrastructure for application-level support such as authentication/session-related functionality and fast-access data operations.

### 🧪 Automated Testing

The project includes automated tests using Pytest.

Test coverage includes:

- Application startup
- Authentication workflows
- Protected endpoints
- Service operations
- Service request workflows
- Role-based access behavior
- API integration scenarios

The test suite runs against an isolated testing environment using SQLite and a Redis test setup.

### 📖 Interactive API Documentation

The API provides automatically generated OpenAPI documentation through Swagger UI.

Available documentation:

- `/docs` — Swagger UI
- `/redoc` — ReDoc
- `/custom-docs` — Customized Swagger UI

The customized documentation provides a cleaner interface for exploring and testing the API endpoints.

### 🐳 Dockerized Development

The application is containerized using Docker and Docker Compose.

The development environment includes:

- FastAPI application
- PostgreSQL database
- Redis

This allows the complete backend environment to be started consistently without manually configuring each service.

---

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Backend Framework | FastAPI |
| API Style | REST |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Security | Password Hashing |
| Caching / Infrastructure | Redis |
| API Documentation | Swagger / OpenAPI / ReDoc |
| Testing | Pytest |
| Containerization | Docker / Docker Compose |
| Version Control | Git / GitHub |

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │      Client         │
                    │  Swagger / API      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │     REST API        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Authentication     Business Logic     Authorization
          & JWT          Service Management    & RBAC
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ PostgreSQL   │      │    Redis     │
             │  Database    │      │ Infrastructure│
             └──────────────┘      └──────────────┘
