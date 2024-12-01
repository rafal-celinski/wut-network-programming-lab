FROM gcc:4.9

WORKDIR /app

COPY server.cpp .

RUN g++ -o server server.cpp

CMD ["./server"]
