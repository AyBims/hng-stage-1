# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# The port is now set by Cloud Run via the PORT environment variable
# Default to 8080 for local development
ENV PORT=8080

# Run the application with Uvicorn when the container launches
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
