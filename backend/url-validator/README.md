# 🔍 URL Validator Microservice

This microservice is responsible for validating URLs using the **Google Safe Browsing API**. It operates asynchronously as a Kafka consumer and is a critical part of the URL Shortener system's safety layer.

---

## 📌 Description

- Consumes messages from the `url_validation` Kafka topic.
- Each message contains a short code and original URL.
- Checks the safety of the URL using **Google Safe Browsing**.
- Stores validation results in **MongoDB** for traceability and analytics.
- Sends the result to a response topic (e.g. `url_validation_result`) for the main application to update its records.

---

## 🧱 Tech Stack

| Component      | Technology                       |
|----------------|----------------------------------|
| Runtime        | Python 3.12 + Asyncio            |
| Web Client     | [httpx](https://www.python-httpx.org/) (async HTTP) |
| Kafka Client   | aiokafka                         |
| Database       | MongoDB (Motor async client)     |
| Validation     | Google Safe Browsing API         |
| Schema         | Pydantic models (shared)         |
| Messaging      | Kafka                            |

---

## 📦 Project Structure

```
validator_app/
├── core/             # Configs and logger
├── databases/        # Kafka and MongoDB clients
├── services/         # Business logic and Google checker
├── main.py           # Entry point
```

---

## ⚙️ How it works

1. Waits for Kafka messages on topic `url_validation`
2. Validates the `original_url` using the Google API
3. Writes the result into MongoDB:
    - Safe or unsafe
    - Threat type(s)
    - Timestamp
4. Sends a response to `url_validation_result` topic for further processing

---

## ▶️ Running Locally

> Requires a running Kafka broker and MongoDB instance (see docker-compose in root project)

```bash
# Activate your environment
poetry shell

# Run the validator
cd backend/url-validator
python validator_app/main.py
```

---

## 🔐 Google Safe Browsing API

You must configure your `.env` with a valid Google API key:

---

## 🥪 Testing

Unit and integration tests (planned). Currently testable via manual Kafka message production or mocking.

---

## 📄 Kafka Message Format

### Incoming (from main service):
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com"
}
```

### Outgoing (to result topic):
```json
{
  "short_code": "abc123",
  "is_safe": true,
  "validated_at": "2025-03-24T22:30:00Z",
  "threat_types": []
}
```

---

## ✅ Status

- ✅ Kafka consumer
- ✅ Google Safe Browsing integration
- ✅ MongoDB logging
- ✅ Kafka response publishing (planned)

---

## ✨ Future Enhancements

- Retry mechanism for failed API calls
- TTL index for MongoDB storage
- Validation result deduplication/cache
- CLI or dashboard for unsafe link review

---