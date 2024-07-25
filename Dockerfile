# Use a non-root user for enhanced security
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create a non-root user
RUN useradd -ms /bin/bash appuser
USER appuser

# Create a directory for the app
WORKDIR /app

# Copy only necessary files (requirements.txt first)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8080

# Run the application with gunicorn and increased timeout
CMD ["gunicorn", "--timeout", "120", "-b", "0.0.0.0:8080", "app:app"]
