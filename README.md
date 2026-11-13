# Assignment 11 — Secure FastAPI Calculator API

A secure FastAPI calculator application extended with SQLAlchemy data models, Pydantic v2 validation, a Simple Factory Pattern for arithmetic operations, bcrypt password hashing, JWT authentication, PostgreSQL integration testing, and automated CI/CD deployment to Docker Hub.

Assignment 11 builds on the existing Assignment 10 application by introducing a `Calculation` model, request and response schemas, and comprehensive tests for calculation data persistence and validation.

**Note:** This assignment focuses on modeling, validation, and testing. Calculation BREAD endpoints will be implemented in Module 12.

---

## Features

### Calculator API

- Arithmetic endpoints: `POST /add`, `/subtract`, `/multiply`, and `/divide`.
- Input validation and division-by-zero handling.
- `GET /health` endpoint for application and Docker health monitoring.

### SQLAlchemy Models

**User Model**
- Unique usernames and email addresses.
- Secure password storage using bcrypt hashing.
- User authentication and account management functionality.
- User creation and update timestamps.

**Calculation Model**
- `id`: Unique calculation identifier.
- `a`: First numeric operand.
- `b`: Second numeric operand.
- `type`: Arithmetic operation type.
- `result`: Stored calculation result.
- Database constraints preventing unsupported operations and division by zero.

### Pydantic Validation

- `UserCreate` and `UserRead` for user validation and serialization.
- `CalculationCreate` for validating calculation operands and operation types.
- `CalculationRead` for serializing stored calculation records.
- Enum validation for supported operations: `Add`, `Sub`, `Multiply`, and `Divide`.
- Validation rejecting invalid numeric inputs, unsupported operations, and zero divisors.
- Response schemas that do not expose password hashes.

### Simple Factory Pattern

A dictionary-based `CalculationFactory` selects and executes the appropriate arithmetic operation.

Supported operations:
- Addition
- Subtraction
- Multiplication
- Division

The factory reuses the existing arithmetic functions, separates calculation selection from other application logic, and provides a foundation for future extensibility.

### Authentication and Security

- Password hashing and verification using Passlib/bcrypt.
- JWT-based authentication.
- Pydantic input validation.
- PostgreSQL integrity constraints.
- Docker image vulnerability scanning with Trivy.

### Automated Testing and Deployment

- Pytest unit tests.
- PostgreSQL-backed integration tests.
- Playwright end-to-end tests.
- Application code coverage reporting.
- GitHub Actions CI/CD automation.
- Docker image building, security scanning, and Docker Hub publishing.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Application programming language |
| FastAPI | Web application framework |
| Uvicorn | ASGI application server |
| SQLAlchemy | ORM and database modeling |
| Pydantic v2 | Data validation and serialization |
| PostgreSQL 16 | Relational database |
| psycopg2 | PostgreSQL database driver |
| Passlib / bcrypt | Password hashing |
| JWT | Authentication |
| pytest | Unit and integration testing |
| pytest-cov | Code coverage reporting |
| Playwright | End-to-end browser testing |
| Docker / Docker Compose | Application containerization |
| GitHub Actions | Continuous integration and deployment |
| Trivy | Docker image security scanning |

---

## Project Structure

```text
assignment11/
├── .github/
│   └── workflows/
│       └── test.yml
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── calculation.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── calculation.py
│   ├── operations/
│   │   ├── __init__.py
│   │   └── factory.py
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── database_init.py
├── templates/
│   └── index.html
├── tests/
│   ├── unit/
│   │   ├── test_app_init.py
│   │   ├── test_calculation.py
│   │   ├── test_calculator.py
│   │   └── test_database_coverage.py
│   ├── integration/
│   │   ├── test_calculation.py
│   │   └── ...existing integration tests
│   ├── e2e/
│   │   └── test_e2e.py
│   └── conftest.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pytest.ini
├── requirements.txt
├── README.md
└── REFLECTION.md
```

The project retains the existing Assignment 10 user, authentication, database, and API functionality.

---

## Local Setup (Ubuntu / WSL)

### 1. Prerequisites

Install:

- Python 3.14
- Git
- Docker and Docker Compose
- A compatible PostgreSQL environment

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/assignment11.git
cd assignment11
```

Replace the repository URL with your actual GitHub repository URL.

### 3. Create a Virtual Environment

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Upgrade pip and install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

### 4. Configure Environment Variables

Create a local `.env` file.

Generate a secure JWT signing key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Example `.env` configuration when running FastAPI directly from WSL and using PostgreSQL on host port `5433`:

```dotenv
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/fastapi_db
SECRET_KEY=REPLACE_WITH_YOUR_GENERATED_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The credentials are examples for local development only. Never commit `.env` or real secrets to GitHub.

---

## Run with Docker Compose

Start the FastAPI application, PostgreSQL, and pgAdmin:

```bash
docker compose up -d --build
docker compose ps
```

Available services:

- FastAPI application: http://localhost:8000/
- Swagger API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- pgAdmin: http://localhost:5050/

The Compose services must expose the corresponding host ports for these URLs to work.

Verify application health:

```bash
curl -i http://localhost:8000/health
```

Expected response:

```text
HTTP/1.1 200 OK
```

```json
{"status": "healthy"}
```

Stop the containers while preserving database volumes:

```bash
docker compose down
```

### PostgreSQL Port Configuration

Assignment 11 uses a separate PostgreSQL container configuration to avoid conflicts with Assignment 10.

| Connection | Port |
|---|---|
| PostgreSQL host port | 5433 |
| PostgreSQL container port | 5432 |
| FastAPI running inside Docker | db:5432 |
| FastAPI running directly in WSL | localhost:5433 |

If Docker Compose exposes PostgreSQL through a different host port, update the environment variables accordingly.

---

## Calculation Model and Validation

### Calculation Model

The SQLAlchemy `Calculation` model is defined in:

`app/models/calculation.py`

It stores the operands, operation type, and computed result.

Database constraints validate supported operation types and reject division by zero.

### CalculationCreate Schema

Defined in:

`app/schemas/calculation.py`

Example valid calculation:

```python
from app.schemas.calculation import CalculationCreate

calculation = CalculationCreate(
    a=10,
    b=5,
    type="Add",
)
```

Example invalid calculation:

```python
CalculationCreate(
    a=10,
    b=0,
    type="Divide",
)
```

The second example raises a Pydantic `ValidationError` because division by zero is not permitted.

### CalculationRead Schema

The `CalculationRead` schema serializes a stored calculation into a validated response object.

Returned fields include `id`, `a`, `b`, `type`, and `result`.

---

## Simple Factory Pattern

The factory implementation is located in:

`app/operations/factory.py`

The `CalculationFactory` uses an operation registry to select the correct arithmetic function.

Example:

```python
from app.operations.factory import CalculationFactory

result = CalculationFactory.calculate(
    10, 5, "Add"
)

print(result)
```

Expected output:

```text
15
```

The factory supports all four arithmetic operations and raises an error when an unsupported operation is supplied.

This design provides reusable calculation logic for the BREAD endpoints planned in Module 12.

---

## Run Tests Locally

Integration tests use a separate PostgreSQL database named `fastapi_test_db`.

**Important:** The test setup can drop and recreate database tables. Never point the test suite at a development or production database containing important data.

### 1. Start PostgreSQL

```bash
docker compose up -d db
```

Verify:

```bash
docker compose ps
```

### 2. Create the Test Database

```bash
docker compose exec db \
  psql -U postgres -d postgres \
  -c "CREATE DATABASE fastapi_test_db;"
```

Skip database creation if the database already exists.

### 3. Configure the Test Database URL

For WSL with PostgreSQL exposed on port `5433`:

```bash
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5433/fastapi_test_db"
```

### 4. Run Calculation Unit Tests

```bash
python -m pytest tests/unit/test_calculation.py -v
```

These tests validate arithmetic operations, factory selection, Pydantic input validation, and invalid calculation handling.

### 5. Run Calculation Integration Tests

```bash
python -m pytest tests/integration/test_calculation.py -v
```

These tests verify database insertion, retrieval, response serialization, and PostgreSQL constraints.

### 6. Run Application Initialization Tests

```bash
python -m pytest tests/unit/test_app_init.py -v
```

These tests verify database initialization, cleanup, and execution of the application's initialization script.

### 7. Start FastAPI for E2E Testing

The Playwright tests require a running FastAPI server.

Start the server in the background:

```bash
nohup python -m uvicorn main:app \
  --host 127.0.0.1 \
  --port 8000 \
  > uvicorn.log 2>&1 &
```

Verify the server is available:

```bash
curl http://127.0.0.1:8000/
```

View logs:

```bash
tail -f uvicorn.log
```

### 8. Run All Tests

```bash
python -m pytest --run-slow -v
```

### 9. Run Tests with 100% Coverage Enforcement

```bash
python -m pytest --run-slow -v \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=100
```

Open `htmlcov/index.html` to inspect the detailed coverage report.



## CI/CD with GitHub Actions

The project uses GitHub Actions to automate testing, security scanning, and Docker image publishing.

The combined pipeline is maintained in:

`.github/workflows/test.yml`

### 1. Automated Testing

The testing job:

- Starts a PostgreSQL 16 service.
- Installs Python dependencies.
- Configures the test environment.
- Installs Playwright Chromium.
- Starts the FastAPI application.
- Runs existing user tests and new calculation tests.
- Enforces 100% application code coverage.
- Generates coverage reports.

### 2. Docker Image Build and Security Scan

After testing succeeds, the workflow builds a Docker image and scans it with Trivy.

Trivy identifies vulnerabilities based on the configured severity threshold.

A passing security scan does not guarantee that the image contains no vulnerabilities.

### 3. Docker Hub Deployment

The deployment job publishes the Docker image to Docker Hub after successful preceding jobs.

The current workflow is configured to deploy from the `main` branch. Deployment from `assignment11-calculation` requires updating the workflow's branch configuration or merging into `main`.

### GitHub Repository Configuration

Navigate to:

**GitHub → Repository Settings → Secrets and variables → Actions**

Configure:

| Type | Name | Purpose |
|---|---|---|
| Repository variable | `DOCKERHUB_USERNAME` | Docker Hub username |
| Repository secret | `DOCKERHUB_TOKEN` | Docker Hub access token |

Do not store access tokens, passwords, or JWT secrets directly in workflow YAML files.

---

## Docker Hub Image

**Docker Hub repository:** [aby3989/assignment11](https://hub.docker.com/repository/docker/aby3989/assignment11/general)

The project currently uses the existing Docker Hub repository from Assignment 11.

After successful deployment, pull the image using:

```bash
docker pull aby3989/assignment11:latest
```

The published application requires a valid JWT secret and a reachable PostgreSQL database.

Configure `DATABASE_URL` and `SECRET_KEY` through the runtime environment. The application image does not automatically provide a PostgreSQL database.

### Verify the Image

Check the downloaded image:

```bash
docker images
```

Run the application through an appropriately configured Docker environment and verify the health endpoint:

```bash
curl http://localhost:8000/health
```

A successful response confirms that the running FastAPI application is responding.

---

## Assignment 11 Testing Summary

| Component | Testing |
|---|---|
| Arithmetic operations | Unit tests |
| Calculation Factory | Unit tests |
| CalculationCreate validation | Unit tests |
| CalculationRead serialization | Integration tests |
| SQLAlchemy Calculation model | Unit and integration tests |
| PostgreSQL persistence | Integration tests |
| Invalid operation constraints | Integration tests |
| Division by zero | Unit and integration tests |
| Existing User functionality | Existing Assignment 10 tests |
| FastAPI endpoints | Integration and E2E tests |
| Application initialization | Unit tests |
| CI/CD pipeline | GitHub Actions |

---
