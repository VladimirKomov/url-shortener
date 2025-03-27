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
| Schema         | Pydantic models (shared-models)  |
| Messaging      | Kafka                            |

---

## 📦 Project Structure

```
validator_app/
├── core/             # Configs, logger, bootstrap container
├── messaging/        # Kafka producer & consumer clients
├── databases/        # MongoDB client
├── schemas/          # Optional internal schemas (if any)
├── services/         # Business logic and Google checker
├── repositories/     # MongoDB repository layer
├── mappers/          # Kafka message transformation
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

> Requires a running Kafka broker and MongoDB instance (see `docker-compose.yml` in the root project)

```bash
# Activate your environment
poetry shell

# Install dependencies
poetry install

# Run the validator
poetry run python validator_app/main.py
```

---

## 🔐 Google Safe Browsing API

You must configure your `.env` with a valid Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## 🥪 Testing

Unit and integration tests are planned.
Currently, the service can be tested by manually producing Kafka messages or using mocks.

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
  "original_url": "https://example.com",
  "is_safe": true,
  "checked_at": "2025-03-24T22:30:00Z",
  "threat_types": [],
  "details": "Checked via Google Safe Browsing"
}
```

---

## ✅ Status

- ✅ Kafka consumer
- ✅ Google Safe Browsing integration
- ✅ MongoDB logging
- ✅ Kafka producer (response publishing)

---

## ✨ Future Enhancements

- Retry mechanism for failed API calls
- TTL index for MongoDB validation results
- Result caching / deduplication
- Internal metrics / Prometheus
- CLI or dashboard for unsafe link monitoring

---