# Stage 1: Build dependencies in a virtual environment
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies into the venv
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final application image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the path to use the venv
ENV PATH="/opt/venv/bin:$PATH"

# Create and set the working directory
WORKDIR /app

# Copy the application code from your local machine
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]