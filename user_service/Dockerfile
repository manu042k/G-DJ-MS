# # Base image
# FROM python:3.10-slim

# # Set work directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy project files
# COPY . .

# # Expose port
# EXPOSE 8000

# # Run Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run Django migrations and start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
