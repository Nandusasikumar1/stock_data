FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir \
    requests==2.32.3 \
    APScheduler==3.10.4

COPY test.py .

CMD ["python", "test.py"]
