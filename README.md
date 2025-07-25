# Async Media Generation Microservice

## Overview

This project implements an **asynchronous media generation microservice** using **FastAPI**, **Celery**, **Redis**, and **SQLModel**. It enables users to submit text prompts that are processed in the background to generate media (e.g., images) via the Replicate API.


## Tech Stack

| Tool        | Purpose                             |
|-------------|-------------------------------------|
| FastAPI     | Async API layer                     |
| Celery      | Background task execution           |
| Redis       | Celery message broker               |
| SQLModel    | Async ORM for job metadata storage  |
| Alembic     | Schema migrations                   |
| Docker      | Containerized deployment            |
| .env        | Environment variable management     |


## Project Structure


```bash
.
├── app/
│   ├── config/           # Celery and env setup
│   ├── crud/             # DB operations
│   ├── database/         # DB connection management
│   ├── models/           # SQLModel schemas
│   ├── routers/          # API routes
│   ├── schemas/          # Request/response models
│   ├── services/         # Media generation and storage
│   ├── tasks/            # Celery tasks
│   └── main.py           # FastAPI entry point
├── alembic/              # DB migrations
├── media/                # Output media files
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── requirements.txt

```


## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:NJ-186/async-media-generator.git
cd async-media-generator
```

### 2. Configure Environment

Create a .env file based on .env.example. Defaults are used if not provided.

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

This launches:

- FastAPI app at `http://localhost:8000`
- Celery worker
- Redis broker
- Automatic Alembic migration

Visit `http://localhost:8000/docs` for API docs.


## Manual Setup (Without Docker)

### Prerequisites

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


## API Endpoints

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
  "job_id": "bc2c32cf-9a77-4b36-9533-e50ac26d7632",
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

## Notes

- To test edge cases, modify the mocked client in app/services/client.
- Retry logic can be verified in app/tasks/async_tasks.
