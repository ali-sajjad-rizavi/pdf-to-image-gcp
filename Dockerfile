# Use an official Python runtime as a base image
FROM python:3.11-slim

# Install Poppler (for pdf2image)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your function
CMD ["functions-framework", "--target=main"]
