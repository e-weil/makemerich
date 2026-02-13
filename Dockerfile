# MakeMeRich — Production Dockerfile — by FORGE
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy app files
COPY app/ ./app/

# Copy API server
COPY app/api/app.py ./api/app.py

EXPOSE 8000

CMD ["uvicorn", "app.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
