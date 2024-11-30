#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>
#include <chrono>

#define SERVER_IP "172.21.36.2"
#define SERVER_PORT 8080
#define BUFFER_SIZE 100000

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cout << "Failed to create socket" << std::endl;
        return -1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    if(bind(sock, (struct sockaddr*)& server_addr, sizeof(server_addr)) < 0) {
        std::cout << "Failed to bind" << std::endl;
        return -1;
    }

    if(listen(sock, 0) < 0) {
        std::cout << "Failed to listen" << std::endl;
        return -1;
    }

    std::cout << "Server listening on " << SERVER_IP << ":" << SERVER_PORT << std::endl;

    int client_socket;
    struct sockaddr_in client_address;

    client_socket = accept(sock, (struct sockaddr*)& client_address, sizeof(client_address));
    if (client_socket < 0) {
        std::cout << "Failed to accept" << std::endl;
        close(sock);
        return -1;
    }

    close(sock);
    std::cout << "Client connected - closing socket to prevent other connections" << std::endl;

    char buffer[BUFFER_SIZE] = {0};
    auto last_time = std::chrono::high_resolution_clock::now();
    while (true) {
        int bytes_received = read(client_socket, buffer, BUFFER_SIZE);
        if (bytes_received > 0) {
            auto current_time = std::chrono::high_resolution_clock::now();
            auto difference = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - last_time).count();
            std::cout << "Received message from client of size: " << bytes_received <<std::endl;
            std::cout << "Time since last message: " << difference << " ms" << std::endl;

            last_time = current_time;
            std::memset(buffer, 0, BUFFER_SIZE);
            sleep(3);
        }
        else {
            std::cout<< "End of connection" << std::endl;
            break;
        }
    }

    close(client_socket);
    return 0;
}