FROM python:3-slim

WORKDIR /app

COPY client.py .

RUN pip install --no-cache-dir pycryptodome

ENTRYPOINT ["python3", "-u", "client.py"]
