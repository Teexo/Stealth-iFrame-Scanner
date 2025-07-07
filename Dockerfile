FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    chromium \
    chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Install SQLmap
RUN wget https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip -O sqlmap.zip && \
    unzip sqlmap.zip && \
    mv sqlmap-master /usr/local/bin/sqlmap && \
    rm sqlmap.zip

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "stealth_iframe_scanner.py"]
