#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "172.21.36.2"
#define SERVER_PORT 5018

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

    int max_datagram_size = 100000;

    char message[max_datagram_size];
    char buffer[1024];
    int message_size = 2;
    bool failed_send = false;
    bool found_max = false;

    while (true) {
        message[0] = message_size & 0xFF;
        message[1] = (message_size >> 8) & 0xFF;
        message[2] = (message_size >> 16) & 0xFF;
        message[3] = (message_size >> 24) & 0xFF;

        for (int i = 4; i < message_size + 4; ++i) {
            message[i] = 'A' + (i % 26);
        }

        ssize_t sent_bytes = sendto(sock, message, message_size + 4, 0, (struct sockaddr*)&server_addr, sizeof(server_addr));
        if (sent_bytes != message_size + 4) {
            failed_send = true;
            std::cout << "Failed to send datagram of size " << message_size + 4 << std::endl;
            message_size -= 1;
            usleep(5000);
            continue;   
        } else {
            std::cout << "Sent datagram of size " << message_size + 4 << " bytes, message size: "<< message_size << std::endl;
            if(failed_send)
            {
                found_max = true;
            }
        }

        struct sockaddr_in from_addr;
        socklen_t from_len = sizeof(from_addr);
        ssize_t recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr*)&from_addr, &from_len);
        if (recv_len > 0) {
            std::string feedback = std::string(buffer, recv_len);
            std::cout << "Received acknowledgment: " << feedback << std::endl;
            if(feedback != "OK")
            {
                std::cout << "Invalid packet received from server, sending message of same size again." << std::endl;
                sleep(1);
                continue;
            }
        } else {
            std::cout << "No acknowledgment received" << std::endl;
        }

        if(found_max)
        {
            std::cout << "Maximum datagram size sent: " << message_size + 4 << std::endl;
            break;
        }
        message_size = message_size * 2;
        sleep(1);
    }

    close(sock);
    return 0;
}