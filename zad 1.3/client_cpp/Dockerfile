FROM gcc:4.9

WORKDIR /app

COPY client.cpp .

RUN g++ -std=c++11 client.cpp -o client

CMD ["./client"]
