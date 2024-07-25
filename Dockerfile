# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app

# Set the working directory
WORKDIR /app

# Copy the service account key into the container
COPY path_to_your_service_account_key.json /app/service_account_key.json

# Set environment variable for the credentials path
ENV GOOGLE_APPLICATION_CREDENTIALS="C:/Users/tharu/Downloads/bold-camera-429007-i5-db9a9cd22bf5.json"

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
