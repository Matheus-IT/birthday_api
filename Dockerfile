FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

COPY requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.dev.txt

COPY ./app .
