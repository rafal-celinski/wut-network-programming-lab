FROM python:3-slim

WORKDIR /app

COPY client.py .

RUN pip install --no-cache-dir pycryptodome
RUN apt-get update && apt-get install -y tcpdump

ENTRYPOINT ["python3", "-u", "client.py"]
