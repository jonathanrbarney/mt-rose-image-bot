# Use an official Python runtime as the base image
FROM python:3.11

# Metadata as described above
LABEL version="1.0"
LABEL description="Docker container for the webcam image processing script."

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

VOLUME /app/images

# Define environment variable (Optional. For example, if you have any)
# ENV NAME World

# Run the script when the container launches
CMD ["python", "auto_score.py"]
