# Use a slim Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Matplotlib (fonts and rendering)
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY arxiv-network-graph.py .

# Create a folder for the output
RUN mkdir output

# Run the script
CMD ["python", "arxiv-network-graph.py"]