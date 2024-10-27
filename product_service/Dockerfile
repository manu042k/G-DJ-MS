# Base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8001

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
