FROM python:3.12-slim

WORKDIR /app

COPY shortener_service/pyproject.toml shortener_service/poetry.lock ./
COPY shared_models ./shared_models
COPY shortener_service/app ./app

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]