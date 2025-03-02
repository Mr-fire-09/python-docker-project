# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy files into the container
COPY requirements.txt requirements.txt
COPY app.py app.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
