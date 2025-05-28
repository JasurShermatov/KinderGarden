# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for PostgreSQL client and potential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    # postgresql-client is included in libpq-dev for Debian slim images
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# Includes src/, migrations/, alembic.ini, manage.py etc.
COPY . .

# Make run.sh executable (assuming it's still needed and copied)
# If run.sh is not in the root, adjust the path
COPY run.sh .
RUN chmod +x run.sh

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# This might need adjustment based on run.sh content and the new structure
# Assuming run.sh handles migrations and starts uvicorn pointing to src.app:app
CMD ["sh", "-c", "./run.sh"]
