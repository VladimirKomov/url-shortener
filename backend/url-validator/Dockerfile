FROM python:3.12-slim

WORKDIR /app

COPY url-validator/pyproject.toml url-validator/poetry.lock ./
COPY shared_models ./shared_models
COPY url-validator/validator_app ./validator_app

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

ENV PYTHONPATH=/app

CMD ["python", "validator_app/main.py"]
