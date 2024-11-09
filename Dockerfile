# Use a base image that includes TeX Live
FROM texlive/texlive

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the application
COPY . .

# Create output directory
RUN mkdir -p output && chmod 777 output

# Expose port
EXPOSE $PORT

# Start command
CMD gunicorn run:app --bind 0.0.0.0:$PORT