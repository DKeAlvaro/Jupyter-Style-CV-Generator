# Use a base image that includes TeX Live
FROM texlive/texlive

# Install Python and venv
RUN apt-get update && \
    apt-get install -y python3-full python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install Python packages in venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create output directory
RUN mkdir -p output && chmod 777 output

# Expose port
EXPOSE $PORT

# Start command using venv python
CMD gunicorn run:app --bind 0.0.0.0:$PORT