# Use the Playwright image that matches the pinned Python Playwright version.
FROM mcr.microsoft.com/playwright/python:v1.59.0-noble

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install Python dependencies for the worker.
COPY requirements.txt requirements-worker.txt ./
RUN pip install --no-cache-dir -r requirements-worker.txt

# Copy project files
COPY . .

# Command to run the worker
CMD ["python", "worker/main.py"]
