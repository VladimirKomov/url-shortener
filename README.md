# URL Shortener API

## 📌 Description
A URL shortening service similar to Bit.ly that allows users to shorten long URLs and retrieve statistics about their usage. The service uses **FastAPI** for the backend, **PostgreSQL** for persistent storage, **Redis** for caching, and is deployable with **Docker & Kubernetes**.

## 🚀 Features
### 🔹 Backend (FastAPI + PostgreSQL + Redis)
- **Shorten a long URL** (`POST /shorten/`) ➝ Returns a short code.
- **Redirect to the original URL** (`GET /s/{short_code}/`) ➝ Redirects to the original long URL.
- **Get click statistics** (`GET /stats/{short_code}/`) ➝ Returns the number of times a short URL has been accessed.
- **Redis caching** for frequently used URLs to reduce database queries.
- **Asynchronous database operations** using SQLAlchemy and `asyncpg`.
- **Optimized background tasks** for updating click counts without blocking requests.

### 🔹 Frontend (React)
- **User-friendly interface** for shortening URLs.
- **Copy to clipboard button** for easy sharing.
- **Display of click statistics** for each shortened URL.

## 🛠 Tech Stack
- **Backend:** FastAPI, PostgreSQL, Redis, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (Persistent Storage), Redis (Cache)
- **Frontend:** React, Axios
- **Deployment:** Docker, Kubernetes, CI/CD (optional)


## ⚡ Quick Start
### 1️⃣ **Run with Docker**
```sh
docker-compose up --build
```
### 2️⃣ **Run manually**
#### **Backend**
```sh
cd backend
uvicorn app.main:app --reload
```
#### **Frontend**
```sh
cd frontend
npm install
npm start
```

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
**GET** `/s/{short_code}/`
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
