FROM python:3-slim

WORKDIR /app

COPY server.py .

RUN pip install --no-cache-dir pycryptodome
RUN apt-get update && apt-get install -y tcpdump && apt-get install -y net-tools

ENTRYPOINT ["python3", "-u", "server.py"]
