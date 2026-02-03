# Dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY pyproject.toml uv.lock /app/
RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync

COPY . /app

# Use gunicorn to serve the Flask app; Render injects $PORT
CMD ["uv run", "gunicorn", "main:app", "-w", "4", "-b", "0.0.0.0:$PORT"]
