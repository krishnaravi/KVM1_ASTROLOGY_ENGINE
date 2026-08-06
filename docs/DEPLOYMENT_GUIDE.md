# KVM1 Astrology Engine - Production Deployment Guide

## Production Server Setup

### 1. Uvicorn / Gunicorn Production Command

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

### 2. Environment Variables Configuration

| Variable | Description | Default |
|---|---|---|
| `REDIS_HOST` | Redis Server Hostname | `localhost` |
| `REDIS_PORT` | Redis Server Port | `6379` |
| `REDIS_PASSWORD` | Redis Server Auth Password | `None` |
| `CACHE_PROVIDER` | Cache provider (`memory`, `redis`, `two_level`) | `two_level` |
| `LOG_LEVEL` | Logging verbosity (`INFO`, `DEBUG`, `WARNING`) | `INFO` |

---

### 3. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```
