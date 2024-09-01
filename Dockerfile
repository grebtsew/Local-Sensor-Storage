# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg, ping, and other necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    iputils-ping && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run your application
CMD ["python", "main.py"]
