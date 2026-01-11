# JAIson Unified - Dockerfile
# Lightweight, production-friendly image for the core server

FROM python:3.12-slim

# metadata
LABEL maintainer="tulovec96 <tulovec96@users.noreply.github.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for audio and ffmpeg (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# copy project
COPY . /app

# install python deps
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# create a non-root user
RUN useradd -m jaisonuser || true
USER jaisonuser

EXPOSE 7272 7273

# default command: start core server
CMD ["python", "src/main.py"]
