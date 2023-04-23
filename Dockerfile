# Dockerfile

# Base image for Django application
FROM python:3.10

# Set the environment variable PYTHONUNBUFFERED for the container
ENV PYTHONUNBUFFERED=1

# Create a directory for the application code
RUN mkdir /code
WORKDIR /code

# Install dependencies for the Django application
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the container
COPY . /code/