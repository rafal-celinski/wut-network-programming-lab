FROM python:3-slim

RUN apt-get update && apt-get install -y iproute2 && apt-get clean

WORKDIR /app

COPY server.py .

CMD ["python3", "-u", "server.py"]
