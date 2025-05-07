# 📊 Statistics Microservice

This microservice is responsible for collecting and storing click statistics in the **URL Shortener System**. It consumes messages from RabbitMQ and saves detailed data about each click to **MongoDB**.

---

## 📌 Description

- Listens to click events via RabbitMQ (topic exchange).
- Each message contains data about a click on a shortened URL.
- Stores IP, User-Agent, Referer, and timestamp.
- Provides an HTTP API to retrieve click statistics by `shortCode`.

---

## 🧱 Tech Stack

| Component    | Technology            |
|-------------|------------------------|
| Framework   | NestJS (TypeScript)    |
| Database    | MongoDB (Mongoose)     |
| Messaging   | RabbitMQ (topic mode)  |
| Transport   | `@nestjs/microservices`|

---

## 📦 Project Structure

```
statistics-service/
├── src/
│   ├── controllers/        # HTTP API
│   ├── services/           # Business logic
│   ├── consumers/          # RabbitMQ consumer
│   ├── models/             # Mongoose schemas
│   ├── mappers/            # Mapping input/output
│   ├── dto/                # DTOs for requests/responses
│   ├── utils/              # Logger etc.
│   ├── app.module.ts
│   ├── main.ts
│   ├── rabbitmq.options.ts
│   ├── mongo.options.ts
```

---

## ⚙️ How it works

1. Waits for RabbitMQ messages on routing key `click_events`.
2. Parses message and stores it in MongoDB.
3. HTTP endpoint `/stats/:shortCode` returns recent clicks.
4. Optional `?limit=N` query param controls result count.

---

## ▶️ Running Locally

```bash
# install deps
npm install

# start service in dev mode
npm run start:dev
```

> Requires running MongoDB and RabbitMQ. You can use Docker to spin them up.

---

## 🧪 Example Message

RabbitMQ message body:

```json
{
  "short_code": "abc123",
  "ip_address": "127.0.0.1",
  "user_agent": "PostmanRuntime/7.43.3",
  "referer": null,
  "timestamp": "2025-05-07T16:36:24.267Z"
}
```

---

## 🌐 HTTP API

**GET /stats/:shortCode**

Query Parameters:
- `limit` (optional) — number of records (default: 100, max: 500)

Response:
```json
[
  {
    "shortCode": "abc123",
    "ipAddress": "127.0.0.1",
    "userAgent": "PostmanRuntime/7.43.3",
    "referer": null,
    "timestamp": "2025-05-07T16:36:24.267Z"
  }
]
```
---

## ✅ Status

- ✅ MongoDB integration
- ✅ RabbitMQ consumer (topic exchange)
- ✅ Statistics controller
- ✅ Click mappers and DTOs

---

## ✨ Future Enhancements

- Authentication and rate limiting
- Aggregated statistics (e.g. total clicks per hour)
- Export to CSV or Excel
- Pagination in API

---