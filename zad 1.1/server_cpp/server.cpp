#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "172.21.36.2"
#define SERVER_PORT 5018

void send_feedback(int sock, const char* ack, sockaddr_in* client_addr, socklen_t client_len){
    ssize_t sent_bytes = sendto(sock, ack, strlen(ack), 0, (struct sockaddr*)client_addr, client_len);
    if (sent_bytes < 0) {
        std::cout << "Failed to send acknowledgment" << std::endl;
    }
}

int main() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        std::cout << "Failed to create socket" << std::endl;
        return -1;
    }

    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    int max_datagram_size = 100000;
    
    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cout << "Failed to bind socket" << std::endl;
        return -1;
    }

    std::cout << "Server listening on " << SERVER_IP << ":" << SERVER_PORT << "..." << std::endl;

    char buffer[max_datagram_size];

    while (true) {
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr*)&client_addr, &client_len);
        
        if (recv_len < 0) {
            std::cout << "Failed to receive datagram" << std::endl;
            break;
        }

        if (recv_len < 4) {
            std::cout << "Received datagram with insufficient size for message length" << std::endl;
            continue;
        }

        unsigned int message_size = (static_cast<uint8_t>(buffer[3]) << 24)| (static_cast<uint8_t>(buffer[2]) << 16)| (static_cast<uint8_t>(buffer[1]) << 8) | static_cast<uint8_t>(buffer[0]);  // Combine the 2 bytes into the message size
        std::cout << "Declared message size: " << message_size << " bytes" << std::endl;

        if (message_size + 4 == recv_len) {
            std::cout << "Message length validated successfully for datagram of size " << message_size + 4 <<std::endl;
            send_feedback(sock, "OK", &client_addr, client_len);
        } else {
            std::cout << "Message length validation failed! Expected " << message_size + 4 << " bytes, but got " << recv_len << " bytes." << std::endl;
            send_feedback(sock, "FAIL", &client_addr, client_len);
        }
    }
    close(sock);
    return 0;
}
