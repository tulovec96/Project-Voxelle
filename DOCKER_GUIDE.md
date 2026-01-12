# Docker Support Guide

This guide covers running Voxelle in Docker containers.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Files](#docker-files)
- [Building Images](#building-images)
- [Running Containers](#running-containers)
- [Docker Compose](#docker-compose)
- [Multi-Stage Builds](#multi-stage-builds)
- [Optimization Tips](#optimization-tips)

---

## Quick Start

### Build and Run with Docker

```bash
# Build image
docker build -t voxelle:latest .

# Run container
docker run -it \
  --env-file .env \
  -v $(pwd)/configs:/app/configs \
  -v $(pwd)/logs:/app/logs \
  voxelle:latest
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Docker Files

### Dockerfile

```dockerfile
# Voxelle Dockerfile - Multi-stage build for optimization

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Build wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

---

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages from wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY src ./src
COPY configs ./configs
COPY prompts ./prompts

# Create logs directory
RUN mkdir -p logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["python", "-u", "src/main.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  voxelle:
    build: .
    image: voxelle:latest
    container_name: voxelle
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    ports:
      - "8000:8000"
      - "8080:8080"
    volumes:
      - ./configs:/app/configs
      - ./logs:/app/logs
      - ./models:/app/models
      - ./output:/app/output
    restart: unless-stopped
    networks:
      - voxelle-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Database service
  postgres:
    image: postgres:15-alpine
    container_name: voxelle-db
    environment:
      POSTGRES_DB: voxelle
      POSTGRES_USER: voxelle
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - voxelle-net
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  voxelle-net:
    driver: bridge
```

---

## Building Images

### Development Build

```bash
# Build with development dependencies
docker build -t voxelle:dev -f Dockerfile.dev .

# Run development container with volume mount
docker run -it \
  -v $(pwd):/app \
  -v /app/venv \
  voxelle:dev
```

### Production Build

```bash
# Build optimized production image
docker build -t voxelle:prod \
  --build-arg ENVIRONMENT=production .

# Run production container
docker run -d \
  --name voxelle-prod \
  --restart=always \
  --env-file .env.prod \
  voxelle:prod
```

### Build Arguments

```bash
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t voxelle:latest .
```

---

## Running Containers

### Basic Run

```bash
docker run voxelle:latest
```

### With Environment File

```bash
docker run --env-file .env.docker voxelle:latest
```

### With Volume Mounts

```bash
docker run -it \
  -v $(pwd)/configs:/app/configs \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/models:/app/models \
  voxelle:latest
```

### Port Mapping

```bash
# Map container ports to host
docker run -p 8000:8000 -p 8080:8080 voxelle:latest

# Map to different host port
docker run -p 9000:8000 voxelle:latest
```

### Resource Limits

```bash
docker run \
  --memory=2g \
  --cpus=2 \
  --memory-swap=3g \
  voxelle:latest
```

### Interactive Terminal

```bash
# Start container with interactive shell
docker run -it voxelle:latest /bin/bash
```

---

## Docker Compose

### Starting Services

```bash
# Start all services in background
docker-compose up -d

# Start with rebuild
docker-compose up --build -d

# Start specific service
docker-compose up -d voxelle
```

### Managing Services

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs voxelle

# Follow logs
docker-compose logs -f voxelle

# Execute command in container
docker-compose exec voxelle python src/main.py --help

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Remove services
docker-compose down

# Remove with volumes
docker-compose down -v
```

### Environment Configuration

Create `.env` file:

```bash
DISCORD_TOKEN=your_token_here
TWITCH_TOKEN=your_token_here
DB_PASSWORD=secure_password
DEBUG=false
LOG_LEVEL=INFO
API_PORT=8000
```

---

## Multi-Stage Builds

### Optimized Build Example

```dockerfile
# Stage 1: Dependency builder
FROM python:3.11-slim as dependency-builder

WORKDIR /tmp

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir ./wheels -r requirements.txt

---

# Stage 2: Development dependencies (optional)
FROM dependency-builder as dev-dependencies

COPY requirements-dev.txt .

RUN pip wheel --no-cache-dir --wheel-dir ./wheels -r requirements-dev.txt

---

# Stage 3: Final production image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 voxelle

# Copy wheels from builder
COPY --from=dependency-builder /tmp/wheels /tmp/wheels

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels -r requirements.txt \
    && rm -rf /tmp/wheels

# Copy application
COPY --chown=voxelle:voxelle src ./src
COPY --chown=voxelle:voxelle configs ./configs
COPY --chown=voxelle:voxelle prompts ./prompts

# Switch to non-root user
USER voxelle

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-u", "src/main.py"]
```

---

## Optimization Tips

### Reduce Image Size

```dockerfile
# Use slim base images
FROM python:3.11-slim

# Multi-stage builds (separate build and runtime)
# Combine RUN commands to reduce layers
RUN apt-get update && apt-get install -y packages \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Use .dockerignore to exclude unnecessary files
```

### Security Best Practices

```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 voxelle
USER voxelle

# Don't run as root
# Scan images for vulnerabilities
# Keep base images updated
# Use specific version tags, not 'latest'
```

### Performance

```dockerfile
# Layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src ./src  # Only invalidates cache if source changes

# Health checks
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/health

# Resource limits in compose
services:
  voxelle:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Monitoring

```bash
# View image layers
docker history voxelle:latest

# Inspect container
docker inspect voxelle

# View statistics
docker stats voxelle

# Check logs
docker logs voxelle
```

---

## Troubleshooting

### Container Won't Start

```bash
# View logs
docker logs voxelle

# Run in interactive mode
docker run -it voxelle:latest /bin/bash

# Check exit code
docker inspect voxelle | grep ExitCode
```

### Network Issues

```bash
# Check networks
docker network ls

# Inspect network
docker network inspect voxelle-net

# Connect container to network
docker network connect voxelle-net container_name
```

### Volume Issues

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect volume_name

# Check mounted volumes
docker inspect -f '{{ json .Mounts }}' container_name
```

---

For more Docker information, see official [Docker Documentation](https://docs.docker.com/).
