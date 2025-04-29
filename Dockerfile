# -------------------
# Base image with system deps
# -------------------

FROM python:3.12-slim-bullseye AS base

# Ensure Python 3.10 is used
ENV PYTHONPATH=/app \
    PYTHON_VERSION=3.10

ENV DEBIAN_FRONTEND=noninteractive

# Install system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    fonts-liberation \
    fonts-noto-color-emoji \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxss1 \
    libxtst6 \
    libgtk-3-0 \
    libasound2 \
    libxrandr2 \
    libu2f-udev \
    xdg-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# -------------------
# Builder stage
# -------------------
FROM base AS builder

WORKDIR /app

# Install uv dependency manager
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

ENV PATH="/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy app source code
COPY app/ /app/app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# -------------------
# Final runtime image
# -------------------
FROM base AS runtime

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=2

# Copy only what's needed for runtime
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app

RUN playwright install --with-deps chromium

# Expose port if the serves an API
EXPOSE 8000
