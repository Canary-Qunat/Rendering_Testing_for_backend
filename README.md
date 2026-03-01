# Canary Backend

A modular and scalable backend built with FastAPI, following Clean Architecture principles and modern async patterns.

---
## Features

- **Clean Architecture**
  - Clear separation of concerns: Domain, Application, Infrastructure, Presentation
  - Dependency inversion with repository interfaces
  - Explicit wiring and dependency management


- **Authentication System**
  - JWT-based authentication
  - Short-lived **Access Token**
  - Long-lived **Refresh Token**
  - Secure refresh token storage (hashed in database)
  - Logout with refresh token revocation


- **Security**
  - Password hashing using **Argon2**
  - JWT signature verification
  - Environment-based configuration
  - CORS support


- **Database**
  - PostgreSQL
  - Async driver (**asyncpg**)
  - Connection pooling
  - Explicit repository pattern (no ORM, no SQLAlchemy)
  - SQL-first approach for performance and control


- **Async Architecture**
  - Fully async request lifecycle
  - Async database access
  - Application-level async services


- **Modular API Structure**
  - Auth endpoints
  - Zerodha integration (planned) 
  - Portfolio and trading endpoints

---

## Tech Stack

- Python 3.11+
- FastAPI
- asyncpg
- PostgreSQL
- Pydantic Settings
- Argon2
- Poetry

---

## Architectural Overview

The project follows a layered architecture:

- **Domain**: Entities and repository interfaces
- **Application**: Business logic and services
- **Infrastructure**: Database, JWT, security, persistence
- **Presentation**: FastAPI routers and schemas

---

## Authentication Flow

1. User registers with email & password

2. Password is hashed with Argon2

3. Login returns:
   - Access Token (short-lived)
   - Refresh Token (stored hashed in DB)
   
4. Logout revokes the refresh token


---
## Installation and setup

### Requirements

Make sure you have installed:

- Docker
- Docker Compose (v2+)

```bash
docker --version
docker compose version
```
---
### Clone the repo
```bash
git clone <https://github.com/Canary-Qunat/Rendering_Testing_for_backend>
cd </Rendering_Testing_for_backend>
```
---
### Configure environment variables

```bash
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=canary
POSTGRES_HOST=db
POSTGRES_PORT=5432 

ACCESS_TOKEN_MINUTES=10 (recommended)
REFRESH_TOKEN_DAYS=30 (recommended)

JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256 
```
---
### Build and run the project

```bash
docker compose up --build
```