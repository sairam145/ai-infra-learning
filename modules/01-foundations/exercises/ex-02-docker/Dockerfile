# Start from a small Linux image with Python already installed
FROM python:3.12-slim

# All following commands run inside /app in the container
WORKDIR /app

# Copy ONLY the requirements first, then install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Now copy the application code
COPY src/ ./src/

# Document that the app listens on port 8000
EXPOSE 8000

# What runs when the container starts. 0.0.0.0 = accept connections from outside the container
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
