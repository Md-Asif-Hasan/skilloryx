# Use Python slim base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies if needed (e.g., for Pillow)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (ignore errors if database isn't ready)
RUN python manage.py collectstatic --noinput --clear || true

# Expose port
EXPOSE 8000

# Create entrypoint script to run migrations and start server
RUN mkdir -p /app/scripts && \
    printf '#!/bin/bash\nset -e\necho "Running migrations..."\npython manage.py migrate --noinput\necho "Starting Daphne..."\nexec daphne main.asgi:application --bind 0.0.0.0 --port ${PORT:-8000}\n' > /app/scripts/entrypoint.sh && \
    chmod +x /app/scripts/entrypoint.sh

# Run the application
ENTRYPOINT ["/app/scripts/entrypoint.sh"]