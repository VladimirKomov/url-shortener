# 🔗 URL Shortener API

A scalable, event-driven URL shortening service inspired by Bit.ly. Built with a modern backend stack and designed for performance, reliability, and extensibility.

---

## 📌 Description

This project provides a backend service for shortening long URLs and tracking their usage statistics. The system is designed with production-grade technologies and patterns, including **asynchronous processing**, **caching**, **event streaming**, and **microservices architecture**.

---

## 🚀 Features

### ⚙️ Core Functionality (Backend)
- `POST /shorten/` – Shorten a long URL.
- `GET /go/{short_code}/` – Redirect to the original URL.
- `GET /stats/{short_code}/` – Return usage statistics (click count).

### 🧠 Architecture Highlights
- **Asynchronous FastAPI backend** with `asyncpg` and SQLAlchemy.
- **Redis caching** to accelerate repeated URL lookups and reduce DB load.
- **Kafka-based event system** for decoupled analytics, logging, and security modules.
- **Modular database layer** using PostgreSQL for persistent storage.
- **Background tasks** update usage data without blocking user-facing endpoints.

---

## 🧱 Tech Stack

| Layer           | Technology                            |
|----------------|----------------------------------------|
| **Backend**     | FastAPI, Pydantic, SQLAlchemy (async) |
| **Database**    | PostgreSQL (persistent), Redis (cache)|
| **Messaging**   | Kafka                                  |
| **DevOps**      | Docker, Kubernetes (deployment-ready) |
| **CI/CD**       | GitHub Actions (planned)              |
| **Frontend**    | React + Axios (planned)               |

---

## 📦 Running the Service

### ⚡ Docker (recommended)
```bash
docker-compose up --build
```

### 2️⃣ **🧪 Local (manual)**
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (when ready)
cd frontend
npm install
npm start

## 🌐 API Endpoints
### 1️⃣ Shorten a URL
**POST** `/shorten/`
#### Request:
```json
{
  "long_url": "https://example.com"
}
```
#### Response:
```json
{
  "short_url": "http://localhost:8000/go/a1b2c3"
}
```

### 2️⃣ Redirect to Original URL
**GET** `/go/{short_code}/`
- Redirects the user to the original long URL.

### 3️⃣ Get URL Statistics
**GET** `/stats/{short_code}/`
#### Response:
```json
{
  "short_code": "a1b2c3",
  "clicks": 42
}
```
✅ Status
✅ Backend core functionality (API, DB, Redis, Kafka) – Implemented
🔄 Frontend and CI/CD – Planned
📈 Extensible architecture for analytics and LLM-based security – Designed
