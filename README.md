# Project launch
This is the basis, the app and database run without problems in Docker.
The project has a Clean Architecture, designed for scalability and resilience to errors.
**The system is not yet ready for production.**

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
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=canary_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
---
### Build and run the project

```bash
docker compose up --build
```