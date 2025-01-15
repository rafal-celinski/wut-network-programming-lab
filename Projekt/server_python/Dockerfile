FROM python:3-slim

WORKDIR /app

COPY server.py .

RUN pip install --no-cache-dir pycryptodome

ENTRYPOINT ["python3", "-u", "server.py"]
