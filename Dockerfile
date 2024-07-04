# Use the official Python image from the Python foundation
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=social_network.settings

# Define the command to run the Django application using the built-in server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# (Optional) Add a health check to ensure the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
