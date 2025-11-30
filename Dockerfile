# === STAGE 1: Build & Install Dependencies ===
# Build stage to install packages efficiently and discard intermediate build tools later.
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies needed for building psycopg2, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# === STAGE 2: Final Production Image ===
# Start fresh with a clean, minimal image (this keeps the final image size small)
FROM python:3.11-slim

WORKDIR /app

# Define the installation path for Python executables
ENV PATH="/usr/local/bin:$PATH"

# Copy only the installed Python packages from the builder stage
# Note: /usr/local/bin typically holds the executables/scripts
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/

# Reinstall *only* the runtime OS-level dependencies (no build-essential needed now)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the actual application source code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

WORKDIR /app/billing_system

# Start the application using Gunicorn (Production HTTP Server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "billing_system.wsgi:application"]
