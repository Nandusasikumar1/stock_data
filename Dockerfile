FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    requests==2.32.3 \
    APScheduler==3.10.4

# Copy the application
COPY app.py .

# Run the script
CMD ["python3", "app.py"]
