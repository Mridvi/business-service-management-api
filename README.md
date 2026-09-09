# Business Service Management Platform

A production-style business operations backend for managing business services, customer requests, and administrative workflows through a secure REST API.

The platform allows businesses to maintain a service catalog, authenticate users, receive and prioritize customer requests, and manage requests through a defined lifecycle. It supports separate customer and administrator workflows using **JWT authentication** and **role-based access control**.

Built with **FastAPI, PostgreSQL, SQLAlchemy, Redis, and Docker**, the project follows a modular backend architecture with interactive **Swagger/OpenAPI documentation** and automated **Pytest testing**.

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
- Administrator service management

### 📋 Service Requests

- Customer service requests
- Request priority levels
- Request status tracking
- Customer request history
- Administrator request management
- Request lifecycle management

### 👥 Business Workflows

- Separate customer and administrator workflows
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

- Automated testing with Pytest
- Authentication and authorization tests
- Service API tests
- Service request workflow tests
- Integration testing

### 📖 API Documentation

- OpenAPI specification
- Interactive Swagger UI
- ReDoc documentation
- Customized Swagger interface

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
| Infrastructure | Redis |
| Documentation | Swagger / OpenAPI / ReDoc |
| Testing | Pytest |
| Containerization | Docker / Docker Compose |
| Version Control | Git / GitHub |

---

## API Structure

All endpoints are versioned under `/api/v1`.

### Authentication

```text
POST   /api/v1/auth/login
GET    /api/v1/auth/me
```

### Services
```text
POST   /api/v1/auth/login
GET    /api/v1/auth/me
GET    /api/v1/services/
GET    /api/v1/services/{service_id}

```

###Customer Requests

```text
POST   /api/v1/auth/login
GET    /api/v1/auth/me
POST   /api/v1/requests/
GET    /api/v1/requests/
GET    /api/v1/requests/{request_id}
```

###Administrator Services
```text
POST   /api/v1/auth/login
GET    /api/v1/auth/me
POST   /api/v1/admin/services
PUT    /api/v1/admin/services/{service_id}
DELETE /api/v1/admin/services/{service_id}
POST   /api/v1/auth/login
GET    /api/v1/auth/me

```
Administrator Requests
```text
GET    /api/v1/admin/requests
PUT    /api/v1/admin/requests/{request_id}/status


```

## Getting Started
### Prerequisites

### Make sure the following are installed:
```text
Python 3.10+
Docker
Docker Compose
Git
```
### Clone the Repository
```text
git clone https://github.com/Mridvi/business-service-management-api.git
cd business-service-management-api

```

### Environment Configuration
```text
Create a .env file based on .env.example:
cp .env.example .env
```
### Configure the environment variables:
```text

POSTGRES_DB=business_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your_secret_key
```

Do not commit your .env file or real credentials to GitHub.

### Run with Docker
```text

docker compose up --build
```

### The API will be available at:
```text
http://localhost:8000
```

### API Documentation

-Swagger UI
```text
http://localhost:8000/docs
```
-Custom Swagger UI
```text
http://localhost:8000/custom-docs
```
-ReDoc
```text
http://localhost:8000/redoc
```
-Run Tests
```text
pytest
```
The test suite uses an isolated test environment for database and Redis-dependent tests.


## Authentication Flow

The API uses JWT-based authentication.
```text
User
 │
 │ Login Credentials
 ▼
Authentication API
 │
 │ Validate Credentials
 ▼
JWT Access Token
 │
 │ Authorization: Bearer <token>
 ▼
Protected API Endpoint
 │
 ▼
Role Verification
 │
 ├───────────────┐
 ▼               ▼
Customer     Administrator
```


## Business Workflow

A typical customer interaction follows this flow:
```text
Browse Available Services
          │
          ▼
     Select Service
          │
          ▼
  Submit Service Request
          │
          ▼
    Set Request Priority
          │
          ▼
        PENDING
          │
          ▼
     IN_PROGRESS
          │
       ┌──┴──┐
       │     │
       ▼     ▼
  COMPLETED CANCELLED

  
```


## Design Highlights
### Modular Backend Architecture
The application separates:
-API routing
-Request and response schemas
-Database models
-Authentication
-Authorization

This improves maintainability and makes the backend easier to extend.

### API Versioning

Application endpoints are organized under:
```text
/api/v1
```
This provides a structured foundation for future API versions.

### Role-Based Access Control
Customer and administrator functionality is separated to protect sensitive business operations.

### Service Availability
Inactive services remain stored in the database but cannot be selected for new service requests.

### Request Prioritization
Requests can be assigned different priority levels, allowing administrators to distinguish between routine requests and urgent business requirements.

### Request Lifecycle
Service requests move through defined operational states, providing a clear workflow from submission to completion or cancellation.




## Future Improvements
-Email notifications
-Request comments and communication history
-File/document attachments
-Service categories
-Customer dashboards
-Analytics and reporting
-Cloud deployment

## Learning Outcomes
This project demonstrates practical experience with:

-Python backend development
-FastAPI REST API development
-RESTful API design
-PostgreSQL database integration
-SQLAlchemy ORM
-JWT authentication
-Role-based authorization
-Business workflow implementation
-Redis integration
-Docker and Docker Compose
-Automated API testing


## Author

Mridvi Sharma
Computer Science & Engineering
Python Backend Developer | FastAPI | SQL | AI/ML




