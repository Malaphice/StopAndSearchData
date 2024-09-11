# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Set the environment variables for Flask
ENV FLASK_APP=runserver.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask when the container launches
CMD ["flask", "run"]
