# Use official Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy current project files into container
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy .env file into the container
COPY .env /app/.env

# Expose the port Flask runs on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "src/app.py"]
