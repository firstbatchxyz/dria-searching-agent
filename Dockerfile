# Stage 1: Builder
FROM python:3.10.14-slim as builder

RUN pip install poetry
WORKDIR /app
COPY . .

RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "server"]
