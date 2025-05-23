# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the command to start the Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3000"]
