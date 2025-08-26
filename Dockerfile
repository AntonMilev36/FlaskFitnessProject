# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt if available
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Default command to run the app
CMD ["python", "app.py"]
