# 🖼️ Async Media Generation Microservice

## Overview

This project implements an **asynchronous media generation microservice** using **FastAPI**, **Celery**, **Redis**, and **SQLModel**. It enables users to submit text prompts that are processed in the background to generate media (e.g., images) via the Replicate API.

---


## 🧪 API Endpoints

### 1. `POST /generate`

Submits a prompt for media generation.

**Request**
```json
{
  "prompt": "A futuristic city at sunset",
  "parameters": "{\"width\":512,\"height\":512}"
}
```

**Response**
```json
{
  "job_id": "bc2c32cf-9a77-4b36-9533-e50ac26d7632",
  "status": "queued"
}
```

### 2. `GET /status/{job_id}`

Fetches the status and result of a submitted job.

**Successful Response**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "result_url": "/media/bc2c32cf-9a77-4b36-9533-e50ac26d7632.png"
}
```

**Failed Response**
```json
{
  "job_id": "bc2c32cf-9a77-4b36-9533-e50ac26d7632",
  "status": "failed",
  "error": "API timeout while calling Replicate."
}
```

---

## ⚙️ Tech Stack

| Tool        | Purpose                             |
|-------------|-------------------------------------|
| FastAPI     | Async API layer                     |
| Celery      | Background task processing          |
| Redis       | Celery message broker               |
| SQLModel    | Async ORM for job metadata storage  |
| httpx       | Async HTTP client (Replicate calls) |
| Alembic     | Schema migrations                   |
| Docker      | Containerized deployment            |
| .env        | Environment variable management     |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com:NJ-186/async-media-generator.git
cd async-media-generator
```

### 2. Set Environment Variables

Create a `.env` file as per `.env.example` file in the root directory. Even if you don't set an env file, the project is designed to have default values

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

This will launch:

- FastAPI app at `http://localhost:8000`
- Celery worker
- Redis broker
- Automatic Alembic migration

Visit `http://localhost:8000/docs` for API docs.

---

## 🧭 Manual Setup (Without Docker)

### Requirements

- Python 3.11+
- Redis (running locally)

### Steps

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Start Redis (if not already running):

    ```bash
    redis-server
    ```

3. Set environment variables via `.env` or shell.

4. Apply database migrations:

    ```bash
    alembic upgrade head
    ```

5. Start Celery worker:

    ```bash
    celery -A app.config.celery_app.celery worker --loglevel=info
    ```

6. Run FastAPI server:

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

---

## 📁 Project Structure

```bash
.
├── app/
│   ├── config/              # Initialises celery app and environment variables
│   ├── crud/                # CRUD operations on models
│   ├── database/            # Manages database connections
│   ├── models/              # SQLModel definitions
│   ├── routers/             # API Routes
│   ├── schemas/             # API Request & Response Schemas
│   ├── services/            # Media generation, storage, Replicate client
│   ├── tasks/               # Celery task definitions
│   └── main.py              # FastAPI entry point
├── alembic/                 # DB migrations
├── alembic.ini
├── media/                   # Media file output
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── pyproject.toml
├── .pre-commit-config.yaml
├── README.md
└── requirements.txt
```

---

## 🔁 Retry Logic

- Failed jobs are retried automatically with **exponential backoff**.
- Retry count and error details are persisted in the database.
