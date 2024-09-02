FROM python:3.11-slim-buster

WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

# Create a non-root user
RUN useradd --create-home appuser

# Change ownership of the application files
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser
