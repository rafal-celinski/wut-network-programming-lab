#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>
#include <netinet/tcp.h>

#define SERVER_IP "172.21.36.2"
#define SERVER_PORT 8080
#define BUFFER_SIZE 200000

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
    socklen_t addr_len = sizeof(client_address);

    client_socket = accept(sock, (struct sockaddr*)& client_address, &addr_len);
    if (client_socket < 0) {
        std::cout << "Failed to accept" << std::endl;
        close(sock);
        return -1;
    }

    close(sock);
    std::cout << "Client connected - closing socket to prevent other connections" << std::endl;

    //Wyłączenie delayed ACK - nie wpływa na wyniki
    // int flag = 1; 
    // if (setsockopt(client_socket, IPPROTO_TCP, TCP_QUICKACK, &flag, sizeof(flag)) < 0) {
    //     std::cout << "Failed to disable delayed ACK" << std::endl;
    // } else {
    //     std::cout << "Disabled delayed ACK successful" << std::endl;
    // }

    char buffer[BUFFER_SIZE] = {0};
    while (true) {
        int bytes_received = read(client_socket, buffer, BUFFER_SIZE);
        if (bytes_received > 0) {
            std::cout << "Received message from client of size: " << bytes_received <<std::endl;
            sleep(1);
        }
        else if (bytes_received <= 0) {
            std::cout << "Error or disconnection occurred" << std::endl;
            break;
        }
    }
    close(client_socket);
    return 0;
}