# Use official Python 3.11 slim image for compatibility with ALT Linux and minimal size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for Prisma and PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Prisma CLI
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Prisma CLI globally
RUN npm install -g prisma

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Generate Prisma client
RUN prisma generate --schema=app/database/schema.prisma

# Expose port for FastAPI
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]