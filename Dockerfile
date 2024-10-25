# Use the Python image
FROM python:3.10

# Update packages and install missing libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app
WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "r2music.py"]
