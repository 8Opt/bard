#!/bin/bash

# Exit immediately if a command fails
set -e

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    set -a  # Automatically export variables
    source .env
    set +a  # Disable automatic export
else
    echo "⚠️ .env file not found! Ensure it exists in the current directory."
    exit 1
fi

# Validate ENVIRONMENT variable (default to "prod" if not set)
ENVIRONMENT=${ENVIRONMENT:-dev}

# Run FastAPI based on the environment mode
if [[ "$ENVIRONMENT" == "dev" ]]; then
    echo "🚀 Running FastAPI in development mode..."
    fastapi dev app --host 0.0.0.0 --port ${PORT:-7777}
else
    echo "🚀 Running FastAPI in production mode..."
    fastapi run app --host 0.0.0.0 --port  ${PORT:-7777}
fi