# 🖼️ Async Media Generation Microservice

## Overview

This project implements an **asynchronous media generation microservice** built using **FastAPI**, **Celery**, **Redis**, and **SQLModel**. It allows users to submit text prompts that are processed in the background to generate media (e.g., images) via the Replicate API (mocked or real). The system emphasizes clean, modular architecture with asynchronous I/O, robust error handling, and containerized deployment.

---

## 🚀 Features

- **Async API** to submit media generation requests and check job status  
- **Background processing** using Celery and Redis (message broker)  
- **Persistent storage** of jobs, metadata, and results using SQLModel  
- **Media storage** on local file system (S3-compatible interface ready)  
- **Dockerized setup** with `docker-compose` for easy local deployment  
- **Alembic migrations** for schema versioning  
- **Async-compatible I/O** for HTTP, DB, and file operations  

---

## 🧩 Architecture

```mermaid
flowchart TD
    User["User"]
    FastAPI["FastAPI API"]
    Redis["Redis (Broker)"]
    Celery["Celery Worker"]
    Replicate["Replicate API (Mocked)"]
    DB["SQLModel (SQLite / PostgreSQL)"]
    Media["Media Storage (Local / S3-compatible)"]

    User -->|POST /generate| FastAPI
    FastAPI -->|Enqueue Job| Redis
    Celery -->|Fetch Job| Redis
    Celery -->|Generate Media| Replicate
    Celery -->|Save Result| Media
    Celery -->|Update Status| DB
    User -->|GET /status/{job_id}| FastAPI
    FastAPI -->|Read Job Status| DB
