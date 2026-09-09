# Business Service Management Platform

A production-style business operations backend designed to manage the complete lifecycle of services and customer service requests through a secure, scalable REST API.

The platform provides a centralized system for businesses to publish and manage their service offerings, onboard and authenticate customers, receive service requests, prioritize incoming work, and manage requests through defined operational stages. It supports separate customer and administrator workflows using JWT authentication and role-based access control, ensuring that users can access only the functionality appropriate to their role.

The backend is built with **FastAPI, PostgreSQL, SQLAlchemy, Redis, and Docker**, following a modular architecture that separates API routing, business logic, database models, authentication, authorization, and infrastructure concerns. The application also includes interactive **Swagger/OpenAPI documentation** and automated **Pytest integration tests** for validating core API workflows.

The project demonstrates how a Python backend can be structured to support real-world business operations rather than functioning as a simple CRUD application. It combines authentication, authorization, relational data management, service workflows, request prioritization, administrative controls, API documentation, testing, and containerized development into a single backend platform.

---

## Features

### 🔐 Authentication & Authorization

- JWT-based authentication
- Secure password hashing
- Customer and Administrator roles
- Role-based access control
- Protected API endpoints
- Current-user profile

### 🏢 Service Management

- Business service catalog
- Service pricing and descriptions
- Activate/deactivate services
- Public service browsing
- Admin service management

### 📋 Service Requests

- Customer service requests
- Request priority levels
- Request status tracking
- Customer request history
- Admin request management
- Request lifecycle management

### 👥 Business Workflows

- Separate customer and admin workflows
- Role-protected administrative operations
- Service availability validation
- Request-to-service relationships

### 🗄️ Database & Infrastructure

- PostgreSQL database
- SQLAlchemy ORM
- Redis integration
- Dockerized application environment
- Docker Compose setup

### 🧪 Testing

- Pytest test suite
- Authentication tests
- Service API tests
- Service request tests
- Integration testing

### 📖 API Documentation

- OpenAPI specification
- Swagger UI
- ReDoc
- Customized Swagger interface

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
