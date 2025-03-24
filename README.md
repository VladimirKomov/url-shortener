# 🔗 URL Shortener API

A scalable, event-driven URL shortening service inspired by Bit.ly. Built with a modern backend stack and designed for performance, reliability, and extensibility.

---

## 📌 Description

This project provides a backend service for shortening long URLs and tracking their usage statistics. It is designed with production-grade technologies and patterns, including **asynchronous processing**, **event streaming**, **microservices**, and **URL safety validation** using Google's Safe Browsing API.

---

## 🚀 Features

### ⚙️ Core Functionality (Backend)
- `POST /shorten/` – Shorten a long URL.
- `GET /go/{short_code}/` – Redirect to the original URL.
- `GET /stats/{short_code}/` – Return usage statistics (click count).
- 🔐 Asynchronous **URL validation** through Kafka + Google Safe Browsing.
- ⚠️ New URLs are **inactive by default** until validated as safe.

### 🧠 Architecture Highlights
- **Asynchronous FastAPI backend** with `asyncpg` and SQLAlchemy.
- **Redis caching** to accelerate repeated URL lookups and reduce DB load.
- **Kafka-based microservices** for decoupled validation, logging, and analytics.
- **MongoDB** used by the validator microservice for audit/logging.
- **Modular service boundaries** for core logic and background processing.
- **Event-driven design** for safety and scalability.

---

## 🧱 Tech Stack

| Layer           | Technology                             |
|-----------------|----------------------------------------|
| **Backend**     | FastAPI, Pydantic, SQLAlchemy (async)  |
| **Database**    | PostgreSQL (persistent), Redis (cache) |
| **Validation**  | Kafka + MongoDB + Google Safe Browsing |
| **Messaging**   | Kafka                                  |
| **DevOps**      | Docker, Kubernetes (planned)           |
| **CI/CD**       | GitHub Actions (planned)               |
| **Frontend**    | React + Axios (planned)                |

---

## 🧪 URL Validation Workflow

1. User submits a URL to shorten.
2. It's stored with `is_valid = False` and a unique short code.
3. The original URL is sent to a Kafka topic.
4. The `url-validator` microservice:
    - Receives the message.
    - Checks the URL with Google Safe Browsing.
    - Saves the result in MongoDB.
    - Sends back a Kafka message with validation status.
5. The main service consumes the result and updates the original record.

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
✅ URL Validator microservice with Google Safe Browsing – Partly
🔄 Frontend and CI/CD – Planned  
📈 Extensible architecture for analytics and LLM-based security – Designed  

🧠 Inspiration
This project showcases how to build a real-world, production-oriented system using modern Python, asynchronous architecture, and microservice communication via Kafka. It also demonstrates real-world use of external APIs for safe browsing validation.
